from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_surveydata, write_metadata
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
        ## TODO: implement this
        ## https://surveyjs.io/form-library/examples/healthcare/patient-medical-history-form-template/vanillajs#content-code
        ## https://www.google.com/search?q=flask+render+json+in+template&oq=flask+render+json+in&gs_lcrp=EgZjaHJvbWUqCAgBEAAYFhgeMgYIABBFGDkyCAgBEAAYFhgeMggIAhAAGBYYHjIICAMQABgWGB4yCAgEEAAYFhgeMggIBRAAGBYYHjIKCAYQABiABBiiBDIKCAcQABiABBiiBDIKCAgQABiABBiiBDIKCAkQABiABBiiBNIBCDc4MzFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
        if CFG['allow_restart'] and 'survey' in session:

            raise NotImplementedError

        ## Case 7: first visit.
        else:

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
                code_reject=CFG['code_reject']
            )

@bp.route('/survey', methods=['POST'])
def pass_message():
    """Write jsPsych message to metadata."""

    if request.is_json:

        ## Retrieve jsPsych data.
        msg = request.get_json()

        ## Update participant metadata.
        session['MESSAGE'] = msg
        write_metadata(session, ['MESSAGE'], 'a')

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
    # if they save incomplete survey data, we're going to make them view tha alert again
    session['alert'] = False
    write_metadata(session, ['MESSAGE', 'alert'], 'a')

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
