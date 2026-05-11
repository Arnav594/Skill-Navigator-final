"""Integration tests against the Flask test client.

Covers the original 4 scenarios plus role-not-found for quiz.
The AI calls inside /analyze will silently fail (no Groq key in test env)
and fall back to rule-based — which is exactly the path we want exercised.
"""
import json


# ---------- /analyze ----------

def test_analyze_happy_path(client):
    """Valid resume text + role returns the full result schema."""
    response = client.post(
        "/analyze",
        data={
            "message": "I am a developer with experience in Python, SQL and APIs.",
            "role": "Backend Developer",
            "roadmap_requested": "false",
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    result = json.loads(response.data)

    for key in ("skills", "missing", "suggestions", "roadmap", "reliability_score"):
        assert key in result

    assert isinstance(result["skills"], list)
    assert isinstance(result["missing"], list)
    assert 0 <= result["reliability_score"] <= 100
    assert len(result["suggestions"]) > 0


def test_analyze_empty_input_returns_400(client):
    """No file and no message means 400 with an error message."""
    response = client.post(
        "/analyze",
        data={"message": "", "role": "Backend Developer", "roadmap_requested": "false"},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "error" in result
    assert len(result["error"]) > 0


# ---------- /quiz ----------

def test_quiz_returns_questions_for_valid_role(client):
    """Quiz route should return up to 5 well-formed questions for a known role."""
    response = client.get("/quiz?role=Backend Developer")
    assert response.status_code == 200
    result = json.loads(response.data)

    assert "questions" in result
    assert len(result["questions"]) > 0
    for q in result["questions"]:
        assert "question" in q
        assert "options" in q
        assert "correct" in q
        assert "explanation" in q
        # Options must be a dict keyed A-D
        assert set(q["options"].keys()) == {"A", "B", "C", "D"}


def test_quiz_missing_role_returns_400(client):
    """No role query param is a 400, not a crash."""
    response = client.get("/quiz")
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "error" in result


def test_quiz_unknown_role_returns_404(client):
    """Unknown role should be a 404, not 500."""
    response = client.get("/quiz?role=Astronaut")
    assert response.status_code == 404
    result = json.loads(response.data)
    assert "error" in result


# ---------- /roles ----------

def test_roles_returns_sorted_list(client):
    """GET /roles returns a sorted JSON array of role strings."""
    response = client.get("/roles")
    assert response.status_code == 200
    roles = json.loads(response.data)
    assert isinstance(roles, list)
    assert len(roles) > 0
    assert roles == sorted(roles)
