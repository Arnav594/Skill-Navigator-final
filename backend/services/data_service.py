"""CSV data loaders. Single source of truth for reading skills.csv and
questions.csv. Wraps the file paths from config so callers stay clean.
"""
import csv
import random
from config import SKILLS_CSV, QUESTIONS_CSV


def load_role_data(role: str) -> list[dict]:
    """Return all rows in skills.csv for the given role."""
    data = []
    with open(SKILLS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["role"] == role:
                data.append(row)
    return data


def load_quiz_questions(role: str) -> list[dict]:
    """Return all quiz rows for the given role, shuffled."""
    questions = []
    with open(QUESTIONS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["role"] == role:
                questions.append(row)
    random.shuffle(questions)
    return questions


def load_all_roles() -> list[str]:
    """Return the sorted list of unique roles in skills.csv."""
    roles = set()
    with open(SKILLS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            roles.add(row["role"])
    return sorted(roles)
