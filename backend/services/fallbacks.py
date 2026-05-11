"""Deterministic fallbacks for when the AI calls fail.

The strings here intentionally match the exact format the frontend parser
expects (TITLE:/DESCRIPTION: blocks and STEP:/HOW: blocks). If you change
this format, also update the parsers in frontend/src/components/Suggestions.jsx
and frontend/src/components/Roadmap.jsx.
"""

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


ROLE_ROADMAPS = {
    "Cloud Engineer": [
        "STEP: Linux Fundamentals\nHOW: Complete the Linux Command Line Basics course on Udemy. Practice daily on a free EC2 instance.",
        "STEP: AWS Core Services\nHOW: Take the AWS Cloud Practitioner course on A Cloud Guru. Focus on EC2, S3, VPC, and IAM.",
        "STEP: Docker Containers\nHOW: Complete Docker's official Get Started tutorial. Build and containerize a simple web application.",
        "STEP: Kubernetes Orchestration\nHOW: Follow the official Kubernetes tutorials. Deploy a multi-container app on a local Minikube cluster.",
        "STEP: Infrastructure as Code\nHOW: Complete HashiCorp's Terraform tutorials. Deploy a full AWS infrastructure using Terraform scripts.",
    ],
    "Backend Developer": [
        "STEP: Programming Foundation\nHOW: Strengthen Python or Node.js skills through freeCodeCamp. Build 3 small backend projects.",
        "STEP: Database Mastery\nHOW: Complete SQLZoo for SQL practice. Build a CRUD application with PostgreSQL as the database.",
        "STEP: RESTful API Development\nHOW: Build a complete REST API with authentication using FastAPI or Express. Deploy it on Heroku.",
        "STEP: API Security\nHOW: Implement JWT tokens, input validation, and rate limiting. Study OWASP API Security Top 10.",
        "STEP: Testing and Documentation\nHOW: Write unit and integration tests with pytest or Jest. Document your API using Swagger/OpenAPI.",
    ],
    "Data Scientist": [
        "STEP: Python for Data Science\nHOW: Complete Python for Data Science course on Coursera. Focus on Pandas and NumPy libraries.",
        "STEP: Statistics and Mathematics\nHOW: Take Khan Academy's Statistics course. Focus on probability, distributions, and hypothesis testing.",
        "STEP: Machine Learning Basics\nHOW: Complete Andrew Ng's Machine Learning course on Coursera. Implement algorithms from scratch.",
        "STEP: Real Projects on Kaggle\nHOW: Complete 3 Kaggle competitions. Start with Titanic dataset then move to more complex problems.",
        "STEP: Deep Learning\nHOW: Take the Deep Learning Specialization on Coursera. Build neural networks using TensorFlow or PyTorch.",
    ],
    "Frontend Developer": [
        "STEP: HTML and CSS Mastery\nHOW: Complete freeCodeCamp's Responsive Web Design certification. Build 5 responsive web pages.",
        "STEP: JavaScript Fundamentals\nHOW: Complete JavaScript.info tutorial completely. Focus on DOM manipulation, events, and async programming.",
        "STEP: React Framework\nHOW: Take the official React tutorial then build a complete Todo app with hooks and state management.",
        "STEP: State Management\nHOW: Learn Redux or Context API for global state. Build a shopping cart application using React.",
        "STEP: Build Your Portfolio\nHOW: Create a professional portfolio with 3-4 projects. Deploy using Netlify or Vercel for free hosting.",
    ],
    "DevOps Engineer": [
        "STEP: Linux and Scripting\nHOW: Complete Linux Foundation's Introduction to Linux course. Write bash scripts for common automation tasks.",
        "STEP: Version Control with Git\nHOW: Practice Git branching strategies using Learn Git Branching website. Contribute to open source projects.",
        "STEP: Docker and Containers\nHOW: Complete Docker's official tutorial. Containerize 3 different types of applications.",
        "STEP: CI/CD Implementation\nHOW: Set up a complete GitHub Actions pipeline. Automate testing and deployment for a sample application.",
        "STEP: Kubernetes and Monitoring\nHOW: Deploy applications on Kubernetes using Minikube. Set up Prometheus and Grafana for monitoring.",
    ],
}


_GENERIC_SUGGESTIONS = [
    "TITLE: Build Real Projects\nDESCRIPTION: Create 2-3 projects that demonstrate your skills. Push them to GitHub with clear documentation.",
    "TITLE: Get Certified\nDESCRIPTION: Pursue relevant certifications for your target role. Certifications validate your skills to employers.",
    "TITLE: Strengthen Your Resume\nDESCRIPTION: Add a clear summary, quantify your achievements, and tailor your resume for each application.",
    "TITLE: Network Actively\nDESCRIPTION: Connect with professionals on LinkedIn. Attend meetups and contribute to open source projects.",
    "TITLE: Practice Interview Skills\nDESCRIPTION: Solve problems on LeetCode daily. Practice system design questions for senior roles.",
]


def resume_suggestions(role: str, missing: list[str]) -> str:
    """Deterministic fallback when the AI suggestions call fails."""
    suggestions = ROLE_SUGGESTIONS.get(role, _GENERIC_SUGGESTIONS)
    return "\n\n".join(suggestions)


def learning_roadmap(role: str, role_data: list[dict], missing: list[str]) -> str:
    """Deterministic fallback roadmap. Uses ROLE_ROADMAPS if available,
    otherwise builds one from the CSV's learning_order column.
    """
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
