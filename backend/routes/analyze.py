"""POST /analyze — main entry point. Orchestrates file parsing, skill
extraction, gap analysis, resume scoring, suggestions, and roadmap.

Logic is unchanged from the original app.py — only restructured to
call into the services/ layer.
"""
from flask import Blueprint, request, jsonify

from resume_parser import parse_and_score
from services.file_service import parse_uploaded_file
from services.skill_service import extract_skills, analyze_gap, skill_confidence
from services.data_service import load_role_data
from services.ai_service import (
    extract_skills_ai,
    generate_ai_suggestions,
    generate_ai_roadmap,
)
from services.fallbacks import resume_suggestions, learning_roadmap

bp = Blueprint("analyze", __name__)


@bp.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("file")
    message = request.form.get("message", "")
    role = request.form.get("role", "")
    roadmap_requested = request.form.get("roadmap_requested", "false") == "true"

    # --- 1. Parse uploaded file if present ---
    resume_text = ""
    if file:
        resume_text, file_error = parse_uploaded_file(file)
        if file_error:
            return jsonify({"error": file_error}), 400

    full_text = (resume_text + "\n" + message) if resume_text else message
    if not full_text.strip():
        return jsonify({"error": "Please upload a resume or type something in the message box."}), 400

    # --- 2. Extract skills (AI primary, rule-based fallback) ---
    ai_skills = extract_skills_ai(full_text)
    user_skills = ai_skills if ai_skills else extract_skills(full_text)

    # --- 3. Gap analysis ---
    role_data = load_role_data(role)
    present, missing = analyze_gap(user_skills, role_data)
    confidence = skill_confidence(full_text, user_skills)

    # --- 4. Resume reliability scoring ---
    resume_analysis = parse_and_score(full_text, user_skills)

    # --- 5. AI suggestions (with fallback) ---
    ai_suggestions = generate_ai_suggestions(full_text, role, missing, resume_analysis["improvements"])
    suggestions = ai_suggestions if ai_suggestions else resume_suggestions(role, missing)

    # --- 6. AI roadmap (with fallback) ---
    ai_roadmap = generate_ai_roadmap(full_text, role, role_data, missing)
    roadmap = ai_roadmap if ai_roadmap else learning_roadmap(role, role_data, missing)

    return jsonify({
        "skills": present,
        "confidence": confidence,
        "missing": missing,
        "suggestions": suggestions,
        "roadmap": roadmap,
        "roadmap_requested": roadmap_requested,
        "reliability_score": resume_analysis["reliability_score"],
        "reliability_label": resume_analysis["label"],
        "reliability_color": resume_analysis["color"],
        "missing_sections": resume_analysis["missing_sections"],
        "improvements": resume_analysis["improvements"],
        "ai_used": ai_suggestions is not None,
    })
