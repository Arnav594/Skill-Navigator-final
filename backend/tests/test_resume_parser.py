"""Tests for resume_parser.py — the golden-schema reliability scorer.

These test the scoring math itself, which the original test suite did not.
We assert score bounds, label/color contract, and improvement-message logic.
"""
from resume_parser import parse_and_score


def test_score_is_within_bounds(sample_resume):
    """Reliability score must always be a 0-100 integer percentage."""
    result = parse_and_score(sample_resume, ["Python", "SQL", "Docker", "AWS"])
    assert 0 <= result["reliability_score"] <= 100
    assert isinstance(result["reliability_score"], int)


def test_score_has_label_and_color(sample_resume):
    """Every result must expose label and color so the UI can render the badge."""
    result = parse_and_score(sample_resume, ["Python"])
    assert result["label"] in {"Excellent", "Good", "Average", "Needs Work"}
    assert result["color"] in {"green", "yellow", "orange", "red"}


def test_empty_resume_scores_low():
    """An empty resume should score poorly and flag missing sections."""
    result = parse_and_score("", [])
    assert result["reliability_score"] < 50
    assert len(result["missing_sections"]) > 0


def test_quantified_metrics_detection(sample_resume):
    """Resume with '40%' should pass the quantified-achievements check
    (so 'Quantify your achievements' should NOT appear in improvements).
    """
    result = parse_and_score(sample_resume, ["Python", "SQL"])
    quant_msg = "Quantify your achievements with numbers and percentages"
    assert quant_msg not in result["improvements"]


def test_low_skill_count_triggers_improvement_message():
    """Fewer than the schema's min_count skills should produce a 'add more skills' nudge."""
    minimal_resume = "EXPERIENCE: Worked at a company. SKILLS: Python. EDUCATION: B.Tech"
    result = parse_and_score(minimal_resume, ["Python"])
    has_skill_nudge = any("skills" in imp.lower() for imp in result["improvements"])
    assert has_skill_nudge
