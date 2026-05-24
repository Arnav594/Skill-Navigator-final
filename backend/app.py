from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import csv
import os
import random
import json
import uuid
from groq import Groq
import fitz
import docx
from dotenv import load_dotenv

# ── New modules ───────────────────────────────────────────────────────────────
from sanitizer import sanitize_resume, sanitize_role, wrap_for_prompt
from skill_normalizer import (
    extract_skills_rule_based,
    normalize_skills_list,
    analyze_gap_normalized,
    normalize_skill,
)
from resume_parser import parse_and_score, skill_confidence
from database import init_db, save_analysis, save_quiz_attempt, get_history, get_quiz_history

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Startup ───────────────────────────────────────────────────────────────────
init_db()

# ── Skill master list ─────────────────────────────────────────────────────────
ALL_SKILLS = {
    "general":  ["Python", "SQL", "Git", "Linux", "APIs", "REST", "JSON", "HTML", "CSS"],
    "cloud":    ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "Ansible"],
    "backend":  ["Node.js", "Express", "Flask", "Django", "FastAPI", "PostgreSQL", "MongoDB", "Redis", "GraphQL"],
    "frontend": ["React", "Vue", "Angular", "JavaScript", "TypeScript", "Tailwind", "Bootstrap", "Webpack"],
    "data":     ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Matplotlib", "Tableau", "Power BI"],
    "devops":   ["GitHub Actions", "CircleCI", "Nginx", "Apache", "Prometheus", "Grafana", "ELK Stack"],
}

# ── Fallback suggestions ──────────────────────────────────────────────────────
ROLE_SUGGESTIONS = {
    "Cloud Engineer": [
        "TITLE: Master AWS Core Services\nDESCRIPTION: Focus on EC2, S3, Lambda, and VPC. Complete the AWS Cloud Practitioner certification as a starting point.",
        "TITLE: Learn Infrastructure as Code\nDESCRIPTION: Practice Terraform by deploying real infrastructure. Start with simple EC2 instances and progress to full VPC setups.",
        "TITLE: Build a CI/CD Pipeline\nDESCRIPTION: Set up a complete pipeline using Jenkins or GitHub Actions. Deploy a sample app automatically on every code push.",
        "TITLE: Container Proficiency\nDESCRIPTION: Learn Docker thoroughly then move to Kubernetes. Deploy a multi-container application using docker-compose.",
        "TITLE: Linux System Administration\nDESCRIPTION: Practice common Linux commands, shell scripting, and system administration tasks on a free EC2 instance.",
    ],
    "Backend Developer": [
        "TITLE: Build RESTful APIs\nDESCRIPTION: Create a complete REST API with authentication using Node.js/Express or Python/FastAPI. Include proper error handling.",
        "TITLE: Database Design Skills\nDESCRIPTION: Practice designing normalized database schemas. Learn both SQL (PostgreSQL) and NoSQL (MongoDB) databases.",
        "TITLE: API Security Practices\nDESCRIPTION: Implement JWT authentication, input validation, and rate limiting. Study OWASP Top 10 API security risks.",
        "TITLE: Version Control Mastery\nDESCRIPTION: Practice Git workflows including branching strategies, pull requests, and resolving merge conflicts.",
        "TITLE: Testing Your Code\nDESCRIPTION: Write unit and integration tests for your APIs. Aim for at least 80% code coverage using pytest or Jest.",
    ],
    "Data Scientist": [
        "TITLE: Master Pandas and NumPy\nDESCRIPTION: Practice data manipulation with real datasets from Kaggle. Focus on cleaning, transforming, and analyzing data.",
        "TITLE: Build ML Projects\nDESCRIPTION: Complete end-to-end machine learning projects. Start with classification problems using Scikit-learn.",
        "TITLE: Data Visualization Skills\nDESCRIPTION: Create compelling visualizations using Matplotlib, Seaborn, and Tableau. Tell stories with your data.",
        "TITLE: Statistics Foundation\nDESCRIPTION: Strengthen your understanding of statistics, probability, and hypothesis testing which are core to data science.",
        "TITLE: Kaggle Competitions\nDESCRIPTION: Participate in Kaggle competitions to practice real-world data science problems and learn from the community.",
    ],
    "Frontend Developer": [
        "TITLE: React Fundamentals\nDESCRIPTION: Master React hooks, state management, and component lifecycle. Build 2-3 complete projects using React.",
        "TITLE: Responsive Design\nDESCRIPTION: Practice building fully responsive layouts using CSS Flexbox, Grid, and Tailwind CSS.",
        "TITLE: JavaScript Deep Dive\nDESCRIPTION: Strengthen your JavaScript fundamentals including async/await, promises, closures, and ES6+ features.",
        "TITLE: Performance Optimization\nDESCRIPTION: Learn techniques like lazy loading, code splitting, and caching to improve web application performance.",
        "TITLE: Build a Portfolio\nDESCRIPTION: Create a professional portfolio website showcasing your projects. This is essential for frontend developers.",
    ],
    "DevOps Engineer": [
        "TITLE: CI/CD Pipeline Mastery\nDESCRIPTION: Build complete CI/CD pipelines using GitHub Actions or Jenkins. Automate testing, building, and deployment.",
        "TITLE: Container Orchestration\nDESCRIPTION: Deploy and manage containerized applications using Kubernetes. Practice with Minikube locally first.",
        "TITLE: Infrastructure Automation\nDESCRIPTION: Use Ansible or Terraform to automate infrastructure provisioning. Apply IaC principles to real projects.",
        "TITLE: Monitoring and Alerting\nDESCRIPTION: Set up monitoring using Prometheus and Grafana. Create dashboards and alerts for system health.",
        "TITLE: Security Best Practices\nDESCRIPTION: Learn DevSecOps principles. Implement security scanning in your CI/CD pipeline using tools like SonarQube.",
    ],
}

