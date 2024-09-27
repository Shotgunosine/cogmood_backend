import re
from playwright.sync_api import Page, expect

def test_no_workerid(page: Page):
    page.goto("http://127.0.0.1:5000/")
    expect(page.locator("body")).to_contain_text("Sorry, there was an error. Sorry, we are missing your Prolific ID. Please start the experiment over from the Prolific link.")
