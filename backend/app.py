import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 Configure Gemini API
genai.configure(api_key="AIzaSyAoMaG4tOVNFhbvBB9eaTJpA9HIdy6dWmI")  # ⚠️ Replace with your key

# Predefined skills
ALL_SKILLS = ["Python", "SQL", "AWS", "Docker", "Kubernetes", "Linux", "APIs", "Node.js"]

# Job roles
JOB_SKILLS = {
    "Cloud Engineer": ["AWS", "Docker", "Kubernetes", "Linux"],
    "Backend Developer": ["Python", "SQL", "APIs", "Node.js"]
}

# 🔹 Rule-based skill extraction (fallback)
def extract_skills(text):
    found = []
    for skill in ALL_SKILLS:
        if skill.lower() in text.lower():
            found.append(skill)
    return found

# 🔹 AI-based skill extraction (Gemini)
def extract_skills_ai(text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        prompt = f"""
        Extract technical skills from the following resume text.
        Return ONLY a comma-separated list of skills.

        Text:
        {text}
        """

        response = model.generate_content(prompt)
        skills = response.text.split(",")

        return [s.strip() for s in skills if s.strip()]

    except Exception as e:
        print("AI error:", e)
        return None

# Confidence score
def skill_confidence(text, skills):
    confidence = {}
    for skill in skills:
        count = text.lower().count(skill.lower())
    if count > 1:
        confidence[skill] = "High - Assumed"
    elif count == 1:
        confidence[skill] = "Medium - Assumed"
    else:
        confidence[skill] = "Low - Assumed"
    return confidence

# Gap analysis
def analyze_gap(user_skills, role):
    job_skills = JOB_SKILLS.get(role, [])
    missing = [s for s in job_skills if s not in user_skills]
    return user_skills, missing

# Resume suggestions
def resume_suggestions(missing_skills):
    return [f"Add a project or experience related to {s}" for s in missing_skills]

# Learning roadmap
def learning_roadmap(missing_skills):
    return [f"Learn basics of {s} (2-3 days)" for s in missing_skills]

# 🚀 API route
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    resume = data.get("resume", "")
    role = data.get("role", "")

    # 🔥 Try AI first, fallback if needed
    ai_skills = extract_skills_ai(resume)

    if ai_skills:
        user_skills = ai_skills
    else:
        user_skills = extract_skills(resume)

    confidence = skill_confidence(resume, user_skills)
    present, missing = analyze_gap(user_skills, role)

    suggestions = resume_suggestions(missing)
    roadmap = learning_roadmap(missing)

    return jsonify({
        "skills": present,
        "confidence": confidence,
        "missing": missing,
        "suggestions": suggestions,
        "roadmap": roadmap
    })

if __name__ == "__main__":
    app.run(debug=True)