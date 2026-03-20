from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import random
from groq import Groq
import fitz
import docx
from resume_parser import parse_and_score
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔑 Groq client — loads from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ Expanded skill list
ALL_SKILLS = {
    "general": ["Python", "SQL", "Git", "Linux", "APIs", "REST", "JSON", "HTML", "CSS"],
    "cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "Ansible"],
    "backend": ["Node.js", "Express", "Flask", "Django", "FastAPI", "PostgreSQL", "MongoDB", "Redis", "GraphQL"],
    "frontend": ["React", "Vue", "Angular", "JavaScript", "TypeScript", "Tailwind", "Bootstrap", "Webpack"],
    "data": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Matplotlib", "Tableau", "Power BI"],
    "devops": ["GitHub Actions", "CircleCI", "Nginx", "Apache", "Prometheus", "Grafana", "ELK Stack"]
}

# ✅ Role-specific fallback suggestions
ROLE_SUGGESTIONS = {
    "Cloud Engineer": [
        "TITLE: Master AWS Core Services\nDESCRIPTION: Focus on EC2, S3, Lambda, and VPC. Complete the AWS Cloud Practitioner certification as a starting point.",
        "TITLE: Learn Infrastructure as Code\nDESCRIPTION: Practice Terraform by deploying real infrastructure. Start with simple EC2 instances and progress to full VPC setups.",
        "TITLE: Build a CI/CD Pipeline\nDESCRIPTION: Set up a complete pipeline using Jenkins or GitHub Actions. Deploy a sample app automatically on every code push.",
        "TITLE: Container Proficiency\nDESCRIPTION: Learn Docker thoroughly then move to Kubernetes. Deploy a multi-container application using docker-compose.",
        "TITLE: Linux System Administration\nDESCRIPTION: Practice common Linux commands, shell scripting, and system administration tasks on a free EC2 instance."
    ],
    "Backend Developer": [
        "TITLE: Build RESTful APIs\nDESCRIPTION: Create a complete REST API with authentication using Node.js/Express or Python/FastAPI. Include proper error handling.",
        "TITLE: Database Design Skills\nDESCRIPTION: Practice designing normalized database schemas. Learn both SQL (PostgreSQL) and NoSQL (MongoDB) databases.",
        "TITLE: API Security Practices\nDESCRIPTION: Implement JWT authentication, input validation, and rate limiting. Study OWASP Top 10 API security risks.",
        "TITLE: Version Control Mastery\nDESCRIPTION: Practice Git workflows including branching strategies, pull requests, and resolving merge conflicts.",
        "TITLE: Testing Your Code\nDESCRIPTION: Write unit and integration tests for your APIs. Aim for at least 80% code coverage using pytest or Jest."
    ],
    "Data Scientist": [
        "TITLE: Master Pandas and NumPy\nDESCRIPTION: Practice data manipulation with real datasets from Kaggle. Focus on cleaning, transforming, and analyzing data.",
        "TITLE: Build ML Projects\nDESCRIPTION: Complete end-to-end machine learning projects. Start with classification problems using Scikit-learn.",
        "TITLE: Data Visualization Skills\nDESCRIPTION: Create compelling visualizations using Matplotlib, Seaborn, and Tableau. Tell stories with your data.",
        "TITLE: Statistics Foundation\nDESCRIPTION: Strengthen your understanding of statistics, probability, and hypothesis testing which are core to data science.",
        "TITLE: Kaggle Competitions\nDESCRIPTION: Participate in Kaggle competitions to practice real-world data science problems and learn from the community."
    ],
    "Frontend Developer": [
        "TITLE: React Fundamentals\nDESCRIPTION: Master React hooks, state management, and component lifecycle. Build 2-3 complete projects using React.",
        "TITLE: Responsive Design\nDESCRIPTION: Practice building fully responsive layouts using CSS Flexbox, Grid, and Tailwind CSS.",
        "TITLE: JavaScript Deep Dive\nDESCRIPTION: Strengthen your JavaScript fundamentals including async/await, promises, closures, and ES6+ features.",
        "TITLE: Performance Optimization\nDESCRIPTION: Learn techniques like lazy loading, code splitting, and caching to improve web application performance.",
        "TITLE: Build a Portfolio\nDESCRIPTION: Create a professional portfolio website showcasing your projects. This is essential for frontend developers."
    ],
    "DevOps Engineer": [
        "TITLE: CI/CD Pipeline Mastery\nDESCRIPTION: Build complete CI/CD pipelines using GitHub Actions or Jenkins. Automate testing, building, and deployment.",
        "TITLE: Container Orchestration\nDESCRIPTION: Deploy and manage containerized applications using Kubernetes. Practice with Minikube locally first.",
        "TITLE: Infrastructure Automation\nDESCRIPTION: Use Ansible or Terraform to automate infrastructure provisioning. Apply IaC principles to real projects.",
        "TITLE: Monitoring and Alerting\nDESCRIPTION: Set up monitoring using Prometheus and Grafana. Create dashboards and alerts for system health.",
        "TITLE: Security Best Practices\nDESCRIPTION: Learn DevSecOps principles. Implement security scanning in your CI/CD pipeline using tools like SonarQube."
    ]
}

