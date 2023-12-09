import pytest
from utils.environment import TestEnvironment
from utils.client import Client


def pytest_addoption(parser):
    # Add custom option for pytest command
    parser.addoption("--env_prefix", action="store", default=None, help="Test env prefix to run test suite on")


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

