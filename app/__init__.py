from pathlib import Path
import os, sys, re, configparser, warnings
from flask import (Flask, redirect, render_template, request, session, url_for)
from hashlib import blake2b
from app import consent, alert, survey, complete, error, taskstart, task, taskcontrol
from .config import CFG
from .io import write_metadata
from .utils import gen_code
from .routing import routing
from itsdangerous.serializer import Serializer


__version__ = '1.2.6'

## Define root directory.
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

## Load and parse configuration file.
cfg = configparser.ConfigParser()
cfg.read(os.path.join(ROOT_DIR, 'app.ini'))

if CFG['debug']:
    warnings.warn("WARNING: Flask currently in debug mode. This should be changed prior to production.")

## Check Flask password.
secret_key = cfg['FLASK']['SECRET_KEY']
if secret_key == "PLEASE_CHANGE_THIS":
    warnings.warn("WARNING: Flask password is currently default. This should be changed prior to production.")

supreme_secret_key = cfg['SUPREME']['SECRET_KEY']
if supreme_secret_key == "PLEASE_CHANGE_THIS":
    warnings.warn("WARNING: SUPREME password is currently default. This should be changed prior to production.")


## Get DB password and connection string
connection_string = os.getenv('CMBEDB_CONNECT')

## Check restart mode; if true, participants can restart experiment.

## Initialize Flask application.
app = Flask(__name__)
app.secret_key = secret_key
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SUPREME_serializer'] = Serializer(supreme_secret_key)
#app.config['APPLICATION_ROOT'] = '/cogmood'
# load existing subjects into database
# mds = sorted(Path(meta_dir).glob('*'))
# to_insert = [[] for md in mds]
# for md in mds:
#     to_insert[md['seqId']-1] = Participant(subid=md['SubId'])
# for pp in to_insert:
## Apply blueprints to the application.
app.register_blueprint(consent.bp)
app.register_blueprint(alert.bp)
app.register_blueprint(survey.bp)
app.register_blueprint(taskstart.bp)
app.register_blueprint(task.bp)
app.register_blueprint(taskcontrol.bp)
app.register_blueprint(complete.bp)
app.register_blueprint(error.bp)

## Define root node.
@app.route('/')
def index():

    ##Debug mode: clear session.
    if CFG['debug']:
        session.clear()

    return routing('/')
