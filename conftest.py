import pytest
from bs4 import BeautifulSoup
from support.environment import Environment
from support.client import Client

##########################################
# Shared steps in pytest global context
##########################################
from steps.auth.steps import *



def pytest_addoption(parser):
    # Add custom option for pytest command
    parser.addoption("--env_prefix", action="store", default=None, help="Prefix of the tested environment domain")


#######################################
# Fixtures
#######################################


@pytest.fixture(scope="session")
def env(request):
    """Create environment configuration fixture.
    Environment can be specified via --env command line option.
    Defaults to production(no prefix).
    """
    env_prefix = request.config.getoption("--env_prefix")
    if not env_prefix:
        env_prefix = ""         # Production env(has not prefix)
        # env_prefix = "qa"     # Fake QA env
        # env_prefix = "dev"    # Fake Dev env
    env = Environment(env_prefix)
    return env


@pytest.fixture(scope="session")
def client(env):
    """Create HTTP client fixture with session management.

    Client is session-scoped for performance - shares connection pool across all tests.
    Session is properly closed after all tests complete.
    """
    client = Client(env=env)
    yield client
    client.session.close()  # Runs at the end of test session


#######################################
# HTML Report Configuration
#######################################

def pytest_bdd_after_scenario(request):
    # Reset client after each test for isolation
    if "client" in request.node.fixturenames:
        client = request.getfixturevalue("client")
        client.reset_session()

    # Reset client and prints all fixtures used in the test to stdout for HTML report
    excluded_fixtures = ("pytestconfig", "request")
    try:
        for fixture_name in request.node.fixturenames:
            if fixture_name not in excluded_fixtures:
                fixture_value = request.getfixturevalue(fixture_name)
                print(f"{fixture_name}: {fixture_value} \n")
    except Exception as e:
        print(f"Error adding fixture data to stdout: {e}")


def pytest_html_results_table_header(cells):
    try:
        # Rename Links column to "Scenario Details"
        soup = BeautifulSoup("", "html.parser")
        th = soup.new_tag("th", **{"class": "sortable result-links", "col": "result-links"})
        th.string = "Scenario Details"
        cells[-1] = th
    except Exception:
        pass


def pytest_html_results_summary(prefix):
    # Wrap CSS for long text in log section
    prefix.extend(["<style>.log, .log * { overflow-wrap:anywhere; word-break:break-word; }</style>"])


def pytest_html_results_table_row(report, cells):
    try:
        if hasattr(report, 'scenario'):
            steps = report.scenario["steps"]
            scenario_name = report.scenario.get("name", "Unknown Scenario")

            soup = BeautifulSoup("", "html.parser")
            td = soup.new_tag("td", **{"class": "col-name"})
            # Scenario name with color based on test status
            scenario_color = "green" if not report.failed else "#bf0026"
            status_emoji = "❌" if report.failed else "✅"
            scenario_header = soup.new_tag("div",
                                           style=f"font-weight:bold; font-size:16px; margin-bottom:10px; color:{scenario_color};")
            scenario_header.string = f"{status_emoji} Scenario: {scenario_name}"
            td.append(scenario_header)

            # Add just scenario name if test passed
            if not report.failed:
                cells[-1] = td
                return

            # For failed tests only
            failed_step_index = next(i for i, step in enumerate(steps) if step.get("failed", False))

            # Add all steps, highlighting the failed one
            for i, step in enumerate(steps):
                step_div = soup.new_tag("div", style="margin-left:15px; margin-bottom:5px;")
                step_content = soup.new_tag("span",
                                            style="color:red; font-weight:bold;" if i == failed_step_index else "")
                step_content.string = f"{step['keyword']} {step['name']}"
                step_div.append(step_content)
                td.append(step_div)

            cells[-1] = td

    except Exception as e:
        print("Failed to modify HTML report:", e)