# ── Fallback roadmaps ─────────────────────────────────────────────────────────
ROLE_ROADMAPS = {
    "Cloud Engineer": [
        "STEP: Linux Fundamentals\nHOW: Complete the Linux Command Line Basics course on Udemy. Practice daily on a free EC2 instance.",
        "STEP: AWS Core Services\nHOW: Take the AWS Cloud Practitioner course on A Cloud Guru. Focus on EC2, S3, VPC, and IAM.",
        "STEP: Docker Containers\nHOW: Complete Docker's official Get Started tutorial at docs.docker.com/get-started.",
        "STEP: Kubernetes Orchestration\nHOW: Follow the official Kubernetes tutorials at kubernetes.io/docs/tutorials.",
        "STEP: Infrastructure as Code\nHOW: Complete HashiCorp's Terraform tutorials at developer.hashicorp.com/terraform/tutorials.",
    ],
    "Backend Developer": [
        "STEP: Programming Foundation\nHOW: Strengthen Python or Node.js skills through freeCodeCamp.org. Build 3 small backend projects.",
        "STEP: Database Mastery\nHOW: Complete SQLZoo.net for SQL practice. Build a CRUD application with PostgreSQL.",
        "STEP: RESTful API Development\nHOW: Build a complete REST API with JWT auth using FastAPI. Deploy it on Render.",
        "STEP: API Security\nHOW: Implement JWT tokens, input validation, and rate limiting. Study OWASP API Security Top 10 at owasp.org.",
        "STEP: Testing and Documentation\nHOW: Write unit and integration tests with pytest or Jest. Document your API using Swagger/OpenAPI.",
    ],
    "Data Scientist": [
        "STEP: Python for Data Science\nHOW: Complete Python for Data Science course on Coursera. Focus on Pandas and NumPy.",
        "STEP: Statistics and Mathematics\nHOW: Take Khan Academy's Statistics course at khanacademy.org.",
        "STEP: Machine Learning Basics\nHOW: Complete Andrew Ng's Machine Learning Specialization on Coursera.",
        "STEP: Real Projects on Kaggle\nHOW: Complete 3 Kaggle competitions at kaggle.com.",
        "STEP: Deep Learning\nHOW: Take the Deep Learning Specialization on Coursera at deeplearning.ai.",
    ],
    "Frontend Developer": [
        "STEP: HTML and CSS Mastery\nHOW: Complete freeCodeCamp's Responsive Web Design certification at freecodecamp.org.",
        "STEP: JavaScript Fundamentals\nHOW: Complete javascript.info tutorial completely.",
        "STEP: React Framework\nHOW: Take the official React tutorial at react.dev then build a complete Todo app.",
        "STEP: State Management\nHOW: Learn Redux or Context API for global state. Build a shopping cart application.",
        "STEP: Build Your Portfolio\nHOW: Create a professional portfolio with 3-4 projects. Deploy using Netlify or Vercel.",
    ],
    "DevOps Engineer": [
        "STEP: Linux and Scripting\nHOW: Complete Linux Foundation's Introduction to Linux at training.linuxfoundation.org.",
        "STEP: Version Control with Git\nHOW: Practice Git branching at learngitbranching.js.org.",
        "STEP: Docker and Containers\nHOW: Complete Docker's official tutorial at docs.docker.com.",
        "STEP: CI/CD Implementation\nHOW: Set up a complete GitHub Actions pipeline for a sample application.",
        "STEP: Kubernetes and Monitoring\nHOW: Deploy on Kubernetes using Minikube. Set up Prometheus and Grafana.",
    ],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_role_data(role: str) -> list:
    data = []
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "skills.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["role"] == role:
                data.append(row)
    return data


def load_quiz_questions(role: str) -> list:
    questions = []
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "questions.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["role"] == role:
                questions.append(row)
    if len(questions) > 5:
        questions = random.sample(questions, 5)
    return questions


def get_or_create_session(request) -> str:
    sid = request.cookies.get("sid")
    if not sid:
        sid = str(uuid.uuid4())
    return sid


def parse_uploaded_file(file):
    filename = file.filename.lower()
    try:
        if filename.endswith(".pdf"):
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            text = "".join(page.get_text() for page in pdf)
            if not text.strip():
                return None, "Could not extract text from PDF. Please paste your resume manually."
            return text.strip(), None
        elif filename.endswith(".docx"):
            doc = docx.Document(file)
            text = "\n".join(para.text for para in doc.paragraphs)
            if not text.strip():
                return None, "Could not extract text from Word file. Please paste your resume manually."
            return text.strip(), None
        else:
            return None, "Unsupported file type. Please upload a PDF or Word (.docx) file."
    except Exception as e:
        print("File parse error:", e)
        return None, "Failed to read the file. Please paste your resume text manually."


# ── AI functions ──────────────────────────────────────────────────────────────

def extract_skills_ai(text: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a skill extractor.\n"
                        "Extract ONLY technical skills from the resume inside <resume> tags.\n"
                        "Return ONLY a comma-separated list. No sentences, no explanations.\n"
                        "Example output: Python, SQL, Docker, AWS"
                    ),
                },
                {
                    "role": "user",
                    "content": wrap_for_prompt(text),
                },
            ],
        )
        raw = response.choices[0].message.content
        skills = [s.strip() for s in raw.split(",") if s.strip()]
        return normalize_skills_list(skills) if skills else None
    except Exception as e:
        print("AI skill extraction error:", e)
        return None


