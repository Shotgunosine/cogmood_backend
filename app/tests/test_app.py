import re
from playwright.sync_api import Page, expect
from .helpers import get_new_workerid

def test_no_workerid(page: Page):
    page.goto("http://127.0.0.1:5000/")
    expect(page.locator("body")).to_contain_text("Sorry, there was an error. Sorry, we are missing your Prolific ID. Please start the experiment over from the Prolific link.")

def test_consent(page: Page):
    workerId = get_new_workerid()
    page.goto(f"http://127.0.0.1:5000/?PROLIFIC_PID={workerId}")
    expect(page.locator("body")).to_contain_text("Welcome to the mood and cognition tasks,")

    agree = page.get_by_role("button", name="I agree")
    agree.click()

    expect(page.locator("body")).to_contain_text("Attention")