# ✅ Role-specific fallback roadmaps
ROLE_ROADMAPS = {
    "Cloud Engineer": [
        "STEP: Linux Fundamentals\nHOW: Complete the Linux Command Line Basics course on Udemy. Practice daily on a free EC2 instance.",
        "STEP: AWS Core Services\nHOW: Take the AWS Cloud Practitioner course on A Cloud Guru. Focus on EC2, S3, VPC, and IAM.",
        "STEP: Docker Containers\nHOW: Complete Docker's official Get Started tutorial. Build and containerize a simple web application.",
        "STEP: Kubernetes Orchestration\nHOW: Follow the official Kubernetes tutorials. Deploy a multi-container app on a local Minikube cluster.",
        "STEP: Infrastructure as Code\nHOW: Complete HashiCorp's Terraform tutorials. Deploy a full AWS infrastructure using Terraform scripts."
    ],
    "Backend Developer": [
        "STEP: Programming Foundation\nHOW: Strengthen Python or Node.js skills through freeCodeCamp. Build 3 small backend projects.",
        "STEP: Database Mastery\nHOW: Complete SQLZoo for SQL practice. Build a CRUD application with PostgreSQL as the database.",
        "STEP: RESTful API Development\nHOW: Build a complete REST API with authentication using FastAPI or Express. Deploy it on Heroku.",
        "STEP: API Security\nHOW: Implement JWT tokens, input validation, and rate limiting. Study OWASP API Security Top 10.",
        "STEP: Testing and Documentation\nHOW: Write unit and integration tests with pytest or Jest. Document your API using Swagger/OpenAPI."
    ],
    "Data Scientist": [
        "STEP: Python for Data Science\nHOW: Complete Python for Data Science course on Coursera. Focus on Pandas and NumPy libraries.",
        "STEP: Statistics and Mathematics\nHOW: Take Khan Academy's Statistics course. Focus on probability, distributions, and hypothesis testing.",
        "STEP: Machine Learning Basics\nHOW: Complete Andrew Ng's Machine Learning course on Coursera. Implement algorithms from scratch.",
        "STEP: Real Projects on Kaggle\nHOW: Complete 3 Kaggle competitions. Start with Titanic dataset then move to more complex problems.",
        "STEP: Deep Learning\nHOW: Take the Deep Learning Specialization on Coursera. Build neural networks using TensorFlow or PyTorch."
    ],
    "Frontend Developer": [
        "STEP: HTML and CSS Mastery\nHOW: Complete freeCodeCamp's Responsive Web Design certification. Build 5 responsive web pages.",
        "STEP: JavaScript Fundamentals\nHOW: Complete JavaScript.info tutorial completely. Focus on DOM manipulation, events, and async programming.",
        "STEP: React Framework\nHOW: Take the official React tutorial then build a complete Todo app with hooks and state management.",
        "STEP: State Management\nHOW: Learn Redux or Context API for global state. Build a shopping cart application using React.",
        "STEP: Build Your Portfolio\nHOW: Create a professional portfolio with 3-4 projects. Deploy using Netlify or Vercel for free hosting."
    ],
    "DevOps Engineer": [
        "STEP: Linux and Scripting\nHOW: Complete Linux Foundation's Introduction to Linux course. Write bash scripts for common automation tasks.",
        "STEP: Version Control with Git\nHOW: Practice Git branching strategies using Learn Git Branching website. Contribute to open source projects.",
        "STEP: Docker and Containers\nHOW: Complete Docker's official tutorial. Containerize 3 different types of applications.",
        "STEP: CI/CD Implementation\nHOW: Set up a complete GitHub Actions pipeline. Automate testing and deployment for a sample application.",
        "STEP: Kubernetes and Monitoring\nHOW: Deploy applications on Kubernetes using Minikube. Set up Prometheus and Grafana for monitoring."
    ]
}