def generate_ai_suggestions(resume: str, role: str, missing: list, improvements: list):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a career advisor. Give exactly 4-5 suggestions.\n"
                        "EXACT format required:\n\n"
                        "TITLE: Write a short 3-5 word title here\n"
                        "DESCRIPTION: Write one detailed paragraph here\n\n"
                        "Rules:\n"
                        "- TITLE line must start with exactly 'TITLE:'\n"
                        "- DESCRIPTION line must start with exactly 'DESCRIPTION:'\n"
                        "- Separate each suggestion with one blank line\n"
                        "- No bullets, no numbers, no asterisks, no markdown"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Role: {role}\n"
                        f"{wrap_for_prompt(resume)}\n"
                        f"Missing skills: {', '.join(missing)}\n"
                        f"Resume improvements needed: {'; '.join(improvements)}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print("AI suggestions error:", e)
        return None


def generate_ai_roadmap(resume: str, role: str, role_data: list, missing: list):
    try:
        context = "\n".join(f"{i['learning_order']}. {i['skill']}" for i in role_data)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a learning roadmap generator.\n"
                        "Each step MUST follow this exact format:\n\n"
                        "STEP: Skill name only here\n"
                        "HOW: One specific practical way to learn this skill with a real URL\n\n"
                        "Separate each step with a blank line.\n"
                        "No bullet points, no asterisks, no markdown."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Role: {role}\n"
                        f"{wrap_for_prompt(resume)}\n"
                        f"Skill order:\n{context}\n"
                        f"Missing skills: {', '.join(missing)}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print("AI roadmap error:", e)
        return None


def resume_suggestions_fallback(role: str, missing: list) -> str:
    suggestions = ROLE_SUGGESTIONS.get(role, [
        "TITLE: Build Real Projects\nDESCRIPTION: Create 2-3 projects that demonstrate your skills. Push them to GitHub.",
        "TITLE: Get Certified\nDESCRIPTION: Pursue relevant certifications for your target role.",
        "TITLE: Strengthen Your Resume\nDESCRIPTION: Add a clear summary, quantify achievements, and tailor for each application.",
        "TITLE: Network Actively\nDESCRIPTION: Connect with professionals on LinkedIn. Attend meetups and contribute to open source.",
        "TITLE: Practice Interview Skills\nDESCRIPTION: Solve problems on LeetCode daily. Practice system design questions.",
    ])
    return "\n\n".join(suggestions)


