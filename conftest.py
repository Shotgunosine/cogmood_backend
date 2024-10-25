import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--server", action="store_true", default=False,
        help="include verification of server-side values, only possible if "
             "run in the directory serving the website"
    )
    parser.addoption(
        "--loadtest", action="store_true", default=False,
        help="disable redirection to proflific pages,"
             "for use during load testing"
    )
    parser.addoption(
        "--url", action="store", default="127.0.0.1:8000",
        help="url for the tests to run against"
    )


@pytest.fixture
def server(request):
    return request.config.getoption("--server")

@pytest.fixture
def url(request):
    return f'http://{request.config.getoption("--url")}/'

@pytest.fixture()
def loadtest(request):
    return request.config.getoption("--loadtest")
