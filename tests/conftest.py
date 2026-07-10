# tests/conftest.py
import pytest
import os
import sys
from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app

@pytest.fixture
def client():
    """Create test client"""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def app_context():
    """Create application context"""
    with flask_app.app_context():
        yield