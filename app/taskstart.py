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
from .database import db, Participant
from .config import CFG
from .routing import routing
from .utils import make_download

## Initialize blueprint.
bp = Blueprint('taskstart', __name__)


@bp.route('/taskstart')
def taskstart():
    """Present download to participant."""

    rres = routing('taskstart')

    supreme_seqid = current_app.config['SUPREME_serializer'].dumps(session['seqId'])
    win_dlpath = os.path.join(CFG['download'], 'win_' + session['seqId'])
    mac_dlpath = os.path.join(CFG['download'], 'mac_' + session['seqId'])
    make_download(supreme_seqid, win_dlpath, 'windows')
    make_download(supreme_seqid, mac_dlpath, 'mac')
    session['dlready'] = True
    write_metadata(session, ['dlready'], 'a')
    if session['platform'] == 'mac':
        platform_link = url_for(taskstart.download_mac)
        other_platform = 'win'
        other_link = url_for(taskstart.download_win)
    else:
        platform_link = url_for(taskstart.download_win)
        other_platform = 'mac'
        other_link = url_for(taskstart.download_mac)
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
    dlpath = os.path.join(CFG['download'], 'mac_' + session['seqId'])

    session['dlstarted'] = True
    write_metadata(session, ['dlstarted'], 'a')
    if os.path.exists(dlpath) and session['dlready']:
        # TODO: figure out mimetype and file extension
        return send_file(
            dlpath,
            as_attachment=True,
            download_name='CogMood_task'
        )
    else:
        return redirect(url_for('task.task', **request.args))

@bp.route('/download/win')
def download_win():
    dlpath = os.path.join(CFG['download'], 'win_' + session['seqId'])

    session['dlstarted'] = True
    write_metadata(session, ['dlstarted'], 'a')
    if os.path.exists(dlpath) and session['dlready']:
        # TODO: figure out mimetype and file extension
        return send_file(
            dlpath,
            as_attachment=True,
            download_name='CogMood_task'
        )
    else:
        return redirect(url_for('task.task', **request.args))
