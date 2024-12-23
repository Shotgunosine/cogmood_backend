from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .routing import routing
from .io import write_metadata

## Initialize blueprint.
bp = Blueprint('task', __name__)


@bp.route('/task')
def task():
    """Present download to participant."""
    rres = routing('task')
    # TODO: Task routing and task template
    if rres is None:
        return render_template('task.html')
    else:
        return rres