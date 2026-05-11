"""All Groq API calls live here.

Three callable functions, each returns None on failure so the route layer
can fall back to deterministic logic. The Groq client is created lazily
via _get_client() so tests can patch it without import-time side effects.
"""
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

_client = None


def _get_client() -> Groq:
    """Lazy singleton — only instantiate when first AI call is made."""
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


# -------- Skill extraction --------
_SKILL_EXTRACT_SYSTEM = """You are a skill extractor.
Your ONLY job is to extract technical skills from the resume text.
Return ONLY a comma-separated list of skills like this:
Python, SQL, Docker, AWS

STRICT RULES:
- No sentences
- No explanations
- No roadmap
- No suggestions
- No extra text whatsoever
- ONLY skill names separated by commas"""


def extract_skills_ai(text: str) -> list[str] | None:
    """Ask the LLM to extract skills as a comma-separated list.
    Returns None on any failure — caller is responsible for falling back.
    """
    try:
        response = _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": _SKILL_EXTRACT_SYSTEM},
                {"role": "user", "content": f"Extract only the technical skills from this resume:\n{text}"},
            ],
        )
        skills = response.choices[0].message.content.split(",")
        return [s.strip() for s in skills if s.strip()]
    except Exception as e:
        print("AI skill-extraction error:", e)
        return None


# -------- Suggestions --------
_SUGGESTIONS_SYSTEM = """You are a career advisor. Give exactly 4-5 suggestions.
You MUST use this EXACT format for every suggestion, no exceptions:

TITLE: Write a short 3-5 word title here
DESCRIPTION: Write one detailed paragraph here

Rules:
- TITLE line must start with exactly "TITLE:"
- DESCRIPTION line must start with exactly "DESCRIPTION:"
- Separate each suggestion with one blank line
- No bullets, no numbers, no asterisks, no markdown
- Every suggestion must have both TITLE and DESCRIPTION"""


def generate_ai_suggestions(resume: str, role: str, missing: list[str], improvements: list[str]) -> str | None:
    """Generate role-specific suggestions using LLM. Returns raw string with
    TITLE:/DESCRIPTION: blocks separated by blank lines, or None on failure.
    """
    try:
        response = _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": _SUGGESTIONS_SYSTEM},
                {"role": "user", "content": f"Role: {role}\nResume: {resume}\nMissing skills: {missing}\nResume improvements needed: {improvements}"},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print("AI suggestions error:", e)
        return None


# -------- Roadmap --------
_ROADMAP_SYSTEM = """You are a learning roadmap generator.
Create a step-by-step roadmap. Each step MUST follow this exact format:

STEP: Skill name only here (no numbers)
HOW: One specific practical way to learn this skill

Separate each step with a blank line.
No bullet points, no asterisks, no markdown, no extra text.
Do NOT include step numbers in the STEP field."""


def generate_ai_roadmap(resume: str, role: str, role_data: list[dict], missing: list[str]) -> str | None:
    """Generate a STEP:/HOW: formatted roadmap. Returns None on failure."""
    try:
        context = "\n".join([f"{i['learning_order']}. {i['skill']}" for i in role_data])
        response = _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": _ROADMAP_SYSTEM},
                {"role": "user", "content": f"Role: {role}\nResume: {resume}\nSkill order:\n{context}\nMissing skills: {missing}"},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print("AI roadmap error:", e)
        return None
