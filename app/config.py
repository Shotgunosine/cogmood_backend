import os
import configparser
import json
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
incomplete_dir = os.path.join(ROOT_DIR, cfg['IO']['INCOMPLETE'])
if not os.path.isdir(incomplete_dir): os.makedirs(incomplete_dir)
reject_dir = os.path.join(ROOT_DIR, cfg['IO']['REJECT'])
if not os.path.isdir(reject_dir): os.makedirs(reject_dir)
task_dir = os.path.join(data_dir, 'task')
if not os.path.isdir(task_dir): os.makedirs(task_dir)
survey_dir = os.path.join(data_dir, 'survey')
if not os.path.isdir(survey_dir): os.makedirs(survey_dir)

CFG = dict(
    debug=cfg['FLASK'].getboolean('DEBUG'),
    allow_restart=cfg['FLASK'].getboolean('ALLOW_RESTART'),
    code_success=cfg['PROLIFIC'].get('CODE_SUCCESS', gen_code(8).upper()),
    code_reject=cfg['PROLIFIC'].get('CODE_REJECT', gen_code(8).upper()),
    data=data_dir,
    meta=meta_dir,
    incomplete=incomplete_dir,
    reject=reject_dir,
    task=task_dir,
    survey=survey_dir,
    disallowed_agents=json.loads(cfg['FLASK']['DISALLOWED_AGENTS'])
)