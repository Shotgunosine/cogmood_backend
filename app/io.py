import os
import json
from datetime import datetime
from hashlib import blake2b
from .config import CFG
from .utils import pseudorandomize


def write_metadata(session, keys, mode='w'):
    """Write metadata to disk.

    Parameters
    ----------
    session : flask session
        Current user session.
    keys : list
        Session keys to write to file.
    mode : r | w | a
        Open file mode.
    """

    ## Define timestamp.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # hash workerid
    h_workerId = blake2b(session['workerId'].encode(), digest_size=24).hexdigest()

    ## Write metadata to disk.
    fout = os.path.join(CFG['meta'], h_workerId)
    with open(fout, mode) as f:
        for k in keys:
            f.write(f'{timestamp}\t{k}\t{session[k]}\n')


def validate_checksum(checksum, expected_length=128):
    if len(checksum) != expected_length:
        return False
    if not checksum.isalnum():
        return False
    return True


def initialize_taskdata(session):
    """Initialize subject entry in task db.

    Parameters
    ----------
    session : flask session
        Current user session.
    """

    ## Write metadata to disk.
    fout = os.path.join(CFG['t_db'], f"{session['subId']}.json")

    blocks = pseudorandomize(CFG['blocks'], CFG['nreps'])
    blocks_json = []
    added_blocks = {bb: 0 for bb in blocks}
    for block in blocks:
        bdict = dict(
            name=f"{block}_{added_blocks[block]}",
            checksum=None,
            uploaded=False
        )
        blocks_json.append(bdict)
        added_blocks[block] += 1
    with open(fout, 'w') as f:
        f.write(json.dumps(blocks_json, indent=2))

def write_taskdata(subId, blocks):
    """Initialize subject entry in task db.

    Parameters
    ----------
    session : flask session
        Current user session.
    """

    ## Write metadata to disk.
    fout = os.path.join(CFG['t_db'], f"{subId}.json")

    with open(fout, 'w') as f:
        f.write(json.dumps(blocks, indent=2))

def hash_file(filename):
    hash_blake = blake2b()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_blake.update(chunk)
    return hash_blake.hexdigest()

def write_surveydata(session, jsondat, method='pass'):
    """Write jsPsych output to disk.

    Parameters
    ----------
    session : flask session
        Current user session.
    json : object
        Data object returned by jsPsych.
    method : pass | reject
        Designates target folder for data.
    """

    ## Write data to disk.
    if method == 'pass':
        fout = os.path.join(CFG['s_complete'], '%s.json' %session['subId'])
    elif method == 'reject':
        fout = os.path.join(CFG['s_reject'], '%s.json' %session['subId'])
    elif method == 'incomplete':
        fout = os.path.join(CFG['s_incomplete'], '%s.json' %session['subId'])
    elif method == 'ongoing':
        fout = os.path.join(CFG['s_ongoing'], '%s.json' %session['subId'])
    try:
        with open(fout, 'w') as f:
            f.write(jsondat)
    except TypeError:
        with open(fout, 'w') as f:
            f.write(json.dumps(jsondat, indent=2))

def get_surveydata(session, method='ongoing'):
    """Write jsPsych output to disk.

    Parameters
    ----------
    session : flask session
        Current user session.
    method : ongoing
        Designates target folder for data.
    """

    ## Write data to disk.
    if method == 'ongoing':
        fin = os.path.join(CFG['s_ongoing'], '%s.json' %session['subId'])
    else:
        raise NotImplementedError("Getting survey data from anywhere but ongoing is not supported")
    with open(fin, 'r') as f:
        data = f.read()
    return data
