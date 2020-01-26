import os, sys, configparser, warnings
from flask import (Flask, redirect, render_template, request, session, url_for)
from app import consent, experiment, complete, error
from .io import write_metadata
from .utils import gen_code

## Define root directory.
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

## Load and parse configuration file.
cfg = configparser.ConfigParser()
cfg.read(os.path.join(ROOT_DIR, 'app.ini'))

## Ensure output directories exist.
data_dir = os.path.join(ROOT_DIR, cfg['IO']['DATA'])
if not os.path.isdir(data_dir): os.makedirs(data_dir)
meta_dir = os.path.join(ROOT_DIR, cfg['IO']['METADATA'])
if not os.path.isdir(meta_dir): os.makedirs(meta_dir)

## Check Flask password.
if cfg['FLASK']['SECRET_KEY'] == "PLEASE_CHANGE_THIS":
    msg = "WARNING: Flask password is currently default. This should be changed prior to production."
    warnings.warn(msg)

## Initialize Flask application.
app = Flask(__name__)
app.secret_key = cfg['FLASK']['SECRET_KEY']

## Apply blueprints to the application.
app.register_blueprint(consent.bp)
app.register_blueprint(experiment.bp)
app.register_blueprint(complete.bp)
app.register_blueprint(error.bp)

## Define root node.
@app.route('/')
def index():

    ## Error-catching: screen for previous visits.
    if 'workerId' in session:

        ## Update metadata.
        session['ERROR'] = "1004: Revisited index."
        write_metadata(session, ['ERROR'], 'a')

        ## Redirect participant to error (previous participation).
        return redirect(url_for('error.error', errornum=1004))

    ## Store directories in session object.
    session['data'] = data_dir
    session['metadata'] = meta_dir

    ## Store Turker info.
    session['workerId']     = request.args.get('workerId')        # MTurk metadata
    session['assignmentId'] = request.args.get('assignmentId')    # MTurk metadata
    session['hitId']        = request.args.get('hitId')           # MTurk metadata
    session['a']            = request.args.get('a')               # TurkPrime metadata
    session['tp_a']         = request.args.get('tp_a')            # TurkPrime metadata
    session['b']            = request.args.get('b')               # TurkPrime metadata
    session['tp_b']         = request.args.get('tp_b')            # TurkPrime metadata
    session['c']            = request.args.get('c')               # TurkPrime metadata
    session['tp_c']         = request.args.get('tp_c')            # TurkPrime metadata

    ## Error-catching: screen for valid workerId.
    if session['workerId'] is None:

        ## Redirect participant to error (admin error).
        return redirect(url_for('error.error', errornum=1000))

    elif session['workerId'] in os.listdir(session['metadata']):

        ## Update metadata.
        session['ERROR'] = "1004: Revisited index."
        write_metadata(session, ['ERROR'], 'a')

        ## Redirect participant to error (previous participation).
        return redirect(url_for('error.error', errornum=1004))

    else:

        ## Update metadata.
        session['subId'] = gen_code(12)
        write_metadata(session, ['workerId','hitId','assignmentId','subId'], 'w')

        ## Redirect participant to consent form.
        return redirect(url_for('consent.consent'))

## DEV NOTE:
## The following route is strictly for development purposes and should be
## commented out before deployment.
# @app.route('/clear')
# def clear():
#     session.clear()
#     return 'Complete!'
