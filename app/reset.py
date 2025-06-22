import os
from flask import (Blueprint, redirect, request, session, url_for)
from hashlib import blake2b
from .config import CFG

bp = Blueprint('reset', __name__)

@bp.route('/reset8292')
def reset():
    """reset session and redirect"""
    workerId = request.args.get('PROLIFIC_PID')
    try:
        h_workerId = blake2b(workerId.encode(), digest_size=24).hexdigest()
        os.remove(os.path.join(CFG['meta'], h_workerId))
    except (AttributeError, FileNotFoundError):
        pass

    session.clear()


    return redirect(url_for('consent.consent', **request.args))