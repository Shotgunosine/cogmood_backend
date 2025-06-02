import os
import re
from hashlib import blake2b
from flask import (redirect, url_for, request, session)
from .io import write_metadata
from .config import CFG
from .utils import gen_code
from .utils import logging

def routing(ep):
    """Unify the routing to reduce repetition"""
    route_debug = CFG['route_debug']
    if route_debug:
        logging.info(f'Routing request for: {ep}')
    info = dict(
        workerId     = request.args.get('PROLIFIC_PID'),    # Prolific metadata
        assignmentId = request.args.get('SESSION_ID'),      # Prolific metadata
        hitId        = request.args.get('STUDY_ID'),        # Prolific metadata
        subId        = gen_code(24),                        # NivTurk metadata
        user_agent   = request.user_agent.string.lower(),   # User metadata
    )
    if route_debug:
        logging.info('Info contents')
        for k,v in info.items():
            logging.info(f"{k}: {v}")
        logging.info('Session contents')
        for k,v in session.items():
            logging.info(f"{k}: {v}")
    disallowed_agent = any([device in info['user_agent'] for device in CFG['disallowed_agents']])
    allowed_agent = any([device in info['user_agent'] for device in CFG['allowed_agents']])

    # Case 1: workerId absent from URL.
    try:
        h_workerId = blake2b(info['workerId'].encode(), digest_size=24).hexdigest()
    except AttributeError:
        if route_debug:
            logging.info('Failed case 1, no PROLIFIC_PID in url')
        ## Redirect participant to error (missing workerId).
        return redirect(url_for('error.error', errornum=1000))

    # complete might be written to metadata without updating session
    # because task uploading has no session
    if h_workerId in os.listdir(CFG['meta']):

        ## Parse log file.
        with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
            logs = f.read()

        # Grab str fields from logs
        fields = [
            'complete',
            'terminalerror',
            'taskinprogress'
        ]

        for field in fields:
            re_res = re.search(f'\t{field}\t(.*)\n', logs)
            if re_res:
                session[field] = re_res.group(1)

    # Case 2: mobile / tablet / game console user.
    # Not a terminal error because we want the user to be able to try again from a different device
    if disallowed_agent or not allowed_agent:
        if route_debug:
            logging.info(f'Failed case 2, agent {info["user_agent"]} not allowed')
        # Redirect participant to error (platform error).
        return redirect(url_for('error.error', errornum=1001))

    # Case 3: session has a terminal error
    elif 'terminalerror' in session:
        if route_debug:
            logging.info(f"Failed case 3, terminalerror {session['terminalerror']}")
        return redirect(url_for('error.error', errornum=int(session['terminalerror'])))

    # Case 4: previous complete.
    elif 'complete' in session:
        if route_debug:
            logging.info(f"Failed case 4, complete {session['complete']}")
            logging.info('Session contents')
            for k,v in session.items():
                logging.info(f"{k}: {v}")

        # Redirect participant to complete page.
        return redirect(url_for('complete.complete', **request.args))

    # Case 5 repeat visit, manually changed workerId.
    elif 'workerId' in session and session['workerId'] != info['workerId']:
        # Update metadata.
        session['terminalerror'] = 1005
        session['ERROR'] = '1005: workerId tampering detected.'
        session['complete'] = 'error'
        write_metadata(session, ['ERROR', 'complete', 'terminalerror'], 'a')

        # Redirect participant to error (unusual activity).
        return redirect(url_for('error.error', errornum=1005))

    # Case 6: workerid not in session
    elif not 'workerId' in session:
        if route_debug:
            logging.info("workerId not in session, rebuilding session")
        # Case 6a: metadata exists for workerid
        if h_workerId in os.listdir(CFG['meta']):

            ## Parse log file.
            with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
                logs = f.read()

            try:
                ## Extract subject ID.
                info['subId'] = re.search('subId\t(.*)\n', logs).group(1)
            except AttributeError:
                return redirect(url_for('error.error', errornum=1009))

            # grab fields with potential boolean values from logs
            bool_fields = [
                'survey',
                'consent',
                'alert',
                'dlstart',
                'dlready'
            ]

            for field in bool_fields:
                re_res = re.search(f'\t{field}\t(.*)\n', logs)
                if re_res and re_res.group(1) == 'True':
                    info[field] = True       # consent = true
                elif re_res and re_res.group(1) == 'False':
                    info[field] = False   # consent = false

            # Grab str fields from logs
            fields = [
                'complete',
                'terminalerror',
                'ERROR',
                'surveycomplete',
                'platform'
            ]

            for field in fields:
                re_res = re.search(f'\t{field}\t(.*)\n', logs)
                if re_res:
                    info[field] = re_res.group(1)

            for k, v in info.items():
                session[k] = v

            if 'macintosh' in info['user_agent']:
                session['platform'] = 'mac'
            else:
                session['platform'] = 'win'
            write_metadata(session, list(session.keys()), 'w')
            # Just a little recursion, once the session is updated, the routing rules will work.
            # This way we don't have to repeat the rules
            if route_debug:
                logging.info('Rebuilt Session contents')
                for k,v in session.items():
                    logging.info(f"{k}: {v}")
            return routing(ep)

        # case 6b: first visit, workerID present
        else:
            for k, v in info.items():
                session[k] = v
            if 'macintosh' in info['user_agent']:
                session['platform'] = 'mac'
            else:
                session['platform'] = 'win'
            write_metadata(session, [
                'workerId',
                'hitId',
                'assignmentId',
                'subId',
                'user_agent',
                'platform'
            ], 'w')

            return redirect(url_for('consent.consent', **request.args))

    # case 7: Not consented
    elif 'consent' not in session:
        if ep == 'consent':
            return
        else:
            return redirect(url_for('consent.consent', **request.args))


    # case 8: Not viewed alert
    elif ('alert' not in session) or not session['alert']:
        if ep == 'alert':
            return
        else:
            return redirect(url_for('alert.alert', **request.args))


    # case 9: Survey not complete and restarts not allwoed
    elif not CFG['allow_restart'] and 'survey' in session:

        ## Update participant metadata.
        session['terminalerror'] = 1004
        session['ERROR'] = "1004: Revisited survey."
        session['complete'] = 'error'
        write_metadata(session, ['terminalerror', 'ERROR', 'complete'], 'a')

        ## Redirect participant to error (previous participation).
        return redirect(url_for('error.error', errornum=1004))

    # case 10: Survey not complete
    elif 'surveycomplete' not in session:
        if ep == 'survey':
            return
        else:
            return redirect(url_for('survey.survey', **request.args))


    # case 11: download not started
    elif 'dlstart' not in session:
        if ep == 'taskstart':
            return
        else:
            return redirect(url_for('taskstart.taskstart', **request.args))

    # case 12: not complete
    else:
        return redirect(url_for('taskstart.taskstart', **request.args))
