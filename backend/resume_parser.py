import json
import os
import re

CONTEXT_SIGNALS = {
    "project": 2, "built": 2, "developed": 2, "implemented": 2,
    "designed": 2, "deployed": 2, "created": 2, "architected": 3,
    "led": 3, "managed": 3, "certified": 3, "certification": 3,
    "years": 2, "proficient": 1, "expert": 3, "experience": 1,
}


def load_schema():
    base_dir = os.path.dirname(__file__)
    schema_path = os.path.join(base_dir, "data", "golden_schema.json")
    with open(schema_path, "r") as f:
        return json.load(f)


def check_section(text: str, keywords: list) -> bool:
    """
    FIX: Line-aware detection.
    Only matches if a keyword starts a line (i.e. is a section heading).
    Old code scanned entire text — 'I have experience' falsely triggered EXPERIENCE section.
    """
    lines = [line.strip().lower() for line in text.splitlines()]
    for keyword in keywords:
        kw = keyword.lower().strip()
        for line in lines:
            clean_line = line.rstrip(':').strip()
            if clean_line == kw or clean_line.startswith(kw + " ") or clean_line.startswith(kw + ":"):
                return True
    return False


def check_metrics(text: str) -> bool:
    """
    FIX: Context-aware metric detection.
    Requires a metric (%, $, etc.) near an action verb indicating achievement.
    """
    pattern = (
        r'(increased|reduced|improved|grew|saved|delivered|achieved|'
        r'generated|cut|boosted|optimized|scaled|handled|processed)'
        r'.{0,60}(\d+\s*%|\$\s*\d+|\d+\s*million|\d+\s*thousand|\d+x)'
    )
    return bool(re.search(pattern, text.lower()))


def check_action_verbs(text: str, verbs: list) -> int:
    text_lower = text.lower()
    return sum(1 for v in verbs if v.lower() in text_lower)


def check_quantified(text: str, patterns: list) -> bool:
    text_lower = text.lower()
    return any(p.lower() in text_lower for p in patterns)


def skill_confidence(text: str, skills: list) -> dict:
    """
    FIX: Context-aware confidence.
    Old code counted raw occurrences — mentioning Python twice = High.
    New code checks whether the skill appears near real context signals.
    """
    confidence = {}
    sentences = re.split(r'[.!?\n]', text.lower())
    for skill in skills:
        sk = skill.lower()
        score = 0
        for sent in sentences:
            if sk not in sent:
                continue
            for signal, weight in CONTEXT_SIGNALS.items():
                if signal in sent:
                    score += weight
        if score >= 5:
            confidence[skill] = "High"
        elif score >= 2:
            confidence[skill] = "Medium"
        else:
            confidence[skill] = "Low"
    return confidence


def get_label_and_color(score: int, scoring: dict) -> tuple:
    """
    FIX: Deterministic integer-based label boundaries.
    Old code used float math which caused boundary edge cases.
    """
    if score >= scoring["excellent"]:
        return "Excellent", "green"
    if score >= scoring["good"]:
        return "Good", "yellow"
    if score >= scoring["average"]:
        return "Average", "orange"
    return "Needs Work", "red"


def parse_and_score(resume_text: str, user_skills: list) -> dict:
    schema = load_schema()
    sections = schema["sections"]
    ats_rules = schema["ats_rules"]

    total_score = 0
    max_score = 0
    section_results = {}
    missing_sections = []
    improvements = []

    for section_name, section_data in sections.items():
        weight = section_data["weight"]
        max_score += weight
        keywords = section_data.get("keywords", [])
        found = check_section(resume_text, keywords)   # FIX: line-aware

        if found:
            section_score = weight
            if section_name == "skills":
                min_count = section_data.get("min_count", 6)
                if len(user_skills) < min_count:
                    section_score = weight * 0.5
                    improvements.append(
                        f"Add more skills — you have {len(user_skills)}, aim for at least {min_count}"
                    )
            if section_name == "experience":
                if not check_metrics(resume_text):      # FIX: context-aware
                    section_score = weight * 0.7
                    improvements.append(
                        "Add quantified achievements (e.g. 'Improved API response time by 40%')"
                    )
            total_score += section_score
            section_results[section_name] = {"found": True,  "score": section_score, "max": weight}
        else:
            section_results[section_name] = {"found": False, "score": 0, "max": weight}
            if section_data.get("required", False):
                missing_sections.append(section_name)
                improvements.append(f"Add a '{section_name.upper()}' section to your resume")

    # ATS: action verbs
    verb_weight = ats_rules["action_verbs"]["weight"]
    max_score += verb_weight
    verbs_found = check_action_verbs(resume_text, ats_rules["action_verbs"]["examples"])
    if verbs_found >= 3:
        total_score += verb_weight
    elif verbs_found > 0:
        total_score += verb_weight * 0.5
        improvements.append("Use more action verbs like 'developed', 'led', 'optimized'")
    else:
        improvements.append("Add strong action verbs to describe your experience")

    # ATS: quantified achievements
    quant_weight = ats_rules["quantified_achievements"]["weight"]
    max_score += quant_weight
    if check_quantified(resume_text, ats_rules["quantified_achievements"]["patterns"]):
        total_score += quant_weight
    else:
        improvements.append("Quantify your achievements with numbers and percentages")

    # FIX: integer math — no float boundary surprises
    reliability_score = int((total_score * 100) // max_score) if max_score > 0 else 0
    label, color = get_label_and_color(reliability_score, schema["scoring"])

    return {
        "reliability_score": reliability_score,
        "label": label,
        "color": color,
        "section_results": section_results,
        "missing_sections": missing_sections,
        "improvements": improvements,
    }