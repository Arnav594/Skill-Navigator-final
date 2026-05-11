"""Rule-based skill extraction, gap analysis, and confidence scoring.

This module owns everything that operates on skills *deterministically* —
the AI-based extraction lives in ai_service. Keep it pure and side-effect
free so tests don't need to mock anything.
"""

# Canonical skill catalog used by the rule-based extractor (fallback path).
ALL_SKILLS = {
    "general":  ["Python", "SQL", "Git", "Linux", "APIs", "REST", "JSON", "HTML", "CSS"],
    "cloud":    ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "Ansible"],
    "backend":  ["Node.js", "Express", "Flask", "Django", "FastAPI", "PostgreSQL", "MongoDB", "Redis", "GraphQL"],
    "frontend": ["React", "Vue", "Angular", "JavaScript", "TypeScript", "Tailwind", "Bootstrap", "Webpack"],
    "data":     ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Matplotlib", "Tableau", "Power BI"],
    "devops":   ["GitHub Actions", "CircleCI", "Nginx", "Apache", "Prometheus", "Grafana", "ELK Stack"],
}


def extract_skills(text: str) -> list[str]:
    """Rule-based skill extraction. Case-insensitive substring match against
    the canonical catalog. Used as fallback when the AI call fails.
    """
    found = []
    text_lower = text.lower()
    for category_skills in ALL_SKILLS.values():
        for skill in category_skills:
            if skill.lower() in text_lower and skill not in found:
                found.append(skill)
    return found


def analyze_gap(user_skills: list[str], role_data: list[dict]) -> tuple[list[str], list[str]]:
    """Compare user_skills against the role's required skills (from CSV).

    Returns (present, missing). `present` is just user_skills passed through
    so callers can use a single tuple unpack — preserves the original API.
    """
    job_skills = [item["skill"] for item in role_data]
    missing = [s for s in job_skills if s not in user_skills]
    return user_skills, missing


def skill_confidence(text: str, skills: list[str]) -> dict[str, str]:
    """Heuristic confidence per skill based on mention frequency in resume."""
    confidence = {}
    for skill in skills:
        count = text.lower().count(skill.lower())
        if count > 1:
            confidence[skill] = "High"
        elif count == 1:
            confidence[skill] = "Medium"
        else:
            confidence[skill] = "Low"
    return confidence
