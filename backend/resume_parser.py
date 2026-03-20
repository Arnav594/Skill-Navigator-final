import json
import os
import re

# 🔹 Load golden schema
def load_schema():
    base_dir = os.path.dirname(__file__)
    schema_path = os.path.join(base_dir, "data", "golden_schema.json")
    with open(schema_path, "r") as f:
        return json.load(f)

# 🔹 Check if a section exists in resume text
def check_section(text, keywords):
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

# 🔹 Count skills in resume
def count_skills(text, skills_list):
    text_lower = text.lower()
    found = [s for s in skills_list if s.lower() in text_lower]
    return len(found)

# 🔹 Check for action verbs
def check_action_verbs(text, verbs):
    text_lower = text.lower()
    found = [v for v in verbs if v.lower() in text_lower]
    return len(found)

# 🔹 Check for quantified achievements
def check_quantified(text, patterns):
    text_lower = text.lower()
    return any(p.lower() in text_lower for p in patterns)

# 🔹 Check for metrics (numbers + %)
def check_metrics(text):
    return bool(re.search(r'\d+%|\d+ percent|\$\d+|\d+ million|\d+ thousand', text.lower()))

# 🔹 MAIN PARSER — compares resume against golden schema
def parse_and_score(resume_text, user_skills):
    schema = load_schema()
    sections = schema["sections"]
    ats_rules = schema["ats_rules"]

    total_score = 0
    max_score = 0
    section_results = {}
    missing_sections = []
    improvements = []

    # 🔸 Score each section
    for section_name, section_data in sections.items():
        weight = section_data["weight"]
        max_score += weight
        keywords = section_data.get("keywords", [])
        found = check_section(resume_text, keywords)

        if found:
            section_score = weight

            # Extra check for skills count
            if section_name == "skills":
                min_count = section_data.get("min_count", 6)
                if len(user_skills) < min_count:
                    section_score = weight * 0.5
                    improvements.append(f"Add more skills — you have {len(user_skills)}, aim for at least {min_count}")

            # Extra check for experience metrics
            if section_name == "experience":
                if not check_metrics(resume_text):
                    section_score = weight * 0.7
                    improvements.append("Add quantified achievements in experience (e.g. 'Improved performance by 30%')")

            total_score += section_score
            section_results[section_name] = {
                "found": True,
                "score": section_score,
                "max": weight
            }
        else:
            section_results[section_name] = {
                "found": False,
                "score": 0,
                "max": weight
            }
            if section_data.get("required", False):
                missing_sections.append(section_name)
                improvements.append(f"Add a '{section_name.upper()}' section to your resume")

    # 🔸 Score ATS rules
    # Action verbs
    action_verbs = ats_rules["action_verbs"]["examples"]
    verb_weight = ats_rules["action_verbs"]["weight"]
    max_score += verb_weight
    verbs_found = check_action_verbs(resume_text, action_verbs)
    if verbs_found >= 3:
        total_score += verb_weight
    elif verbs_found > 0:
        total_score += verb_weight * 0.5
        improvements.append("Use more action verbs like 'developed', 'led', 'optimized'")
    else:
        improvements.append("Add strong action verbs to describe your experience")

    # Quantified achievements
    quant_weight = ats_rules["quantified_achievements"]["weight"]
    max_score += quant_weight
    quant_patterns = ats_rules["quantified_achievements"]["patterns"]
    if check_quantified(resume_text, quant_patterns):
        total_score += quant_weight
    else:
        improvements.append("Quantify your achievements with numbers and percentages")

    # 🔸 Calculate final reliability score
    reliability_score = round((total_score / max_score) * 100) if max_score > 0 else 0

    # 🔸 Score label
    scoring = schema["scoring"]
    if reliability_score >= scoring["excellent"]:
        label = "Excellent"
        color = "green"
    elif reliability_score >= scoring["good"]:
        label = "Good"
        color = "yellow"
    elif reliability_score >= scoring["average"]:
        label = "Average"
        color = "orange"
    else:
        label = "Needs Work"
        color = "red"

    return {
        "reliability_score": reliability_score,
        "label": label,
        "color": color,
        "section_results": section_results,
        "missing_sections": missing_sections,
        "improvements": improvements
    }