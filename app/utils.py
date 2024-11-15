import random
import string
import copy
import logging
import os
import plistlib
import shutil
from typing import Optional
from pathlib import Path
from pefile import PE, DIRECTORY_ENTRY


def gen_code(N):
    """Generate random completion code."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))


def pseudorandomize(inblocks, nreps, shuffle_blocks=True, nested_output=False):
    """
    pseudorandomize the input blocks so that each task occurs once before
    any task is repeated and no tasks occur back to back. Will trigger an
    infinite loop if the number of blocks it too small to generate enough unique
    orders to satisfy the shuffle blocks condition for the number of repetitions
    requested.

    Parameters
    ==========
    inblocks : list of strings or list of list of strings
        list of tasks to randomize
    nreps : int
        number of repetitions of each task
    shuffle blocks : bool
        Should task order be shuffled every time they're repeated
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


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def edit_app_worker_id(app_path: str, new_worker_id: str, output_app_path: str) -> None:
    """
    Modifies the 'WorkerID' field in the Info.plist of a macOS .app bundle.

    Args:
        app_path (str): Path to the original .app bundle whose 'WorkerID' will be modified.
        new_worker_id (str): New 'WorkerID' value to replace the existing one.
        output_app_path (Optional[str]): Path to save the modified .app bundle. If not provided, 
                                         the original bundle will be overwritten.

    Raises:
        FileNotFoundError: If the specified .app bundle or Info.plist file does not exist.
        ValueError: If the Info.plist file cannot be loaded or parsed.
    """

    # Construct the path to the Info.plist file inside the original .app bundle
    plist_path = Path(app_path) / 'Contents' / 'Info.plist'

    # Ensure the .app bundle and Info.plist exist
    if not plist_path.exists():
        raise FileNotFoundError(f"The file {plist_path} does not exist.")

    try:
        # If an output path is specified, copy the original .app bundle to the new location
        output_path = Path(output_app_path)
        if output_path.exists():
            raise FileExistsError(
                f"The output path {output_app_path} already exists.")
        shutil.copytree(app_path, output_app_path)
        # Update plist path to the new location
        plist_path = output_path / 'Contents' / 'Info.plist'


        # Load the plist file
        with plist_path.open('rb') as plist_file:
            plist_data = plistlib.load(plist_file)

        # Log current WorkerID, if present
        current_worker_id = plist_data.get('WorkerID', None)
        if current_worker_id:
            logging.info(f"Current WorkerID: {current_worker_id}")

        # Update the WorkerID
        plist_data['WorkerID'] = new_worker_id

        # Write the updated plist back
        with plist_path.open('wb') as plist_file:
            plistlib.dump(plist_data, plist_file)

        logging.info(f"Successfully updated WorkerID to {new_worker_id}")

    except Exception as e:
        raise ValueError(f"Failed to modify the plist file: {e}")


def edit_exe_worker_id(exe_file_path: str, new_worker_id: str, output_file_path: str) -> None:
    """
    Modifies the 'WorkerID' field in the version information of an executable.

    Args:
        exe_file_path (str): Path to the executable whose 'WorkerID' will be modified.
        new_worker_id (str): New 'WorkerID' value to replace the existing one. 
                              **Must** be less than or equal to the length of the current 'WorkerID' for a successful update.
        output_file_path (str): **Optional**. Path where the modified executable will be saved. 
                                If not provided, the original executable will be overwritten.

    Raises:
        FileNotFoundError: If the specified executable does not exist.
        ValueError: If the PE file cannot be loaded or parsed.
    """

    if not os.path.exists(exe_file_path):
        raise FileNotFoundError(f"The file {exe_file_path} does not exist.")

    output_file_path = Path(output_file_path)

    try:
        pe: PE = PE(exe_file_path, fast_load=True)
        pe.parse_data_directories(
            directories=[DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])
    except Exception as e:
        raise ValueError(f"Failed to load or parse the PE file: {e}")

    # Access the WorkerID and update it if found
    if hasattr(pe, 'FileInfo'):
        for file_info in pe.FileInfo:
            for info in file_info:
                if info.name == 'StringFileInfo':
                    version_info_dict: dict = info.StringTable[0].entries
                    worker_id_bytes: bytes = version_info_dict.get(
                        b'WorkerID', None)

                    if worker_id_bytes:
                        logging.info(
                            f"Found WorkerID: {worker_id_bytes.decode('utf-8')}")

                        # Calculate the original size in bytes and the new value size
                        original_size: int = len(worker_id_bytes)
                        new_worker_id_bytes: bytes = new_worker_id.encode(
                            'utf-8')
                        new_size: int = len(new_worker_id_bytes)

                        if new_size <= original_size:
                            # Create the new value padded with null bytes up to the original size
                            padded_new_worker_id: bytes = new_worker_id_bytes + \
                                b'\x00' * (original_size - new_size)

                            # Update the value with the padded version
                            version_info_dict[b"WorkerID"] = padded_new_worker_id

                            # Write the updated attribute to the output file
                            pe.write(output_file_path)
                            logging.info(
                                f"Successfully updated WorkerID to {new_worker_id}")
                        else:
                            logging.error(
                                f"Error: New value '{new_worker_id}' is larger than the existing space of {original_size} bytes.")
                        return

    logging.error(f"Error: WorkerID not found in {exe_file_path}")