def learning_roadmap_fallback(role: str, role_data: list, missing: list) -> str:
    if role in ROLE_ROADMAPS:
        return "\n\n".join(ROLE_ROADMAPS[role])
    sorted_data = sorted(role_data, key=lambda x: int(x["learning_order"]))
    roadmap = [
        f"STEP: Learn {item['skill']}\n"
        f"HOW: Search for '{item['skill']} tutorial for beginners' on YouTube."
        for item in sorted_data if item["skill"] in missing
    ]
    return "\n\n".join(roadmap)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/roles", methods=["GET"])
def get_roles():
    roles = set()
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "skills.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            roles.add(row["role"])
    return jsonify(sorted(list(roles)))


@app.route("/quiz", methods=["GET"])
def get_quiz():
    role = sanitize_role(request.args.get("role", ""))
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
                    "A": q["option_a"], "B": q["option_b"],
                    "C": q["option_c"], "D": q["option_d"],
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


@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json() or {}
    session_id = get_or_create_session(request)
    role = sanitize_role(data.get("role", ""))
    score = int(data.get("score", 0))
    total = int(data.get("total", 5))
    answers = data.get("answers", {})
    if not role:
        return jsonify({"error": "Role is required"}), 400
    row_id = save_quiz_attempt(session_id, role, score, total, answers)
    resp = make_response(jsonify({"saved": True, "id": row_id}))
    resp.set_cookie("sid", session_id, max_age=60 * 60 * 24 * 30, samesite="Lax")
    return resp


@app.route("/history", methods=["GET"])
def history():
    session_id = request.cookies.get("sid", "")
    if not session_id:
        return jsonify({"analyses": [], "quizzes": []})
    return jsonify({
        "analyses": get_history(session_id),
        "quizzes":  get_quiz_history(session_id),
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    session_id = get_or_create_session(request)

    file              = request.files.get("file")
    message           = request.form.get("message", "")
    role              = sanitize_role(request.form.get("role", ""))
    roadmap_requested = request.form.get("roadmap_requested", "false") == "true"

    # Parse uploaded file
    resume_text = ""
    if file:
        resume_text, file_error = parse_uploaded_file(file)
        if file_error:
            return jsonify({"error": file_error}), 400

    # Priority 1: sanitize ALL inputs
    resume_text = sanitize_resume(resume_text)
    message     = sanitize_resume(message)
    full_text   = (resume_text + "\n" + message).strip()

    if not full_text:
        return jsonify({"error": "Please upload a resume or type something in the message box."}), 400

    # Priority 2: normalized skill extraction
    ai_skills  = extract_skills_ai(full_text)
    raw_skills = ai_skills if ai_skills else extract_skills_rule_based(full_text, ALL_SKILLS)
    user_skills = normalize_skills_list(raw_skills)

    # Gap analysis using normalized matching
    role_data = load_role_data(role)
    present, missing = analyze_gap_normalized(user_skills, role_data)

    # Context-aware confidence
    confidence = skill_confidence(full_text, user_skills)

    # Priority 3: line-aware resume scoring
    resume_analysis = parse_and_score(full_text, user_skills)

    # Match score
    total_skills = len(present) + len(missing)
    match_score  = round((len(present) / total_skills) * 100) if total_skills > 0 else 0

    # AI suggestions and roadmap
    ai_suggestions = generate_ai_suggestions(full_text, role, missing, resume_analysis["improvements"])
    suggestions    = ai_suggestions or resume_suggestions_fallback(role, missing)

    ai_roadmap = generate_ai_roadmap(full_text, role, role_data, missing)
    roadmap    = ai_roadmap or learning_roadmap_fallback(role, role_data, missing)

    # Priority 4: persist to database
    save_analysis(
        session_id=session_id,
        role=role,
        skills=present,
        missing=missing,
        match_score=match_score,
        reliability_score=resume_analysis["reliability_score"],
        label=resume_analysis["label"],
        improvements=resume_analysis["improvements"],
        ai_used=ai_suggestions is not None,
    )

    resp = make_response(jsonify({
        "skills":            present,
        "confidence":        confidence,
        "missing":           missing,
        "suggestions":       suggestions,
        "roadmap":           roadmap,
        "roadmap_requested": roadmap_requested,
        "reliability_score": resume_analysis["reliability_score"],
        "reliability_label": resume_analysis["label"],
        "reliability_color": resume_analysis["color"],
        "missing_sections":  resume_analysis["missing_sections"],
        "improvements":      resume_analysis["improvements"],
        "ai_used":           ai_suggestions is not None,
        "match_score":       match_score,
    }))
    resp.set_cookie("sid", session_id, max_age=60 * 60 * 24 * 30, samesite="Lax")
    return resp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)