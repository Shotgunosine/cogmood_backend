import os
import json
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
    send_file
)
from .io import write_metadata, initialize_taskdata
from .config import CFG
from .routing import routing
from .utils import edit_exe_worker_id, edit_app_worker_id
from hashlib import blake2b


## Initialize blueprint.
bp = Blueprint('taskstart', __name__)


@bp.route('/taskstart')
def taskstart():
    """Present download to participant."""

    rres = routing('taskstart')
    if rres is None:
        h_workerId = blake2b(session['workerId'].encode(), digest_size=24).hexdigest()
        supreme_subid = current_app.config['SUPREME_serializer'].dumps(h_workerId)
        subject_task_code = None
        if CFG['custom_exes']:
            if 'dlready' not in session or not session['dlready']:
                win_dlpath = os.path.join(CFG['download'], 'win_' + str(session['subId']) + '.exe')
                mac_dlpath = os.path.join(CFG['download'], 'mac_' + str(session['subId']) + '.dmg')
                edit_exe_worker_id(exe_file_path=CFG['base_exe'], new_worker_id=supreme_subid, output_file_path=win_dlpath)
                edit_app_worker_id(app_path=CFG['base_app'], new_worker_id=supreme_subid, output_dmg_path=mac_dlpath)
        else:
            subject_task_code = blake2b(session['workerId'].encode(), digest_size=4, salt=CFG['salt'].encode()).hexdigest()[:4]
        session['dlready'] = True
        write_metadata(session, ['dlready'], 'a')
        initialize_taskdata(session)
        mac_link = url_for('taskstart.download_mac', **request.args)
        win_link = url_for('taskstart.download_win', **request.args)
        if session['complete_button'] and not session['dlstarted']:
            button_before_dl = True
        else:
            button_before_dl = False
        if session['complete_button'] and session['taskinprogess']:
            taskinprogress = True
            with open(os.path.join(CFG['t_db'], f"{session['subId']}.json"), 'r') as f:
                s_tdb = json.loads(f.read())
                n_blocks_needed = len([bb['name'] for bb in s_tdb if not bb['uploaded']])
        else:
            n_blocks_needed = None
        return render_template('taskstart.html',
                               platform=session['platform'],
                               mac_link=mac_link,
                               win_link=win_link,
                               subject_task_code=subject_task_code,
                               button_before_dl=button_before_dl,
                               n_blocks_needed=n_blocks_needed)
    else:
        return rres

@bp.route('/download/mac')
def download_mac():
    if CFG['custom_exes']:
        dlpath = os.path.join(CFG['download'], 'mac_' + str(session['subId']) + '.dmg')
    else:
        dlpath = CFG['base_dmg']

    session['dlstarted'] = True
    write_metadata(session, ['dlstarted'], 'a')
    if os.path.exists(dlpath) and session['dlready']:
        return send_file(
            dlpath,
            as_attachment=True,
            download_name='SUPREME.dmg',
            mimetype="application/octet-stream"
        )
    else:
        return redirect(url_for('taskstart.taskstart', **request.args))

@bp.route('/download/win')
def download_win():
    if CFG['custom_exes']:
        dlpath = os.path.join(CFG['download'], 'win_' + str(session['subId']) + '.exe')
    else:
        dlpath = CFG['base_exe']

    session['dlstarted'] = True
    write_metadata(session, ['dlstarted'], 'a')
    if os.path.exists(dlpath) and session['dlready']:
        return send_file(
            dlpath,
            as_attachment=True,
            download_name='CogMood_task.exe',
            mimetype="application/vnd.microsoft.portable-executable"
        )
    else:
        return redirect(url_for('taskstart.taskstart', **request.args))


@bp.route('/taskstart', methods=['POST'])
def taskstart_post():
    session['complete_button'] = True
    write_metadata(session, ['complete_button'], 'a')
    return redirect(url_for('taskstart.taskstart', **request.args))
