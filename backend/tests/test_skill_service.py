"""Tests for services/skill_service.py — pure functions, no mocking needed."""
from services.skill_service import extract_skills, analyze_gap, skill_confidence


# ---------- extract_skills (rule-based fallback) ----------

def test_extract_skills_finds_known_skills():
    """Rule-based extractor should pick up exact-match skills from the catalog."""
    text = "I have experience with Python, SQL, Docker and AWS."
    skills = extract_skills(text)
    assert "Python" in skills
    assert "SQL" in skills
    assert "Docker" in skills
    assert "AWS" in skills


def test_extract_skills_is_case_insensitive():
    """Skill detection must not depend on casing in the resume."""
    text = "i love python and PostgreSQL and reactjs"
    skills = extract_skills(text)
    assert "Python" in skills
    assert "PostgreSQL" in skills


def test_extract_skills_returns_empty_for_no_match():
    """No skills means empty list, not error."""
    skills = extract_skills("This text contains no recognizable technologies.")
    assert skills == []


def test_extract_skills_no_duplicates():
    """A skill mentioned twice should appear once in the result."""
    text = "Python python PYTHON python"
    skills = extract_skills(text)
    assert skills.count("Python") == 1


# ---------- analyze_gap ----------

def test_analyze_gap_identifies_missing_skills(sample_role_data):
    """Skills required by the role but absent from the user list become 'missing'."""
    user_skills = ["Python", "SQL"]
    present, missing = analyze_gap(user_skills, sample_role_data)
    assert present == user_skills
    assert "FastAPI" in missing
    assert "PostgreSQL" in missing
    assert "Docker" in missing
    assert "Python" not in missing


def test_analyze_gap_with_full_match(sample_role_data):
    """User who has every required skill should have an empty 'missing' list."""
    full_skills = [item["skill"] for item in sample_role_data]
    present, missing = analyze_gap(full_skills, sample_role_data)
    assert missing == []


def test_analyze_gap_with_empty_role_data():
    """Role with no required skills means nothing can be missing."""
    present, missing = analyze_gap(["Python"], [])
    assert missing == []


# ---------- skill_confidence ----------

def test_skill_confidence_levels():
    """Mention count maps to High / Medium / Low confidence."""
    text = "Python Python Python and some SQL stuff"
    confidence = skill_confidence(text, ["Python", "SQL", "Rust"])
    assert confidence["Python"] == "High"     # 3 mentions
    assert confidence["SQL"] == "Medium"      # 1 mention
    assert confidence["Rust"] == "Low"        # 0 mentions
