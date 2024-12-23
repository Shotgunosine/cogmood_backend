import os
import re
import json
from flask import (Blueprint, request, current_app)
from .config import CFG
from .io import write_taskdata, hash_file, validate_checksum
from itsdangerous.exc import BadSignature
from werkzeug.utils import secure_filename
from datetime import datetime
from .validation import validate

## Initialize blueprint.
bp = Blueprint('taskcontrol', __name__)


@bp.route('/taskcontrol', methods=['GET','POST'])
def taskcontrol():
    data = {}
    # validate seqId
    try:
        h_workerId = current_app.config['SUPREME_serializer'].loads(request.args['worker_id'])
    except KeyError:
        data['error'] = 'No worker_id'
        return data, 400
    except BadSignature:
        data['error'] = 'Invalid worker_id'
        return data, 400

    # get corresponding subId
    with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
        logs = f.read()

    subId = re.search('subId\t(.*)\n', logs).group(1)

    # load subject's task_db json
    try:
        with open(os.path.join(CFG['t_db'], f"{subId}.json"), 'r') as f:
            s_tdb = json.loads(f.read())
            blocks_needed = [bb['name'] for bb in s_tdb if not bb['uploaded']]
    except FileNotFoundError:
        data['error'] = 'Subjects task data not initialized'
        return data, 400

    if request.method == 'GET':
        data['blocks_to_run'] = blocks_needed
        return data, 200
    else:
        # confirm that block needs to be uploaded
        try:
            r_block = request.form['block_name']
            r_task = r_block.split('_')[0]
        except KeyError:
            data['error'] = 'No block name'
            return data, 400
        if request.form['block_name'] not in blocks_needed:
            data['error'] = 'Block already uploaded'
            return data, 400

        # get request checksum
        try:
            r_checksum = request.form['checksum']
            if not validate_checksum(r_checksum):
                data['error'] = f"Checksum is not 128 character alphanumeric."
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

        block_filename = os.path.join(sub_ul_dir, secure_filename(r_block) + '.zip')
        file.save(block_filename)

        # confirm checksum
        checksum = hash_file(block_filename)
        all_uploaded = True
        all_valid = True
        valid = False
        if r_checksum != checksum:
            sub_bul_dir = os.path.join(CFG['t_badupload'], subId)
            if not os.path.isdir(sub_bul_dir): os.makedirs(sub_bul_dir)
            bad_block_filename = os.path.join(sub_bul_dir, secure_filename(r_block) + '.zip')
            os.rename(block_filename, bad_block_filename)
            data['error'] = "Checksums didn't match"
            return data, 409
        else:
            # validate uploaded data
            try:
                valid, reason = validate(block_filename, r_task)

            except (NameError, RecursionError):
                valid = False
                reason = 'format'

            for block in s_tdb:
                if block['name'] == r_block:
                    block['uploaded'] = True
                    block['checksum'] = checksum
                    block['valid'] = valid
                    block['reason'] = reason
                # faster than &= based on timeit
                if not block['uploaded']:
                    all_uploaded = False
                if not block['valid']:
                    all_valid = False

            write_taskdata(subId, s_tdb)

        if all_uploaded:
            # set metadata to complete
            # not using write_metadata because we don't have a session object
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not all_valid:
                complete_code = 'task_invalid'
            else:
                complete_code = 'success'
            # Write metadata to disk.
            fout = os.path.join(CFG['meta'], h_workerId)
            with open(fout, 'a') as f:
                f.write(f'{timestamp}\tcomplete\t{complete_code}\n')

        return data, 200