from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_metadata
from .routing import routing

## Initialize blueprint.
bp = Blueprint('alert', __name__)

@bp.route('/alert')
def alert():
    """Present alert to participant."""

    rres = routing('alert')
    if rres is not None:
        return rres
    else:
        ## Update participant metadata.
        session['alert'] = True
        write_metadata(session, ['alert'], 'a')

        ## Present alert page.
        return render_template('alert.html')

@bp.route('/alert', methods=['POST'])
def alert_post():
    """Process participant repsonse to alert page."""

    ## Redirect participant to experiment.
    return redirect(url_for('survey.survey', **request.args))
