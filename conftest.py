import pytest
from py.xml import html
from utils.environment import TestEnvironment
from utils.client import Client


def pytest_addoption(parser):
    # Add custom option for pytest command
    parser.addoption("--env_prefix", action="store", default=None, help="Test env prefix to run test suite on")


#######################################
# Fixtures
#######################################


@pytest.fixture(scope="session")
def env(request):
    env_prefix = request.config.getoption("--env_prefix")
    if not env_prefix:
        env_prefix = "jsonplaceholder"   # Production env
        # domain_prefix = "qa-jsonplaceholder"   # Fake QA env
        # domain_prefix = "dev-jsonplaceholder"   # Fake Dev env

    env = TestEnvironment(env_prefix)
    return env


@pytest.fixture(scope="session")
def client(env):
    client = Client(env=env)
    yield client
    client.session.close()


#######################################
# HTML Report Hooks
#######################################


def pytest_html_results_table_header(cells):
    try:
        # Rename "Links" column to "Failed Step"
        cells[-1] = html.th("Failed Step", class_="sortable result-links", col="result-links")
    except Exception:
        pass


def pytest_html_results_table_row(report, cells):
    try:
        # Add step name to Failed Step cell
        if report.failed:
            steps = report.scenario["steps"]
            failed_step = next(step for step in steps if step["failed"])
            cells[-1] = html.td(f"{failed_step['name']}", class_="col-name", style="color:red; font-weight:bold;")
    except Exception as e:
        pass
