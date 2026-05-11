"""Local dev entry point: `python run.py` starts the Flask dev server.

For production (Render, etc.) use `gunicorn app:app` — the existing
deploy config keeps working since app.py still exports `app`.
"""
from app import app
from config import DEBUG, PORT

if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)
