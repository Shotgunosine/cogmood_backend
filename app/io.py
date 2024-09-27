import os
from datetime import datetime
from hashlib import blake2b
from .config import CFG

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
    h_workerId = blake2b(session['workerId'].encode(), digest_size=20).hexdigest()

    ## Write metadata to disk.
    fout = os.path.join(CFG['meta'], h_workerId)
    with open(fout, mode) as f:
        for k in keys:
            f.write(f'{timestamp}\t{k}\t{session[k]}\n')

def write_surveydata(session, json, method='pass'):
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
        fout = os.path.join(CFG['survey'], '%s.json' %session['subId'])
    elif method == 'reject':
        fout = os.path.join(CFG['reject'], '%s.json' %session['subId'])
    elif method == 'incomplete':
        fout = os.path.join(CFG['incomplete'], '%s.json' %session['subId'])

    with open(fout, 'w') as f: f.write(json)
