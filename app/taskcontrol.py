import sys
from flask import (Blueprint, request)
from .config import CFG
from .database import db, Participant

## Initialize blueprint.
bp = Blueprint('taskcontrol', __name__)

@bp.route('/taskcontrol', methods=['POST'])
def control_post():
    data = {}
    ## validate seqId
    try:
        seqId = int(request.form['seqId'])
    except KeyError:
        data['error'] = 'No seqId'
        return data, 400
    except ValueError:
        data['error'] = 'Invalid seqId'
        return data, 400

    ## call the database to lookup the workerId
    record = db.session.execute(db.select(Participant).filter_by(seqid=seqId)).scalars().all()

    ## read the subject, load the
    try:
        workerId = record[0].workerid
    except IndexError:
        data['error'] = 'seqId not found'
        return data, 400

