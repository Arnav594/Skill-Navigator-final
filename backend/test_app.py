import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app, extract_skills, analyze_gap, resume_suggestions, learning_roadmap

# ✅ TEST SETUP
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ================================================
# TEST 1 — HAPPY PATH
# User submits a valid resume with known skills
# and gets back a proper analysis response
# ================================================
def test_happy_path_analyze(client):
    """
    Happy path: A user submits a resume with
    known skills for Backend Developer role.
    Expects a valid response with skills,
    missing skills, suggestions and roadmap.
    """
    data = {
        "message": "I am a developer with experience in Python, SQL and APIs.",
        "role": "Backend Developer",
        "roadmap_requested": "false"
    }

    response = client.post(
        "/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    result = json.loads(response.data)

    # Must have all required fields
    assert "skills" in result
    assert "missing" in result
    assert "suggestions" in result
    assert "roadmap" in result
    assert "reliability_score" in result

    # Skills must be a list
    assert isinstance(result["skills"], list)

    # Missing must be a list
    assert isinstance(result["missing"], list)

    # Reliability score must be between 0 and 100
    assert 0 <= result["reliability_score"] <= 100

    # Suggestions must not be empty
    assert len(result["suggestions"]) > 0

    print("✅ Happy path test passed!")

# ================================================
# TEST 2 — EDGE CASE
# User submits empty resume and message
# Expects a proper error response
# ================================================
def test_edge_case_empty_input(client):
    """
    Edge case: User submits completely empty
    input with no file and no message.
    Expects a 400 error with a clear message.
    """
    data = {
        "message": "",
        "role": "Backend Developer",
        "roadmap_requested": "false"
    }

    response = client.post(
        "/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

    result = json.loads(response.data)

    # Must return an error message
    assert "error" in result

    # Error message must not be empty
    assert len(result["error"]) > 0

    print("✅ Edge case test passed!")

# ================================================
# TEST 3 — UNIT TEST
# Test rule-based skill extraction fallback
# ================================================
def test_skill_extraction_fallback():
    """
    Unit test: Rule-based skill extraction
    should correctly identify known skills
    from resume text without AI.
    """
    resume_text = "I have experience with Python, SQL, Docker and AWS."
    skills = extract_skills(resume_text)

    assert "Python" in skills
    assert "SQL" in skills
    assert "Docker" in skills
    assert "AWS" in skills

    print("✅ Skill extraction fallback test passed!")

# ================================================
# TEST 4 — UNIT TEST
# Test quiz route returns questions
# ================================================
def test_quiz_route(client):
    """
    Happy path: Quiz route should return
    5 questions for a valid role.
    """
    response = client.get("/quiz?role=Backend Developer")

    assert response.status_code == 200

    result = json.loads(response.data)

    assert "questions" in result
    assert len(result["questions"]) > 0
    assert len(result["questions"]) <= 5

    # Each question must have required fields
    for q in result["questions"]:
        assert "question" in q
        assert "options" in q
        assert "correct" in q
        assert "explanation" in q

    print("✅ Quiz route test passed!")