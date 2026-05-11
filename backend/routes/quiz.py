"""GET /quiz?role=... — return shuffled MCQs for a role."""
from flask import Blueprint, request, jsonify
from services.data_service import load_quiz_questions

bp = Blueprint("quiz", __name__)


@bp.route("/quiz", methods=["GET"])
def get_quiz():
    role = request.args.get("role", "")

    if not role:
        return jsonify({"error": "Role is required"}), 400

    try:
        questions = load_quiz_questions(role)
        if not questions:
            return jsonify({"error": f"No questions found for role: {role}"}), 404

        quiz = [
            {
                "question": q["question"],
                "options": {
                    "A": q["option_a"],
                    "B": q["option_b"],
                    "C": q["option_c"],
                    "D": q["option_d"],
                },
                "correct": q["correct_answer"],
                "explanation": q["explanation"],
            }
            for q in questions
        ]

        return jsonify({"role": role, "questions": quiz})

    except Exception as e:
        print("Quiz error:", e)
        return jsonify({"error": "Failed to load quiz. Please try again."}), 500
