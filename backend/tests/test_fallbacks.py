"""Tests for services/fallbacks.py — deterministic suggestions and roadmaps.

These guarantee the AI-failure path produces well-formed output that the
frontend parsers can consume.
"""
from services.fallbacks import resume_suggestions, learning_roadmap, ROLE_SUGGESTIONS


def test_suggestions_use_role_specific_when_available():
    """A known role uses its role-specific suggestion list, not the generic one."""
    out = resume_suggestions("Backend Developer", missing=["FastAPI"])
    assert "TITLE:" in out
    assert "DESCRIPTION:" in out
    # All Backend Developer suggestions should be present
    for s in ROLE_SUGGESTIONS["Backend Developer"]:
        title = s.split("\n")[0].replace("TITLE:", "").strip()
        assert title in out


def test_suggestions_fall_back_to_generic_for_unknown_role():
    """Unknown role should still get a non-empty, well-formed suggestion blob."""
    out = resume_suggestions("Mars Colonist", missing=[])
    assert "TITLE:" in out
    assert "DESCRIPTION:" in out
    assert len(out) > 0


def test_roadmap_uses_role_specific_when_available():
    """Known role pulls from ROLE_ROADMAPS, not the CSV-derived fallback."""
    out = learning_roadmap("Backend Developer", role_data=[], missing=[])
    assert "STEP:" in out
    assert "HOW:" in out


def test_roadmap_falls_back_to_csv_for_unknown_role(sample_role_data):
    """For an unknown role, build the roadmap from the CSV's learning_order column."""
    out = learning_roadmap(
        "Mars Colonist",
        role_data=sample_role_data,
        missing=["FastAPI", "PostgreSQL"],
    )
    # Only missing skills should appear
    assert "FastAPI" in out
    assert "PostgreSQL" in out
    assert "Python" not in out   # not in missing list
