"""
Phase 9 merge reference for backend/tests/conftest.py.

Merge this behaviour into the existing conftest.py instead of replacing fixtures
that already support the SmartLMS test suite.
"""

import os

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    database_url = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///:memory:",
    )

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": database_url,
            "JWT_SECRET_KEY": "test-secret-key",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
