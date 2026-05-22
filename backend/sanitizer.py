import re

MAX_RESUME_CHARS = 8000

INJECTION_PATTERNS = [
    r'ignore\s+(all\s+)?previous\s+instructions?',
    r'you\s+are\s+now\s+a?\s*different',
    r'new\s+instructions?:',
    r'system\s+prompt',
    r'disregard\s+(all\s+)?prior',
    r'forget\s+(all\s+)?previous',
    r'override\s+(all\s+)?instructions?',
    r'do\s+not\s+follow\s+(the\s+)?instructions?',
    r'pretend\s+(you\s+are|to\s+be)',
    r'jailbreak',
    r'dan\s+mode',
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]


def sanitize_resume(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    text = text[:MAX_RESUME_CHARS]
    for pattern in COMPILED_PATTERNS:
        text = pattern.sub("[removed]", text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\n{4,}', '\n\n', text)
    return text.strip()


def sanitize_role(role: str) -> str:
    if not role or not isinstance(role, str):
        return ""
    role = re.sub(r'[^a-zA-Z0-9\s./+#-]', '', role)
    return role.strip()[:100]


def wrap_for_prompt(resume_text: str, label: str = "resume") -> str:
    return f"<{label}>\n{resume_text}\n</{label}>"