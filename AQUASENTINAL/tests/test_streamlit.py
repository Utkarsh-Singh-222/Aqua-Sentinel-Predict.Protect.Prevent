from streamlit.testing.v1 import AppTest
import os
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def test_app_loads():
    app_path = BASE_DIR / "app" / "main.py"
    at = AppTest.from_file(str(app_path))
    # It takes a moment to run the app
    at.run(timeout=30)
    
    # Assert no exceptions
    assert not at.exception, f"App threw an exception: {at.exception}"
