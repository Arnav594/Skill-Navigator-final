"""Service layer: business logic separated from HTTP routing.

Each module owns one concern:
- ai_service:    Groq LLM calls (skill extraction, suggestions, roadmap)
- skill_service: rule-based skill extraction, gap analysis, confidence
- file_service:  parsing uploaded PDF/DOCX resumes
- data_service:  loading CSV data (roles, skills, quiz questions)
- fallbacks:     role-specific suggestions and roadmaps when AI fails
"""
