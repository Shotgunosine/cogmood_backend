import os
import re
from hashlib import blake2b
from flask import (redirect, url_for, request, session)
from .io import write_metadata
from .config import CFG
from .utils import gen_code


def routing(ep):
    """Unify the routing to reduce repetition"""
    print(ep)
    info = dict(
        workerId     = request.args.get('PROLIFIC_PID'),    # Prolific metadata
        assignmentId = request.args.get('SESSION_ID'),      # Prolific metadata
        hitId        = request.args.get('STUDY_ID'),        # Prolific metadata
        subId        = gen_code(24),                        # NivTurk metadata
        address      = request.remote_addr,                 # NivTurk metadata
        user_agent   = request.user_agent.string,           # User metadata
    )
    print("running routing")
    print(info)
    print()
    print("session")
    print(session)
    # Case 1: workerId absent from URL.
    try:
        h_workerId = blake2b(info['workerId'].encode(), digest_size=20).hexdigest()
    except AttributeError:
        ## Redirect participant to error (missing workerId).
        return redirect(url_for('error.error', errornum=1000))


    # Case 2: mobile / tablet / game console user.
    # Not a terminal error because we want the user to be able to try again from a different device
    if any([device in info['user_agent'].lower() for device in CFG['disallowed_agents']]):

        # Redirect participant to error (platform error).
        return redirect(url_for('error.error', errornum=1001))

    # Case 3: session has a terminal error
    elif 'terminalerror' in session:

        return redirect(url_for('error.error', errornum=int(session['terminalerror'])))

    # Case 4: previous complete.
    elif 'complete' in session:

        # Redirect participant to complete page.
        return redirect(url_for('complete.complete'))

    # Case 5 repeat visit, manually changed workerId.
    elif 'workerId' in session and session['workerId'] != info['workerId']:
        # Update metadata.
        session['terminalerror'] = 1005
        session['ERROR'] = '1005: workerId tampering detected.'
        session['complete'] = 'error'
        write_metadata(session, ['ERROR', 'complete', 'terminalerror'], 'a')

        # Redirect participant to error (unusual activity).
        return redirect(url_for('error.error', errornum=1005))

    # Case 6: repeat visit, preexisting log but no session data.
    elif not 'workerId' in session:
        if h_workerId in os.listdir(CFG['meta']):

            ## Parse log file.
            with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
                logs = f.read()

            ## Extract subject ID.
            info['subId'] = re.search('subId\t(.*)\n', logs).group(1)

            # grab fields with potential boolean values from logs
            bool_fields = [
                'survey',
                'consent',
                'alert',
                'dlstart'
            ]

            for field in bool_fields:
                re_res = re.search(f'{field}\t(.*)\n', logs)
                if re_res and re_res.group(1) == 'True':
                    info[field] = True       # consent = true
                elif re_res and re_res.group(1) == 'False':
                    info[field] = False   # consent = false

            # Grab str fields from logs
            fields = [
                'seqId',
                'complete',
                'terminalerror',
                'ERROR',
                'surveycomplete',
            ]

            for field in fields:
                re_res = re.search(f'{field}\t(.*)\n', logs)
                if re_res:
                    info[field] = re_res.group(1)

            for k, v in info.items():
                session[k] = v

            write_metadata(session, [
                'workerId',
                'hitId',
                'assignmentId',
                'subId',
                'address',
                'user_agent'
            ], 'w')
            # Just a little recursion, once the session is updated, the routing rules will work.
            # This way we don't have to repeat the rules
            return routing(ep)

        # case 7: first visit, workerID present
        else:
            for k, v in info.items():
                session[k] = v
            write_metadata(session, [
                'workerId',
                'hitId',
                'assignmentId',
                'subId',
                'address',
                'user_agent'
            ], 'w')

            return redirect(url_for('consent.consent', **request.args))

    # case 8: Not consented
    elif 'consent' not in session:
        print('8')
        if ep == 'consent':
            return
        else:
            return redirect(url_for('consent.consent', **request.args))


    # case 9: Not viewed alert
    elif ('alert' not in session) or not session['alert']:
        print('9')
        if ep == 'alert':
            return
        else:
            return redirect(url_for('alert.alert', **request.args))


    # case 10: Survey not complete and restarts not allwoed
    elif not CFG['allow_restart'] and 'survey' in session:

        ## Update participant metadata.
        session['terminalerror'] = 1004
        session['ERROR'] = "1004: Revisited survey."
        session['complete'] = 'error'
        write_metadata(session, ['terminalerror', 'ERROR', 'complete'], 'a')

        ## Redirect participant to error (previous participation).
        return redirect(url_for('error.error', errornum=1004))

    # case 11: Survey not complete
    elif 'surveycomplete' not in session:
        if ep == 'survey':
            return
        else:
            return redirect(url_for('survey.survey', **request.args))


    # case 12: download not started
    elif 'dlstart' not in session:
        if ep == 'taskstart':
            return
        else:
            return redirect(url_for('taskstart.taskstart'))

    # case 13: not complete
    elif 'complete' not in session:
        if ep == 'task':
            return 'task'
        else:
            return redirect(url_for('task.task', **request.args))

    else:
        return redirect(url_for('error.error', **request.args))
