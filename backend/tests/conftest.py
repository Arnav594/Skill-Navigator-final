"""Shared pytest fixtures.

`client` provides a Flask test client.
`sample_role_data` is a deterministic role_data shape matching skills.csv rows.
`sample_resume` is a representative resume blob for unit tests.
"""
import sys
import os
import pytest

# Make backend root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def sample_role_data():
    """Mimics rows that load_role_data would return for Backend Developer."""
    return [
        {"role": "Backend Developer", "skill": "Python",      "learning_order": "1", "priority": "high"},
        {"role": "Backend Developer", "skill": "SQL",         "learning_order": "2", "priority": "high"},
        {"role": "Backend Developer", "skill": "FastAPI",     "learning_order": "3", "priority": "high"},
        {"role": "Backend Developer", "skill": "PostgreSQL",  "learning_order": "4", "priority": "medium"},
        {"role": "Backend Developer", "skill": "Docker",      "learning_order": "5", "priority": "medium"},
    ]


@pytest.fixture
def sample_resume():
    return (
        "John Doe — Backend Developer\n"
        "EXPERIENCE: Developed Python REST APIs with FastAPI. "
        "Optimized PostgreSQL queries reducing latency by 40%. "
        "Led a team that shipped a microservice in 3 months.\n"
        "SKILLS: Python, SQL, Docker, AWS\n"
        "EDUCATION: B.Tech Computer Science"
    )
