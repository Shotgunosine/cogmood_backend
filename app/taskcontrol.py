import sys
import os
import re
import json
from hashlib import blake2b
from flask import (Blueprint, request, current_app)
from .config import CFG
from .io import initialize_taskdata, write_taskdata, hash_file, validate_checksum
from itsdangerous.exc import BadSignature
from werkzeug.utils import secure_filename


## Initialize blueprint.
bp = Blueprint('taskcontrol', __name__)

@bp.route('/taskcontrol', methods=['POST'])
def control_post():
    data = {}
    # validate seqId
    try:
        h_workerId = current_app.config['SUPREME_serializer'].loads(request.form['workerId'])
    except KeyError:
        data['error'] = 'No workerId'
        return data, 400
    except BadSignature:
        data['error'] = 'Invalid workerId'
        return data, 400

    # get correspondig subId
    with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
        logs = f.read()

    subId = re.search('subId\t(.*)\n', logs).group(1)

    # load subject's task_db json
    try:
        with open(os.path.join(CFG['t_db'], subId), 'r') as f:
            s_tdb = json.loads(f.read())
    except FileNotFoundError:
        data['error'] = 'Subjects task data not initialized'
        return data, 400

    # check which blocks have been completed/uploaded
    blocks_to_upload = []
    blocks_to_run = []
    for block in s_tdb:
        if block['uploaded']:
            continue
        try:
            c_block_checksum = request.form[block['name']]
            if not validate_checksum(c_block_checksum):
                data['error'] = f"Checksum for {block['name']} is not 64 character alpha numeric."
                return data, 400
        except KeyError:
            blocks_to_run.append(block['name'])
            continue
        # First time the server has seen the block
        if block['checksum'] is None:
            blocks_to_upload.append(block['name'])

    if len(blocks_to_upload) > 0:
        data['blocks_to_upload'] = blocks_to_upload

    if len(blocks_to_run) > 0:
        data['blocks_to_run'] = blocks_to_run

    return data, 200


@bp.route('/taskupload', methods=['POST'])
def taskupload():
    data = {}

    try:
        h_workerId = current_app.config['SUPREME_serializer'].loads(request.form['workerId'])
    except KeyError:
        data['error'] = 'No workerId'
        return data, 400
    except BadSignature:
        data['error'] = 'Invalid workerId'
        return data, 400

    # get correspondig subId
    with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
        logs = f.read()

    subId = re.search('subId\t(.*)\n', logs).group(1)

    # load subject's task_db json
    try:
        with open(os.path.join(CFG['t_db'], subId), 'r') as f:
            s_tdb = json.loads(f.read())
            blocks_needed = [bb['name'] for bb in s_tdb if not bb['uploaded']]
    except FileNotFoundError:
        data['error'] = 'Subjects task data not initialized'
        return data, 400

    # confirm that block needs to be uploaded
    try:
        r_block = request.form['block']
    except KeyError:
        data['error'] = 'No block name'
        return data, 400
    if request.form['block'] not in blocks_needed:
        data['error'] = 'Block already uploaded'
        return data, 400

    # get request checksum
    try:
        r_checksum = request.form['checksum']
        if not validate_checksum(r_checksum):
            data['error'] = f"Checksum is not 64 character alpha numeric."
            return data, 400
    except KeyError:
        data['error'] = "No checksum in request"
        return data, 400

    # check if the post request has the file part
    if 'file' not in request.files:
        data['error'] = 'No file part'
        return data, 400
    file = request.files['file']

    # save file
    sub_ul_dir = os.path.join(CFG['t_upload'], subId)
    if not os.path.isdir(sub_ul_dir): os.makedirs(sub_ul_dir)

    block_filename = os.path.join(sub_ul_dir, secure_filename(r_block))
    file.save(block_filename)

    # confirm checksum
    checksum = hash_file(block_filename)
    if r_checksum != checksum:
        sub_bul_dir = os.path.join(CFG['t_badupload'], subId)
        if not os.path.isdir(sub_bul_dir): os.makedirs(sub_bul_dir)
        bad_block_filename = os.path.join(sub_bul_dir, secure_filename(r_block))
        os.rename(block_filename, bad_block_filename)
        data['error'] = "Checksums didn't match"
        return data, 400
    else:
        for block in s_tdb:
            if block['name'] == r_block:
                block['uploaded'] = True
                block['checksum'] = checksum
                break

        write_taskdata(subId)

    return data, 200
