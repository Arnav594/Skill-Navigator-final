"""Flask app factory. Keeps the entrypoint tiny — all the actual work
lives in routes/ and services/.
"""
from flask import Flask
from flask_cors import CORS

from routes import roles, quiz, analyze


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(roles.bp)
    app.register_blueprint(quiz.bp)
    app.register_blueprint(analyze.bp)

    return app


# Module-level `app` instance — preserved so existing deploys
# (Render, Gunicorn `app:app`) keep working without config changes.
app = create_app()
