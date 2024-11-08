import os
import re
from hashlib import blake2b
from pathlib import Path
import json
from playwright.sync_api import Page, expect
from .helpers import get_new_workerid
from ..config import CFG
from .. import ROOT_DIR
import pytest
import requests
from itsdangerous.serializer import Serializer
import configparser
from ..io import hash_file
from ..utils import pseudorandomize
import logging

LOGGER = logging.getLogger(__name__)

def logged_goto(page, url):
    page.on('request', lambda request: LOGGER.info([request.method, request.url]))
    page.on('response', lambda response: LOGGER.info([response.status, response.url]))
    page.goto(url)

def test_pseudorandomize():
    blocks = ['foo', 'bar', 'baz']
    for nreps in range(5):
        res = pseudorandomize(blocks, nreps)
        fcount = 0
        bcount = 0
        zcount = 0
        lastblock = ""
        for bb in res:
            if bb == 'foo':
                fcount += 1
            elif bb == 'bar':
                bcount += 1
            elif bb == 'baz':
                zcount += 1
            assert bb != lastblock
            lastblock = bb
        assert fcount == nreps
        assert bcount == nreps
        assert zcount == nreps

def test_no_workerid(url, page: Page):
    LOGGER.info('RUNNING: test_no_workerid')
    logged_goto(page, url)
    expect(page.locator("body")).to_contain_text("Sorry, there was an error. Sorry, we are missing your Prolific ID. Please start the experiment over from the Prolific link.")
    LOGGER.info('PASSED: test_no_workerid')


@pytest.mark.browser_context_args(user_agent="macintosh")
def test_consent(url, page: Page):
    LOGGER.info('RUNNING: test_no_consent')
    workerId = get_new_workerid()
    logged_goto(page, f'{url}?PROLIFIC_PID={workerId}')
    expect(page.locator("body")).to_contain_text("Welcome to the mood and cognition tasks,")

    agree = page.get_by_role("button", name="I agree")
    agree.click()

    expect(page.locator("body")).to_contain_text("Attention")
    LOGGER.info('PASSED: test_no_consent')

