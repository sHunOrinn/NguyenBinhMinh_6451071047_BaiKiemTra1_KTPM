import os
from datetime import datetime
from pathlib import Path

import pytest
import selenium
from selenium import webdriver

import config
from utils.excel_report import generate_report

ROOT = Path(__file__).parent
SCREENSHOT_DIR = ROOT / "screenshots"
REPORT_DIR = ROOT / "reports"

RESULTS = {} # nodeid -> dict (1 dong cua bao cao)
RUN = {"started": None, "browser": "Chrome", "headless": False}


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False,
                     help="Chay Chrome o che do headless (khong hien cua so)")


def pytest_sessionstart(session):
    RUN["started"] = datetime.now()


# driver
@pytest.fixture
def driver(request):
    headless = config.HEADLESS or request.config.getoption("--headless")
    opts = webdriver.ChromeOptions()
    opts.unhandled_prompt_behavior = "ignore"      # tu xu ly alert, khong de Selenium tu dong tat
    opts.add_argument("--lang=vi")
    if headless:
        for arg in ("--headless=new", "--window-size=1920,1080",
                    "--no-sandbox", "--disable-dev-shm-usage"):
            opts.add_argument(arg)
    d = webdriver.Chrome(options=opts)             # Selenium Manager tu tai driver phu hop
    if not headless:
        d.maximize_window()
    d.set_page_load_timeout(30)
    RUN["headless"] = headless
    RUN["browser"] = f"Chrome {d.capabilities.get('browserVersion', '')}".strip()
    yield d
    d.quit()                                      


# thu thap ket qua
def _first_line(text, limit=400):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    is_final_call = rep.when == "call"
    is_setup_problem = rep.when == "setup" and (rep.skipped or rep.failed)
    if not (is_final_call or is_setup_problem):
        return

    marker = item.get_closest_marker("tc")
    meta = dict(marker.kwargs) if marker else {}
    tc_id = meta.get("id", item.name)

    if rep.passed:
        status, actual = "PASSED", "Đúng như mong đợi"
    elif rep.skipped:
        status = "SKIPPED"
        reason = rep.longrepr[2] if isinstance(rep.longrepr, tuple) else str(rep.longrepr)
        actual = _first_line(reason.replace("Skipped: ", ""))
    else:
        is_assert = call.excinfo is not None and call.excinfo.errisinstance(AssertionError)
        status = "FAILED" if (is_final_call and is_assert) else "ERROR"
        actual = _first_line(call.excinfo.exconly()) if call.excinfo else _first_line(rep.longreprtext)

    shot = ""
    d = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if status in ("FAILED", "ERROR") and d is not None:
        try:
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            path = SCREENSHOT_DIR / f"{tc_id}_{datetime.now():%H%M%S}.png"
            d.save_screenshot(str(path))
            shot = str(path)
        except Exception:
            shot = ""

    RESULTS[item.nodeid] = {
        "id": tc_id,
        "group": meta.get("group", ""),
        "title": meta.get("title", item.name),
        "priority": meta.get("priority", ""),
        "precondition": meta.get("precondition", ""),
        "steps": meta.get("steps", ""),
        "data": meta.get("data", ""),
        "expected": meta.get("expected", ""),
        "actual": actual,
        "status": status,
        "duration": rep.duration,
        "screenshot": shot,
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }


# xuat Excel
def pytest_sessionfinish(session, exitstatus):
    if not RESULTS:
        return
    started = RUN["started"] or datetime.now()
    meta = {
        "system": "Văn phòng điện tử – Trường ĐH Giao thông vận tải (UTC)",
        "url": config.LOGIN_URL,
        "started": started.strftime("%d/%m/%Y %H:%M:%S"),
        "browser": RUN["browser"],
        "mode": "Headless" if RUN["headless"] else "Có giao diện",
        "tools": f"Selenium {selenium.__version__} + pytest {pytest.__version__}",
    }
    out = REPORT_DIR / f"bao_cao_kiem_thu_{started:%Y%m%d_%H%M%S}.xlsx"
    path = generate_report(list(RESULTS.values()), meta, out)
    tr = session.config.pluginmanager.get_plugin("terminalreporter")
    if tr:
        tr.write_line("")
        tr.write_line(f"Da xuat bao cao Excel: {path}")
