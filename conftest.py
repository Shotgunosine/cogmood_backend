import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--server", action="store_true", default=False,
        help="include verification of server-side values, only possible if "
             "run in the directory serving the website"
    )


@pytest.fixture
def server(request):
    return request.config.getoption("--server")