import sys
import os
import re
from hashlib import blake2b
from flask import (Blueprint, request)
from .config import CFG
from .database import db, Participant

## Initialize blueprint.
bp = Blueprint('taskcontrol', __name__)

@bp.route('/taskcontrol', methods=['POST'])
def control_post():
    data = {}
    # validate seqId
    try:
        seqId = int(request.form['seqId'])
    except KeyError:
        data['error'] = 'No seqId'
        return data, 400
    except ValueError:
        data['error'] = 'Invalid seqId'
        return data, 400

    # call the database to look up the workerId
    record = db.session.execute(db.select(Participant).filter_by(seqid=seqId)).scalars().all()

    # read the subject metadata to load the subId
    try:
        workerId = record[0].workerid
    except IndexError:
        data['error'] = 'seqId not found'
        return data, 400

    h_workerId = blake2b(workerId.encode(), digest_size=20).hexdigest()
    with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
        logs = f.read()

    subId = re.search('subId\t(.*)\n', logs).group(1)

    # validate the token

    # check which blocks have been completed/uploaded
    # check blocks in request
    # save data
    # update metadata with completed and uploaded blocks
    #
