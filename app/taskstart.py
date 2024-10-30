import os
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
    h_workerId = blake2b(session['workerId'].encode(), digest_size=24).hexdigest()
    supreme_subid = current_app.config['SUPREME_serializer'].dumps(h_workerId)
    win_dlpath = os.path.join(CFG['download'], 'win_' + str(session['subId']) + '.exe')
    mac_dlpath = os.path.join(CFG['download'], 'mac_' + str(session['subId']) + '.app')
    # make_download(supreme_subid, win_dlpath, 'windows')
    edit_exe_worker_id(exe_file_path=BASE_EXE_PATH, new_worker_id=supreme_subid, output_file_path=win_dlpath)
    # make_download(supreme_subid, mac_dlpath, 'mac')
    edit_app_worker_id(app_path=BASE_APP_PATH, new_worker_id=supreme_subid, output_app_path=mac_dlpath)
    session['dlready'] = True
    write_metadata(session, ['dlready'], 'a')
    initialize_taskdata(session)

    if session['platform'] == 'mac':
        platform_link = url_for('taskstart.download_mac')
        other_platform = 'win'
        other_link = url_for('taskstart.download_win')
    else:
        platform_link = url_for('taskstart.download_win')
        other_platform = 'mac'
        other_link = url_for('taskstart.download_mac')
    if rres is None:
        return render_template('taskstart.html',
                               platform=session['platform'],
                               platform_link=platform_link,
                               other_platform=other_platform,
                               other_link=other_link)
    else:
        return rres

@bp.route('/download/mac')
def download_mac():
    dlpath = os.path.join(CFG['download'], 'mac_' + str(session['subId']) + '.app')

    session['dlstarted'] = True
    write_metadata(session, ['dlstarted'], 'a')
    if os.path.exists(dlpath) and session['dlready']:
        return send_file(
            dlpath,
            as_attachment=True,
            download_name='CogMood_task',
            mimetype="inode/directory"
        )
    else:
        return redirect(url_for('task.task', **request.args))

@bp.route('/download/win')
def download_win():
    dlpath = os.path.join(CFG['download'], 'win_' + str(session['subId']) + '.exe')

    session['dlstarted'] = True
    write_metadata(session, ['dlstarted'], 'a')
    if os.path.exists(dlpath) and session['dlready']:
        return send_file(
            dlpath,
            as_attachment=True,
            download_name='CogMood_task',
            mimetype="application/vnd.microsoft.portable-executable"
        )
    else:
        return redirect(url_for('task.task', **request.args))
