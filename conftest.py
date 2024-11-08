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
    parser.addoption(
        "--ignore-https-errors", action="store_true", default=False,
        help="ignore https errors to enable testing with self-signed cert"
    )


@pytest.fixture
def server(request):
    return request.config.getoption("--server")

@pytest.fixture
def url(request):
    return f'https://{request.config.getoption("--url")}/'

@pytest.fixture()
def loadtest(request):
    return request.config.getoption("--loadtest")

@pytest.fixture()
def ignore_https_errors(request):
    return request.config.getoption("--ignore-https-errors")

@pytest.fixture(scope="session")
def browser_context_args(request, browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": request.config.getoption("--ignore-https-errors")
    }
