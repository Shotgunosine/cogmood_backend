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
task_db_dir = os.path.join(task_dir, 'db')
if not os.path.isdir(task_db_dir): os.makedirs(task_db_dir)
task_upload_dir = os.path.join(task_dir, 'upload')
if not os.path.isdir(task_upload_dir): os.makedirs(task_upload_dir)
task_badupload_dir = os.path.join(task_dir, 'bad_upload')
if not os.path.isdir(task_badupload_dir): os.makedirs(task_badupload_dir)
dl_dir = os.path.join(data_dir, 'download')
if not os.path.isdir(dl_dir): os.makedirs(dl_dir)
base_exe_dir = os.path.join(data_dir, 'base_executables')
if not os.path.isdir(base_exe_dir): os.makedirs(base_exe_dir)
survey_dir = os.path.join(data_dir, 'survey')
if not os.path.isdir(survey_dir): os.makedirs(survey_dir)
survey_incomplete_dir = os.path.join(survey_dir, 'incomplete')
if not os.path.isdir(survey_incomplete_dir): os.makedirs(survey_incomplete_dir)
survey_ongoing_dir = os.path.join(survey_dir, 'ongoing')
if not os.path.isdir(survey_ongoing_dir): os.makedirs(survey_ongoing_dir)
survey_reject_dir = os.path.join(survey_dir, 'reject')
if not os.path.isdir(survey_reject_dir): os.makedirs(survey_reject_dir)
survey_complete_dir = os.path.join(survey_dir, 'complete')
if not os.path.isdir(survey_complete_dir): os.makedirs(survey_complete_dir)

CFG = dict(
    debug=cfg['FLASK'].getboolean('DEBUG'),
    route_debug=cfg['FLASK'].getboolean('ROUTE_DEBUG'),
    allow_restart=cfg['FLASK'].getboolean('ALLOW_RESTART'),
    code_success=cfg['PROLIFIC']['CODE_SUCCESS'],
    code_reject=cfg['PROLIFIC']['CODE_REJECT'],
    code_attn3=cfg['PROLIFIC']['CODE_ATTN3'],
    code_attn4=cfg['PROLIFIC']['CODE_ATTN4'],
    code_attn5=cfg['PROLIFIC']['CODE_ATTN5'],
    code_inval=cfg['PROLIFIC']['CODE_INVAL'],
    data=data_dir,
    meta=meta_dir,
    incomplete=incomplete_dir,
    reject=reject_dir,
    task=task_dir,
    t_db=task_db_dir,
    t_upload=task_upload_dir,
    t_badupload=task_badupload_dir,
    survey=survey_dir,
    s_incomplete=survey_incomplete_dir,
    s_ongoing=survey_ongoing_dir,
    s_reject=survey_reject_dir,
    s_complete=survey_complete_dir,
    download=dl_dir,
    base_exe=os.path.join(base_exe_dir, 'SUPREME.exe'),
    base_app=os.path.join(base_exe_dir, 'SUPREME.app'),
    disallowed_agents=json.loads(cfg['FLASK']['DISALLOWED_AGENTS']),
    allowed_agents=json.loads(cfg['FLASK']['ALLOWED_AGENTS']),
    blocks=json.loads(cfg['SUPREME']['BLOCKS']),
    nreps=json.loads(cfg['SUPREME']['NREPS'])
)