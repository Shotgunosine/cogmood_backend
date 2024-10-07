from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_metadata
from .routing import routing
from hashlib import blake2b

## Initialize blueprint.
bp = Blueprint('consent', __name__)

@bp.route('/consent')
def consent():
    """Present consent form to participant."""

    rres = routing('consent')

    if rres is None:
        return render_template('consent.html')
    else:
        return rres

@bp.route('/consent', methods=['POST'])
def consent_post():
    """Process participant repsonse to consent form."""

    ## Retrieve participant response.
    subj_consent = int(request.form['subj_consent'])
    bot_check = request.form.get('future_contact', False)

    ## Check for suspicious responding.
    if bot_check:

        ## Update participant metadata.
        session['consent'] = False
        session['complete'] = 'error'
        session['terminalerror'] = 1005
        session['ERROR'] = '1005: failed bot check on consent.'
        write_metadata(session, ['consent','complete', 'terminalerror', 'ERROR'], 'a')

        ## Redirect participant to error (unusual activity).
        return redirect(url_for('error.error', errornum=1005))

    ## Check participant response.
    elif subj_consent:

        ## Update participant metadata.
        session['consent'] = True
        write_metadata(session, ['consent'], 'a')

        ## TODO: validate subid and workerId
        ## TODO: deal with psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "participant_subid_key"
        ## DETAIL:  Key (subid)=(ae1c2x4nmzi7e2q87nomvrer) already exists.

        h_workerId = blake2b(session['workerId'].encode(), digest_size=20).hexdigest()

        ## Redirect participant to alert page.
        return redirect(url_for('alert.alert', **request.args))

    else:

        ## Update participant metadata.
        session['consent'] = False
        session['complete'] = 'error'
        session['terminalerror'] = 1002
        session['ERROR'] = '1002: did not consent.'
        write_metadata(session, ['consent', 'complete', 'terminalerror', 'ERROR'], 'a')

        ## Redirect participant to error (decline consent).
        return redirect(url_for('error.error', errornum=1002))