# 🔹 Rule-based skill extraction (fallback)
def extract_skills(text):
    found = []
    text_lower = text.lower()
    for category_skills in ALL_SKILLS.values():
        for skill in category_skills:
            if skill.lower() in text_lower and skill not in found:
                found.append(skill)
    return found

# 🔹 AI-based skill extraction
def extract_skills_ai(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": """You are a skill extractor.
Your ONLY job is to extract technical skills from the resume text.
Return ONLY a comma-separated list of skills like this:
Python, SQL, Docker, AWS

STRICT RULES:
- No sentences
- No explanations
- No roadmap
- No suggestions
- No extra text whatsoever
- ONLY skill names separated by commas"""},
                {"role": "user", "content": f"Extract only the technical skills from this resume:\n{text}"}
            ]
        )
        skills = response.choices[0].message.content.split(",")
        return [s.strip() for s in skills if s.strip()]

    except Exception as e:
        print("AI error:", e)
        return None

# 🔹 Load CSV
def load_role_data(role):
    data = []
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "skills.csv")

    with open(csv_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["role"] == role:
                data.append(row)

    print("Loaded CSV rows:", data)
    return data

# 🔹 Load quiz questions
def load_quiz_questions(role):
    questions = []
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "questions.csv")

    with open(csv_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["role"] == role:
                questions.append(row)

    if len(questions) > 5:
        questions = random.sample(questions, 5)

    return questions

# 🔹 Roles API
@app.route("/roles", methods=["GET"])
def get_roles():
    roles = set()
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "skills.csv")

    with open(csv_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            roles.add(row["role"])

    return jsonify(sorted(list(roles)))

# 🔹 Gap analysis
def analyze_gap(user_skills, role):
    role_data = load_role_data(role)
    job_skills = [item["skill"] for item in role_data]
    missing = [s for s in job_skills if s not in user_skills]
    return user_skills, missing, role_data

# 🔹 Confidence
def skill_confidence(text, skills):
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

# ✅ Role-specific fallback suggestions
def resume_suggestions(role, missing):
    suggestions = ROLE_SUGGESTIONS.get(role, [
        "TITLE: Build Real Projects\nDESCRIPTION: Create 2-3 projects that demonstrate your skills. Push them to GitHub with clear documentation.",
        "TITLE: Get Certified\nDESCRIPTION: Pursue relevant certifications for your target role. Certifications validate your skills to employers.",
        "TITLE: Strengthen Your Resume\nDESCRIPTION: Add a clear summary, quantify your achievements, and tailor your resume for each application.",
        "TITLE: Network Actively\nDESCRIPTION: Connect with professionals on LinkedIn. Attend meetups and contribute to open source projects.",
        "TITLE: Practice Interview Skills\nDESCRIPTION: Solve problems on LeetCode daily. Practice system design questions for senior roles."
    ])
    return "\n\n".join(suggestions)

# ✅ Role-specific fallback roadmap
def learning_roadmap(role, role_data, missing):
    if role in ROLE_ROADMAPS:
        return "\n\n".join(ROLE_ROADMAPS[role])

    sorted_data = sorted(role_data, key=lambda x: int(x["learning_order"]))
    roadmap = []
    for item in sorted_data:
        if item["skill"] in missing:
            roadmap.append(
                f"STEP: Learn {item['skill']}\n"
                f"HOW: Search for '{item['skill']} tutorial for beginners' on YouTube. "
                f"Complete a free course then build a small project using {item['skill']}."
            )
    return "\n\n".join(roadmap)

# 🔥 AI Suggestions
def generate_ai_suggestions(resume, role, missing, improvements):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": """You are a career advisor. Give exactly 4-5 suggestions.
You MUST use this EXACT format for every suggestion, no exceptions:

TITLE: Write a short 3-5 word title here
DESCRIPTION: Write one detailed paragraph here

Rules:
- TITLE line must start with exactly "TITLE:"
- DESCRIPTION line must start with exactly "DESCRIPTION:"
- Separate each suggestion with one blank line
- No bullets, no numbers, no asterisks, no markdown
- Every suggestion must have both TITLE and DESCRIPTION"""},
                {"role": "user", "content": f"Role: {role}\nResume: {resume}\nMissing skills: {missing}\nResume improvements needed: {improvements}"}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print("AI suggestions error:", e)
        return None

# 🔥 AI Roadmap
def generate_ai_roadmap(resume, role, role_data, missing):
    try:
        context = "\n".join([f"{i['learning_order']}. {i['skill']}" for i in role_data])

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": """You are a learning roadmap generator.
Create a step-by-step roadmap. Each step MUST follow this exact format:

STEP: Skill name only here (no numbers)
HOW: One specific practical way to learn this skill

Separate each step with a blank line.
No bullet points, no asterisks, no markdown, no extra text.
Do NOT include step numbers in the STEP field."""},
                {"role": "user", "content": f"Role: {role}\nResume: {resume}\nSkill order:\n{context}\nMissing skills: {missing}"}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print("AI roadmap error:", e)
        return None

# 🔹 Parse uploaded file
def parse_uploaded_file(file):
    filename = file.filename.lower()
    try:
        if filename.endswith(".pdf"):
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in pdf:
                text += page.get_text()
            if not text.strip():
                return None, "Could not extract text from PDF. Please paste your resume manually."
            return text.strip(), None

        elif filename.endswith(".docx"):
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            if not text.strip():
                return None, "Could not extract text from Word file. Please paste your resume manually."
            return text.strip(), None

        else:
            return None, "Unsupported file type. Please upload a PDF or Word (.docx) file."

    except Exception as e:
        print("File parse error:", e)
        return None, "Failed to read the file. Please paste your resume text manually."

# 🎯 QUIZ ROUTE
@app.route("/quiz", methods=["GET"])
def get_quiz():
    role = request.args.get("role", "")

    if not role:
        return jsonify({"error": "Role is required"}), 400

    try:
        questions = load_quiz_questions(role)
        if not questions:
            return jsonify({"error": f"No questions found for role: {role}"}), 404

        quiz = []
        for q in questions:
            quiz.append({
                "question": q["question"],
                "options": {
                    "A": q["option_a"],
                    "B": q["option_b"],
                    "C": q["option_c"],
                    "D": q["option_d"],
                },
                "correct": q["correct_answer"],
                "explanation": q["explanation"]
            })

        return jsonify({"role": role, "questions": quiz})

    except Exception as e:
        print("Quiz error:", e)
        return jsonify({"error": "Failed to load quiz. Please try again."}), 500

# 🚀 MAIN API
@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("file")
    message = request.form.get("message", "")
    role = request.form.get("role", "")
    roadmap_requested = request.form.get("roadmap_requested", "false") == "true"

    resume_text = ""
    file_error = None
    if file:
        resume_text, file_error = parse_uploaded_file(file)
        if file_error:
            return jsonify({"error": file_error}), 400

    full_text = resume_text + "\n" + message if resume_text else message

    if not full_text.strip():
        return jsonify({"error": "Please upload a resume or type something in the message box."}), 400

    ai_skills = extract_skills_ai(full_text)
    user_skills = ai_skills if ai_skills else extract_skills(full_text)

    present, missing, role_data = analyze_gap(user_skills, role)
    confidence = skill_confidence(full_text, user_skills)

    resume_analysis = parse_and_score(full_text, user_skills)

    ai_suggestions = generate_ai_suggestions(full_text, role, missing, resume_analysis["improvements"])
    suggestions = ai_suggestions if ai_suggestions else resume_suggestions(role, missing)

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
        "ai_used": ai_suggestions is not None
    })

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)