@pytest.mark.browser_context_args(user_agent="macintosh")
def test_survey_complete(url, server, page: Page, request):
    LOGGER.info('RUNNING: test_survey_complete')
    workerId = get_new_workerid()
    logged_goto(page, f"{url}?PROLIFIC_PID={workerId}")
    expect(page).to_have_url(f'{url}consent?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I agree").click()
    expect(page).to_have_url(f'{url}alert?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I understand").click()
    expect(page).to_have_url(f'{url}survey?PROLIFIC_PID={workerId}')
    test_dir = Path(request.path).parent
    input_path = test_dir / 'data/surveyinput_1.json'
    survey_input = json.loads(input_path.read_text())
    expected_out_path = test_dir / 'data/surveyexpectedoutput_1.json'
    expected_out = json.loads(expected_out_path.read_text())

    for pgn, pg in enumerate(survey_input):
        for qq in pg:
            if qq['type'] in ['radiogroup', 'checkbox']:
                page.get_by_label(qq['title']).locator("label").filter(has_text=qq['answer']).click()
            elif qq['type'] == 'text':
                page.get_by_label(qq['title']).fill(str(qq['answer']))
            elif qq['type'] == 'matrix':
                qqname = f"row {qq['title']}, column {qq['answer']}"
                page.get_by_role("cell", name=qqname).locator("label").click()
            elif qq['type'] == 'ladder':
                answer = qq['answer'].replace(' ', '-')
                if qq['answer'] in ['Bottom rung', 'Top rung']:
                    page.locator(f"#{answer}").click()
                else:
                    page.locator(f"[id=\"\\3{answer}\"]").click()
            elif qq['type'] == 'html':
                continue
        if pgn + 1 == len(survey_input):
            page.get_by_role("button", name="Complete").click()
        else:
            page.get_by_role("button", name="Next").click()
    expect(page).to_have_url(f'{url}taskstart?PROLIFIC_PID={workerId}')

    if server:
        # get saved data and compare to expectation
        h_workerId = blake2b(workerId.encode(), digest_size=24).hexdigest()
        with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
            logs = f.read()
        subId = re.search('subId\t(.*)\n', logs).group(1)
        fin = os.path.join(CFG['s_complete'], '%s.json' % subId)
        with open(fin, 'r') as f:
            saved_data = json.loads(f.read())

        assert saved_data[0]['response'] == expected_out

    LOGGER.info('PASSED: test_survey_complete')


@pytest.mark.browser_context_args(user_agent="macintosh")
def test_survey_attn1(url, server, loadtest, page: Page, request):
    LOGGER.info('RUNNING: test_survey_attn1')
    workerId = get_new_workerid()
    logged_goto(page, f"{url}?PROLIFIC_PID={workerId}")
    expect(page).to_have_url(f'{url}consent?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I agree").click()
    expect(page).to_have_url(f'{url}alert?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I understand").click()
    expect(page).to_have_url(f'{url}survey?PROLIFIC_PID={workerId}')
    test_dir = Path(request.path).parent
    input_path = test_dir / 'data/surveyinput_2.json'
    survey_input = json.loads(input_path.read_text())
    expected_out_path = test_dir / 'data/surveyexpectedoutput_2.json'
    expected_out = json.loads(expected_out_path.read_text())

    for pgn, pg in enumerate(survey_input):
        for qq in pg:
            if qq['type'] in ['radiogroup', 'checkbox']:
                page.get_by_label(qq['title']).locator("label").filter(has_text=qq['answer']).click()
            elif qq['type'] == 'text':
                page.get_by_label(qq['title']).fill(str(qq['answer']))
            elif qq['type'] == 'matrix':
                qqname = f"row {qq['title']}, column {qq['answer']}"
                page.get_by_role("cell", name=qqname).locator("label").click()
            elif qq['type'] == 'html':
                continue
        if pgn + 1 == len(survey_input):
            if not loadtest:
                page.get_by_role("button", name="Complete").click()
        else:
            page.get_by_role("button", name="Next").click()
    if not loadtest:
        expect(page).to_have_url(f'{url}error/1008')

    if server:
        # get saved data and compare to expectation
        h_workerId = blake2b(workerId.encode(), digest_size=24).hexdigest()
        with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
            logs = f.read()
        subId = re.search('subId\t(.*)\n', logs).group(1)
        fin = os.path.join(CFG['s_reject'], '%s.json' % subId)
        with open(fin, 'r') as f:
            saved_data = json.loads(f.read())

        for k,v in saved_data[0]['response'].items():
            if v is not None:
                assert expected_out[k] == v
    LOGGER.info('PASSED: test_survey_attn1')


@pytest.mark.browser_context_args(user_agent="macintosh")
def test_survey_attn3(url, server, loadtest, page: Page, request):
    LOGGER.info('RUNNING: test_survey_attn3')
    workerId = get_new_workerid()
    logged_goto(page, f"{url}?PROLIFIC_PID={workerId}")
    expect(page).to_have_url(f'{url}consent?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I agree").click()
    expect(page).to_have_url(f'{url}alert?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I understand").click()
    expect(page).to_have_url(f'{url}survey?PROLIFIC_PID={workerId}')
    test_dir = Path(request.path).parent
    input_path = test_dir / 'data/surveyinput_3.json'
    survey_input = json.loads(input_path.read_text())
    expected_out_path = test_dir / 'data/surveyexpectedoutput_3.json'
    expected_out = json.loads(expected_out_path.read_text())

    for pgn, pg in enumerate(survey_input):
        for qq in pg:
            if qq['type'] in ['radiogroup', 'checkbox']:
                page.get_by_label(qq['title']).locator("label").filter(has_text=qq['answer']).click()
            elif qq['type'] == 'text':
                page.get_by_label(qq['title']).fill(str(qq['answer']))
            elif qq['type'] == 'matrix':
                qqname = f"row {qq['title']}, column {qq['answer']}"
                page.get_by_role("cell", name=qqname).locator("label").click()
            elif qq['type'] == 'html':
                continue
        if pgn + 1 == len(survey_input):
            if not loadtest:
                page.get_by_role("button", name="Next").click()
        else:
            page.get_by_role("button", name="Next").click()
    if not loadtest:
        expect(page.get_by_role("img", name="Prolific logo")).to_be_visible()

    if server:
        # get saved data and compare to expectation
        h_workerId = blake2b(workerId.encode(), digest_size=24).hexdigest()
        with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
            logs = f.read()
        subId = re.search('subId\t(.*)\n', logs).group(1)
        fin = os.path.join(CFG['s_reject'], '%s.json' % subId)
        with open(fin, 'r') as f:
            saved_data = json.loads(f.read())

        for k,v in saved_data[0]['response'].items():
            if v is not None:
                assert expected_out[k] == v
    LOGGER.info('PASSED: test_survey_attn3')


@pytest.mark.browser_context_args(user_agent="macintosh")
def test_taskcontrol(url, server, loadtest, ignore_https_errors, page: Page, request):
    LOGGER.info('RUNNING: test_taskcontrol')
    workerId = get_new_workerid()
    logged_goto(page, f"{url}?PROLIFIC_PID={workerId}")
    expect(page).to_have_url(f'{url}consent?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I agree").click()
    expect(page).to_have_url(f'{url}alert?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I understand").click()
    expect(page).to_have_url(f'{url}survey?PROLIFIC_PID={workerId}')
    test_dir = Path(request.path).parent
    input_path = test_dir / 'data/surveyinput_1.json'
    survey_input = json.loads(input_path.read_text())
    expected_out_path = test_dir / 'data/surveyexpectedoutput_1.json'
    expected_out = json.loads(expected_out_path.read_text())

    verify = True
    if ignore_https_errors:
        verify = False

    for pgn, pg in enumerate(survey_input):
        for qq in pg:
            if qq['type'] in ['radiogroup', 'checkbox']:
                page.get_by_label(qq['title']).locator("label").filter(has_text=qq['answer']).click()
            elif qq['type'] == 'text':
                page.get_by_label(qq['title']).fill(str(qq['answer']))
            elif qq['type'] == 'matrix':
                qqname = f"row {qq['title']}, column {qq['answer']}"
                page.get_by_role("cell", name=qqname).locator("label").click()
            elif qq['type'] == 'html':
                continue
        if pgn + 1 == len(survey_input):
            page.get_by_role("button", name="Complete").click()
        else:
            page.get_by_role("button", name="Next").click()
    expect(page).to_have_url(f'{url}taskstart?PROLIFIC_PID={workerId}')

    # mock task communication with server
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(ROOT_DIR, 'app.ini'))
    supreme_secret_key = cfg['SUPREME']['SECRET_KEY']
    serializer = Serializer(supreme_secret_key)
    h_workerId = blake2b(workerId.encode(), digest_size=24).hexdigest()

    # test initial get
    LOGGER.info(['GET', f"{url}taskcontrol"])
    req = requests.get(
        url=f"{url}taskcontrol",
        params={'worker_id':serializer.dumps(h_workerId)},
        verify=verify
    )
    LOGGER.info([req.status_code, f"{url}taskcontrol"])
    req_dat = req.json()
    assert req.status_code == 200

    # get expected response
    blocks = CFG['blocks']
    blocks.extend(CFG['blocks'])
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

    expected_blocks = [bb['name'] for bb in blocks_json]

    for eb in expected_blocks:
        assert eb in req_dat['blocks_to_run']

    for bb in req_dat['blocks_to_run']:
        assert bb in expected_blocks

    while len(expected_blocks) != 0:
        # test upload
        completed_block = expected_blocks.pop()
        test_data_path = test_dir / 'data/oneblock_test.zip'
        checksum = hash_file(test_data_path)

        with open(test_data_path, 'rb') as f:
            LOGGER.info(['POST', f"{url}taskcontrol"])
            req = requests.post(
                url=f"{url}taskcontrol",
                params={'worker_id': serializer.dumps(h_workerId)},
                data={
                    'block_name': completed_block,
                    'checksum': checksum
                },
                files={'file': f},
                verify=verify
            )
            LOGGER.info([req.status_code, f"{url}taskcontrol"])

        assert req.status_code == 200

        # test next get
        LOGGER.info(['GET', f"{url}taskcontrol"])
        req = requests.get(
            url=f"{url}taskcontrol",
            params={'worker_id': serializer.dumps(h_workerId)},
            verify=verify
        )
        LOGGER.info([req.status_code, f"{url}taskcontrol"])
        req_dat = req.json()
        assert req.status_code == 200

        for eb in expected_blocks:
            assert eb in req_dat['blocks_to_run']

        for bb in req_dat['blocks_to_run']:
            assert bb in expected_blocks

        if server:
            # confirm stdb updated
            with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
                logs = f.read()
            subId = re.search('subId\t(.*)\n', logs).group(1)
            with open(os.path.join(CFG['t_db'], f'{subId}.json'), 'r') as f:
                s_tdb = json.loads(f.read())

            for bb in s_tdb:
                if bb['name'] == completed_block:
                    assert bb['uploaded']
                    assert bb['checksum'] == checksum
                    assert bb['valid']

    if server:
        # confirm that task is marked as complete
        with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
            logs = f.read()
        assert re.search('complete\t(.*)\n', logs).group(1) == 'success'

    if not loadtest:
        page.goto(f"{url}?PROLIFIC_PID={workerId}")
        expect(page.get_by_role("img", name="Prolific logo")).to_be_visible()

    LOGGER.info('PASSED: test_taskcontrol')
