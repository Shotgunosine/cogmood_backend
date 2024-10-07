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
from .io import write_metadata
from .config import CFG
from .routing import routing
from .utils import make_download
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
    make_download(supreme_subid, win_dlpath, 'windows')
    make_download(supreme_subid, mac_dlpath, 'mac')
    session['dlready'] = True
    write_metadata(session, ['dlready'], 'a')
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
