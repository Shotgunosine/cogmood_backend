from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_metadata
from .database import db, Participant
from .routing import routing

## Initialize blueprint.
bp = Blueprint('taskstart', __name__)


@bp.route('/taskstart')
def taskstart():
    """Present download to participant."""

    rres = routing('taskstart')
    if rres is None:
        return render_template('taskstart.html')
    else:
        return rres