import sys
import os
import pytest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from utils.config import get_config
from utils.logger import get_logger

logger = get_logger("conftest")


@pytest.fixture(scope="session")
def config():
    return get_config()


def _dismiss_demo_modal(page):
    modal = page.locator("#demoWarningModal")
    try:
        modal.wait_for(state="visible", timeout=3000)
        page.get_by_role("button", name="I Understand & Continue").click()
        modal.wait_for(state="hidden", timeout=3000)
    except Exception:
        pass


@pytest.fixture(autouse=True)
def dismiss_modal(page):
    _dismiss_demo_modal(page)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, config):
    return {
        **browser_context_args,
        "base_url": config["base_url"],
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, config):
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": config["headless"],
        "slow_mo": config["slow_mo"],
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]

        # Capture screenshot on failure for debugging
        screenshot_path = f"reports/{item.nodeid.replace('/', '_').replace('::', '_')}.png"
        page.screenshot(path=screenshot_path)
        logger.error(f"Test failed — screenshot saved: {screenshot_path}")

        # Persist error log so llm_runner.py can analyze it
        error_log = str(report.longrepr)
        error_file = "reports/last_failure.txt"
        os.makedirs("reports", exist_ok=True)
        with open(error_file, "w") as f:
            f.write(f"Test: {item.nodeid}\n\n")
            f.write(error_log)
        logger.error(f"Error log saved: {error_file}")
