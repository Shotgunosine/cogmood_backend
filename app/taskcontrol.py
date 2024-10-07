import sys
import os
import re
from hashlib import blake2b
from flask import (Blueprint, request, current_app)
from .config import CFG
from itsdangerous.exc import BadSignature


## Initialize blueprint.
bp = Blueprint('taskcontrol', __name__)

@bp.route('/taskcontrol', methods=['POST'])
def control_post():
    data = {}
    # validate seqId
    try:
        subId =  current_app.config['SUPREME_serializer'].loads(request.form['subId'])
    except KeyError:
        data['error'] = 'No subId'
        return data, 400
    except BadSignature:
        data['error'] = 'Invalid subId'
        return data, 400


    # with open(os.path.join(CFG['meta'], subId), 'r') as f:
    #     logs = f.read()
    #
    # subId = re.search('subId\t(.*)\n', logs).group(1)

    # validate the token

    # check which blocks have been completed/uploaded
    # check blocks in request
    # save data
    # update metadata with completed and uploaded blocks
    #
