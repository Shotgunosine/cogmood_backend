from hashlib import blake2b
import random
import os
from ..config import CFG

def get_new_workerid():
    newid = False
    while not newid:
        workerId = str(random.randint(1, 1000000))
        h_workerId = blake2b(workerId.encode(), digest_size=24).hexdigest()
        if h_workerId in os.listdir(CFG['meta']):
            continue
        else:
            newid = True
    return workerId
