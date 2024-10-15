import random
import string
import copy

def gen_code(N):
    """Generate random completion code."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))


def make_download(sid, dlpath, platform):
    pass


def pseudorandomize(inblocks, nreps, shuffle_blocks=True, nested_output=False):
    """
    pseudorandomize the input blocks so that each task occurs once before
    any task is repeated and no tasks occur back to back. Will trigger an
    infinite loop if the number of blocks it too small to generate enough unique
    orders to satisfy the shuffle blocks condition for the number of repititions
    requested.

    Parameters
    ==========
    inblocks : list of strings or list of list of strings
        list of tasks to randomize
    nreps : int
        number of repititions of each task
    shuffle blocks : bool
        Should task order be shuffeled everytime they're repeated
    nested_output : bool
        Should the output be nested (list of lists)

    """
    blocks = []
    these_tasks = copy.deepcopy(inblocks)
    if not isinstance(these_tasks[0], list):
        these_tasks = [these_tasks]
    random.shuffle(these_tasks)
    for i in range(nreps):
        tasks = copy.deepcopy(these_tasks)
        for task_block in tasks:
            if shuffle_blocks:
                random.shuffle(task_block)
                if len(blocks) > 0:
                    while ((blocks[-1][-1] == task_block[0]) or task_block in blocks):
                        random.shuffle(task_block)
            blocks.append(task_block)

    if nested_output:
        return blocks
    else:
        flat_blocks = []
        for task_block in blocks:
            for task in task_block:
                flat_blocks.append(task)
        return flat_blocks
