import os

import pytest


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_E2E") != "1",
    reason="E2E test requires Playwright and a live FastAPI server.",
)


def test_app_homepage(page):
    page.goto("http://127.0.0.1:8000/")

    assert "FastAPI Calculator" in page.content()
