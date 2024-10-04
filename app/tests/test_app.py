import os
import re
from hashlib import blake2b
from pathlib import Path
import json
from playwright.sync_api import Page, expect
from .helpers import get_new_workerid
from ..config import CFG
import pytest

TESTURL="http://127.0.0.1:5000/"
def test_no_workerid(page: Page):
    page.goto(TESTURL)
    expect(page.locator("body")).to_contain_text("Sorry, there was an error. Sorry, we are missing your Prolific ID. Please start the experiment over from the Prolific link.")


def test_consent(page: Page):
    workerId = get_new_workerid()
    page.goto(f"{TESTURL}?PROLIFIC_PID={workerId}")
    expect(page.locator("body")).to_contain_text("Welcome to the mood and cognition tasks,")

    agree = page.get_by_role("button", name="I agree")
    agree.click()

    expect(page.locator("body")).to_contain_text("Attention")


def test_survey_complete(page: Page, request):
    workerId = get_new_workerid()
    page.goto(f"{TESTURL}?PROLIFIC_PID={workerId}")
    expect(page).to_have_url(f'{TESTURL}consent?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I agree").click()
    expect(page).to_have_url(f'{TESTURL}alert?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I understand").click()
    expect(page).to_have_url(f'{TESTURL}survey?PROLIFIC_PID={workerId}')
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
            elif qq['type'] == 'html':
                continue
        if pgn + 1 == len(survey_input):
            page.get_by_role("button", name="Complete").click()
        else:
            page.get_by_role("button", name="Next").click()
    expect(page).to_have_url(f'{TESTURL}taskstart?PROLIFIC_PID={workerId}')

    # get saved data and compare to expectation
    h_workerId = blake2b(workerId.encode(), digest_size=20).hexdigest()
    with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
        logs = f.read()
    subId = re.search('subId\t(.*)\n', logs).group(1)
    fin = os.path.join(CFG['s_complete'], '%s.json' % subId)
    with open(fin, 'r') as f:
        saved_data = json.loads(f.read())

    assert saved_data[0]['response'] == expected_out

def test_survey_attn1(page: Page, request):
    workerId = get_new_workerid()
    page.goto(f"{TESTURL}?PROLIFIC_PID={workerId}")
    expect(page).to_have_url(f'{TESTURL}consent?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I agree").click()
    expect(page).to_have_url(f'{TESTURL}alert?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I understand").click()
    expect(page).to_have_url(f'{TESTURL}survey?PROLIFIC_PID={workerId}')
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
            page.get_by_role("button", name="Complete").click()
        else:
            page.get_by_role("button", name="Next").click()
    expect(page).to_have_url(f'{TESTURL}error/1008')

    # get saved data and compare to expectation
    h_workerId = blake2b(workerId.encode(), digest_size=20).hexdigest()
    with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
        logs = f.read()
    subId = re.search('subId\t(.*)\n', logs).group(1)
    fin = os.path.join(CFG['s_reject'], '%s.json' % subId)
    with open(fin, 'r') as f:
        saved_data = json.loads(f.read())

    for k,v in saved_data[0]['response'].items():
        if v is not None:
            assert expected_out[k] == v


def test_survey_attn3(page: Page, request):
    workerId = get_new_workerid()
    page.goto(f"{TESTURL}?PROLIFIC_PID={workerId}")
    expect(page).to_have_url(f'{TESTURL}consent?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I agree").click()
    expect(page).to_have_url(f'{TESTURL}alert?PROLIFIC_PID={workerId}')
    page.get_by_role("button", name="I understand").click()
    expect(page).to_have_url(f'{TESTURL}survey?PROLIFIC_PID={workerId}')
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
        page.get_by_role("button", name="Next").click()
    expect(page.get_by_role("img", name="Prolific logo")).to_be_visible()

    # get saved data and compare to expectation
    h_workerId = blake2b(workerId.encode(), digest_size=20).hexdigest()
    with open(os.path.join(CFG['meta'], h_workerId), 'r') as f:
        logs = f.read()
    subId = re.search('subId\t(.*)\n', logs).group(1)
    fin = os.path.join(CFG['s_reject'], '%s.json' % subId)
    with open(fin, 'r') as f:
        saved_data = json.loads(f.read())

    for k,v in saved_data[0]['response'].items():
        if v is not None:
            assert expected_out[k] == v
