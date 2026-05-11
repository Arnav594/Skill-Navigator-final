"""Configuration: environment variables, paths, and runtime constants.

All env access lives here so the rest of the codebase never reaches for
os.getenv directly. Makes tests and future deploys easier.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SKILLS_CSV = os.path.join(DATA_DIR, "skills.csv")
QUESTIONS_CSV = os.path.join(DATA_DIR, "questions.csv")
GOLDEN_SCHEMA_JSON = os.path.join(DATA_DIR, "golden_schema.json")

# --- API keys ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Model config ---
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# --- Flask config ---
DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
PORT = int(os.getenv("PORT", 5000))
