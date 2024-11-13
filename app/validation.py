from zipfile import ZipFile
import tempfile
from . import log

FLKR_THR = 12
FLKR_NTRIALS = 48
FLKR_KEYS = {'run_num', 'appear_time_time', 'appear_time_error', 'disappear_time', 'pressed',
             'press_time_time','press_time_error', 'rt', 'block', 'trial_id', 'correct',
             'fmri_tr_time', 'eeg_pulse_time', 'log_time','loc_x', 'loc_y', 'condition',
             'stim', 'dir', 'corr_resp', 'log_num'}
RDM_THR = 13
RDM_NTRIALS = 68
RDM_KEYS = {'run_num', 'appear_time_time', 'appear_time_error', 'disappear_time_time',
            'disappear_time_error', 'pressed', 'press_time_time', 'press_time_error', 'rt',
            'block', 'trial_id', 'correct', 'refresh_rate', 'fmri_tr_time', 'eeg_pulse_time',
            'log_time', 'left_coherence', 'right_coherence', 'correct_resp',
            'incorrect_resp', 'log_num'}
# this is actually 1 - ntrials, just to make the test easier later
BART_NTRIALS = 17
BART_KEYS = {'subject', 'run_num', 'balloon_number_session', 'set_number', 'balloon_number',
             'block', 'balloon_id', 'bag_ID_number', 'balloon_in_bag', 'trial', 'pop_range_0',
             'pop_range_1', 'pop_status', 'reward_appear_time_time', 'reward_appear_time_error',
             'invis_appear_time_time', 'invis_appear_time_error', 'rt_start_time', 'rt',
             'press_time_time', 'press_time_error', 'key_pressed', 'total', 'grand_total',
             'rewards', 'balloon_size', 'trkp_press_time', 'eeg_pulse_time', 'log_time', 'log_num'}
CAB_THR = 14
CAB_NTRIALS = 48
CAB_KEYS = {'appearL_time', 'appearL_error', 'appearR_time', 'appearR_error', 'disappearL',
            'disappearR', 'resp_acc', 'resp_rt', 'press_time', 'press_error', 'pressed', 'block',
            'trial_id', 'fmri_tr_time', 'eeg_pulse_time', 'log_time', 'pair_inds_0', 'pair_inds_1',
            'cond_strength', 'cond_trial', 'resp_correct', 'num_trial', 'lag_L', 'lag_R', 'img_L',
            'img_R', 'log_num'}

def validate_flkr(zipped_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        slog_file = ZipFile(zipped_path).extract('FLKR_0.slog', path=tmpdir)
        lod = log.log2dl(slog_file)
    if len(lod) != FLKR_NTRIALS:
        return False, 'ntrials'
    if lod[0].keys() != FLKR_KEYS:
        return False, 'keys'
    corrects = [int(dd['correct']) for dd in lod if (dd['condition'] == '+') and (dd['correct'])]
    if len(corrects) < FLKR_THR:
        return False, 'chance'
    return True, 'valid'


def validate_rdm(zipped_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        slog_file = ZipFile(zipped_path).extract('RDM_0.slog', path=tmpdir)
        lod = log.log2dl(slog_file)
    if len(lod) != RDM_NTRIALS:
        return False, 'ntrials'
    if lod[0].keys() != RDM_KEYS:
        return False, 'keys'
    corrects = [
        int(dd['correct'])
        for dd in lod
        if (max(dd['left_coherence'], dd['right_coherence'])
           - min(dd['left_coherence'], dd['right_coherence']) >= 0.24) and (dd['correct'])]
    if len(corrects) < RDM_THR:
        return False, 'chance'
    return True, 'valid'


def validate_bart(zipped_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        slog_file = ZipFile(zipped_path).extract('BART_0.slog', path=tmpdir)
        lod =log.log2dl(slog_file)
    if lod[0].keys() != BART_KEYS:
        return False, 'keys'
    pressed_j = False
    pressed_f = False
    max_balloon = 0
    for dd in lod:
        if not pressed_j and dd['key_pressed'] == 'J':
            pressed_j = True
        elif not pressed_f and dd['key_pressed'] == 'F':
            pressed_f = True
        if dd['balloon_number_session'] > max_balloon:
            max_balloon = dd['balloon_number_session']
    if not pressed_j or not pressed_f:
        return False, 'chance'
    if max_balloon != BART_NTRIALS:
        return False, 'ntrials'
    return True, 'valid'


def validate_cab(zipped_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        slog_file = ZipFile(zipped_path).extract('CAB_0.slog', path=tmpdir)
        lod = log.log2dl(slog_file)
    if len(lod) != CAB_NTRIALS:
        return False, 'ntrials'
    if lod[0].keys() != CAB_KEYS:
        return False, 'keys'
    corrects = [
        int(dd['resp_acc'])
        for dd in lod
        if dd['resp_acc']
        and (
                   (dd['cond_trial'] == 'new')
                   or (dd['cond_strength'] == 'strong' and dd['cond_trial'] != 'recombined')
        )
    ]
    if len(corrects) < CAB_THR:
        return False, 'chance'
    return True, 'valid'


def validate(zipped_path, task):
    if task == 'flkr':
        return validate_flkr(zipped_path)
    elif task == 'rdm':
        return validate_rdm(zipped_path)
    elif task == 'bart':
        return validate_bart(zipped_path)
    elif task == 'cab':
        return validate_cab(zipped_path)
    else:
        raise NotImplementedError(f'No validation implemented for {task}.')
