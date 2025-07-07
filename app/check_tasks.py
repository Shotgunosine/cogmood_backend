from argparse import ArgumentParser
from pathlib import Path
from zipfile import ZipFile
import tempfile
from . import log
from .validation import validate
import pandas as pd

def print_task_performance(sub_id):
    for task_name in ['flkr', 'cab', 'rdm']:
        for runnum in [0, 1, 2]:
            if runnum == 2 and task_name != 'rdm':
                continue
            zipped_path = task_data_dir /sub_id/ f'{task_name}_{runnum}.zip'
            with tempfile.TemporaryDirectory() as tmpdir:
                slog_file = ZipFile(zipped_path).extract(f'log_{task_name}_0.slog', path=tmpdir)
                lod = log.log2dl(slog_file)
                loddf = pd.DataFrame(lod)
            print()
            print(f'task_name: {task_name}, run: {runnum}')
            if task_name == 'cab':
                print(loddf.groupby(['cond_strength', 'cond_trial']).resp_acc.mean())
                print(loddf.groupby(['cond_strength', 'cond_trial']).resp_rt.mean())
            elif task_name == 'flkr':
                print(loddf.groupby("condition").correct.mean())
                print(loddf.groupby("condition").rt.mean())
            elif task_name == 'rdm':
                loddf['coh_dif'] = np.abs(loddf.left_coherence - loddf.right_coherence)
                print(loddf.groupby('coh_dif').correct.sum())
                print(loddf.groupby('coh_dif').correct.mean())
                print(loddf.groupby('coh_dif').rt.mean())

if __name__ == "__main__":

    parser = ArgumentParser(description = 'Print performance stats')
    parser.add_argument('--workerId', help='Optional: Worker id of the participant to'
                                           ' print performance stats.', default=None)
    args = parser.parse_args()
    data_dir = Path('../data')
    md_dir = Path('../metadata')
    survey_dir = data_dir / 'survey'
    task_data_dir = data_dir / 'task/upload'
    task_db_dir = data_dir / 'task/db'

    for mdp in sorted(md_dir.glob('*')):
        if mdp.parts[-1] == '.placeholder':
            continue

        md_lines = [ll.split('\t') for ll in mdp.read_text().split('\n')]
        fields_to_capture = [
            'workerId',
            'subId',
            'complete'
        ]
        try:
            md = {}
            for mdl in md_lines:
                for field in fields_to_capture:
                    if mdl[1] == field:
                        md[field] = mdl[2]
            if args.workerId is not None:
                if md.get('workerId', None) == args.workerId:
                    print('###################################')
                    print("Worker ID:", md['workerId'])
                    print('###################################')
                    print_task_performance(md['subId'])
                    print()
                    print()
            elif md.get('complete', None) == 'task_invalid':
                # print performance information for all tasks for folks with an invalid task
                print('###################################')
                print("Worker ID:", md['workerId'])
                print('###################################')
                print_task_performance(md['subId'])
                print()
                print()
        except IndexError:
            continue