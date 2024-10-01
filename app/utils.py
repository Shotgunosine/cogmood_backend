import random
import string

def gen_code(N):
    """Generate random completion code."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))



def make_download(sid, dlpath, platform):
    pass