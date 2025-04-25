import os
import importlib
import pytest
from typing import Any

# Add option to use a specific runner
def pytest_addoption(parser):
    parser.addoption(
        "--runner",
        default=os.environ.get("PYTEST_RUNNER", "ldk_lnprototest.Runner"),
        help="Runner to use for tests",
    )

@pytest.fixture(scope="function")
def runner(pytestconfig: Any) -> Any:
    """Return an instance of the requested runner"""
    runner_name = pytestconfig.getoption("runner")
    try:
        # Split into module and class parts
        module_name, class_name = runner_name.rsplit(".", 1)
        runner_module = importlib.import_module(module_name)
        runner_class = getattr(runner_module, class_name)
        return runner_class(pytestconfig)
    except (ImportError, AttributeError) as e:
        pytest.fail(f"Failed to load runner {runner_name}: {e}")
