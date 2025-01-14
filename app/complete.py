from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_metadata
from .config import CFG
from .utils import logging

## Initialize blueprint.
bp = Blueprint('complete', __name__)

@bp.route('/complete')
def complete():
    """Present completion screen to participant."""

    route_debug = CFG['route_debug']
    if route_debug:
        logging.info(f'Request to complete')
        logging.info('Session contents')
        for k, v in session.items():
            logging.info(f"{k}: {v}")

    # Case 1: Error-catching: screen for missing session.
    if not 'workerId' in session:

        ## Redirect participant to error (missing workerId).
        return redirect(url_for('error.error', errornum=1000))

    # Case 2: terminalerror set in session data
    elif 'terminalerror' in session:

        ## Redirect participant to error (missing workerId).
        return redirect(url_for('error.error', errornum=session['terminalerror']))

    # Case 3: visit complete page without previous completion.
    elif 'complete' not in session:

        ## Flag experiment as complete.
        session['terminalerror'] = 1007
        session['ERROR'] = "1007: Visited complete page before completion."
        session['complete'] = 'reject'
        write_metadata(session, ['ERROR','complete','code_reject'], 'a')

        ## Redirect participant with decoy code.
        url = "https://app.prolific.co/submissions/complete?cc=" + CFG['code_reject']
        return redirect(url)

    # Case 4: visit complete page with previous rejection.
    elif session['complete'] == 'reject':

        ## Redirect participant with decoy code.
        url = "https://app.prolific.co/submissions/complete?cc=" + CFG['code_reject']
        return redirect(url)

    # Case 5: visit complete page after task failed validation
    elif session['complete'] == 'task_invalid':

        ## Redirect participant with decoy code.
        url = "https://app.prolific.co/submissions/complete?cc=" + CFG['code_inval']
        return redirect(url)

    # Case 6: visit complete page with succesfull completion.
    elif session['complete'] == 'success':

        ## Redirect participant with completion code.
        url = "https://app.prolific.co/submissions/complete?cc=" + CFG['code_success']
        return redirect(url)

    # Case 7: catch all
    else:

        ## Redirect participant to error (unusual activity).
        return redirect(url_for('error.error'))
