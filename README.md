# Skill Navigator V2

An AI-powered career navigation platform that analyzes resumes, identifies skill gaps, and provides personalized learning roadmaps for job seekers.

---

## Candidate Name
Arnav Uniyal

## Scenario Chosen
Skill-Bridge Career Navigator (Scenario 2)

## Estimated Time Spent
6 hours

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Run Commands

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Test Commands
```bash
cd backend
pytest test_app.py -v
```

---

## AI Disclosure

**Did you use an AI assistant (Copilot, ChatGPT, etc.)?**
Yes. Claude (Anthropic) was used for development guidance throughout the project. Groq API (LLaMA 3.1 8b) was used as the AI engine powering the application features.

**How did you verify the suggestions?**
Every suggestion was tested manually in the browser and terminal before being kept. Each feature was verified end-to-end including the happy path and edge cases. AI-generated code was reviewed line by line to ensure correctness and alignment with the project requirements.

**Give one example of a suggestion you rejected or changed:**
Claude initially suggested implementing RAG (Retrieval-Augmented Generation) using ChromaDB and sentence-transformers for the roadmap and suggestions feature. I rejected this approach because it was overly complex for the 4-6 hour project scope and introduced unnecessary dependencies. Instead, I used direct Groq API calls with carefully structured prompts, which achieved the same quality of output more efficiently and with less setup overhead.

---

## Tradeoffs & Prioritization

**What did you cut to stay within the 4-6 hour limit?**
- OCR support for image-based resume uploads was cut because Tesseract installation on Windows added significant setup complexity
- User authentication and session management were not implemented as they were outside the core scope
- Production deployment was skipped to prioritize functionality and testing within the time limit

**What would you build next if you had more time?**
- Implement RAG using ChromaDB for more semantically accurate skill matching against job descriptions
- Add OCR support for image resumes using Tesseract
- Deploy frontend on Vercel and backend on Render for a live demo
- Add user accounts to save analysis history and track skill improvement over time
- Expand the quiz database with more roles and dynamically AI-generated questions
- Implement a full mock interview feature with voice input and AI evaluation

**Known limitations:**
- Groq free tier has rate limits which may slow responses under heavy usage
- Skill extraction accuracy depends on LLaMA following strict prompt formatting
- Resume reliability score is based on keyword detection rather than semantic understanding
- Quiz questions are static and CSV-based rather than dynamically generated per user
- Image resume uploads are not supported in the current version

---

## Project Structure
```
SKILL NAVIGATOR V2/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── resume_parser.py       # Golden schema resume scorer
│   ├── test_app.py            # pytest tests
│   ├── .env                   # API keys (not committed)
│   ├── .env.example           # Template for API keys
│   └── data/
│       ├── skills.csv         # Role-skill mapping dataset
│       ├── questions.csv      # Quiz questions dataset
│       └── golden_schema.json # ATS benchmark schema
├── frontend/
│   └── src/
│       └── App.jsx            # Main React component
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite) |
| Backend | Python Flask |
| AI Provider | Groq API (LLaMA 3.1 8b) |
| File Parsing | PyMuPDF, python-docx |
| Testing | pytest |
| Data | CSV and JSON synthetic datasets |

---

## Features

- Resume Upload — Supports PDF and Word (.docx) files
- AI Skill Extraction — Extracts technical skills using LLaMA 3.1 with rule-based fallback
- Skill Match Score — Shows how well the resume matches the selected target role
- Resume Reliability Score — Compares resume structure against a golden ATS benchmark schema
- AI Suggestions — Role-specific career improvement suggestions with numbered display
- Visual Learning Roadmap — Interactive tree and milestone diagram with step-by-step guidance
- Role Quiz — 5 randomized MCQ questions per role with detailed scorecard and explanations
- Smart Fallback — Role-specific rule-based fallback when AI is unavailable or fails

---

## AI Integration + Fallback

| Feature | AI Path | Fallback Path |
|---|---|---|
| Skill Extraction | LLaMA 3.1 via Groq | Rule-based keyword matching across 50+ skills |
| Suggestions | LLaMA 3.1 via Groq | Role-specific structured suggestions |
| Roadmap | LLaMA 3.1 via Groq | Role-specific structured roadmap with real resources |
| Quiz | CSV-based static questions | Friendly error message with retry option |
| File Upload | PyMuPDF and python-docx | Clear error message with manual paste option |

---

## Security

- API keys stored in .env file and never committed to GitHub
- .env is listed in .gitignore
- Synthetic data only used — no real personal information included
- .env.example provided as a safe template for reviewers

---

## Synthetic Dataset

Included in /backend/data/:

- **skills.csv** — Maps 5 roles to required skills with learning order and priority levels
- **questions.csv** — 10 MCQ questions per role (50 total) with correct answers and explanations
- **golden_schema.json** — ATS benchmark schema defining what a perfect resume looks like

---

## Tests
```
test_happy_path_analyze        PASSED
test_edge_case_empty_input     PASSED
test_skill_extraction_fallback PASSED
test_quiz_route                PASSED

4 passed in 2.67s
```

---

## Demo Video

https://youtu.be/XfJda8UPhmM

## 🌐 Live Demo

Frontend: https://skill-navigator-final.vercel.app  
Backend: https://skill-navigator-final.onrender.com  

> Note: Backend may take 15–20 seconds to wake up (free tier on Render).
