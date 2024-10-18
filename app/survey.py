from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_surveydata, write_metadata, get_surveydata
from .config import CFG
from .routing import routing

## Initialize blueprint.
bp = Blueprint('survey', __name__)

@bp.route('/survey')
def survey():
    """Present survey to participant."""

    rres = routing('survey')

    if rres is not None:
        return rres
    else:
        ## Case 6: repeat visit allowed
        if CFG['allow_restart'] and 'survey' in session:

            try:
                prev_data = get_surveydata(session)
            except FileNotFoundError:
                # case 6, they started the survey, but haven't entered anything yet
                prev_data = None

        ## Case 7: first visit.
        else:
            prev_data = None
            ## Update participant metadata.
            session['survey'] = True
            write_metadata(session, ['survey'], 'a')

        ## Present survey.
        return render_template(
            'survey.html',
            workerId=session['workerId'],
            assignmentId=session['assignmentId'],
            hitId=session['hitId'],
            code_success=CFG['code_success'],
            code_attn3=CFG['code_attn3'],
            code_attn4=CFG['code_attn4'],
            code_attn5=CFG['code_attn5'],
            code_reject=CFG['code_reject'],
            prev_data=prev_data
        )

@bp.route('/surveynodl', methods=['POST'])
def survey_nodl():
    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_surveydata(session, JSON, method='reject')

    ## Flag partial data saving.
    session['MESSAGE'] = 'incomplete dataset saved'
    session['terminalerror'] = 1008
    session['ERROR'] = '1008: not willing to download and run task.'
    session['complete'] = 'error'
    write_metadata(session, ['MESSAGE', 'terminalerror', 'ERROR', 'complete'], 'a')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)

@bp.route('/survey', methods=['POST'])
def pass_message():
    """Write jsPsych message to metadata."""

    if request.is_json:

        ## Retrieve jsPsych data.
        msg = request.get_json()

        ## Update participant metadata.
        session['MESSAGE'] = msg
        write_metadata(session, ['MESSAGE'], 'a')
    # TODO: implement intermediate rejection for failing check questions
    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)

@bp.route('/ongoing_save', methods=['POST'])
def ongoing_save():
    """Save incomplete jsPsych dataset to disk."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()
        ## Save jsPsch data to disk.
        write_surveydata(session, JSON, method='ongoing')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)
@bp.route('/incomplete_save', methods=['POST'])
def incomplete_save():
    """Save incomplete jsPsych dataset to disk."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_surveydata(session, JSON, method='incomplete')

    ## Flag partial data saving.
    session['MESSAGE'] = 'incomplete dataset saved'
    write_metadata(session, ['MESSAGE'], 'a')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)

@bp.route('/redirect_success', methods = ['POST'])
def redirect_success():
    """Save complete jsPsych dataset to disk."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_surveydata(session, JSON, method='pass')

    ## Flag experiment as complete.
    session['surveycomplete'] = 'success'
    write_metadata(session, ['surveycomplete'], 'a')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## The corresponding jsPsych function handles the redirect.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)

@bp.route('/redirect_reject', methods = ['POST'])
def redirect_reject():
    """Save rejected jsPsych dataset to disk."""
    # TODO: add paramters here so we can record the rejection reason
    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_surveydata(session, JSON, method='reject')

    ## Flag experiment as complete.
    session['complete'] = 'reject'
    write_metadata(session, ['complete'], 'a')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## The corresponding jsPsych function handles the redirect.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)

@bp.route('/redirect_error', methods = ['POST'])
def redirect_error():
    """Save rejected jsPsych dataset to disk."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_surveydata(session, JSON, method='reject')

    ## Flag experiment as complete.
    session['complete'] = 'error'
    write_metadata(session, ['complete'], 'a')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## The corresponding jsPsych function handles the redirect.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)
