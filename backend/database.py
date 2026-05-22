import sqlite3
import json
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "skill_navigator.db")


def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS analyses (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id          TEXT NOT NULL,
                role                TEXT NOT NULL,
                skills              TEXT,
                missing             TEXT,
                match_score         INTEGER,
                reliability_score   INTEGER,
                reliability_label   TEXT,
                improvements        TEXT,
                ai_used             INTEGER DEFAULT 0,
                created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT NOT NULL,
                role        TEXT NOT NULL,
                score       INTEGER NOT NULL,
                total       INTEGER NOT NULL,
                answers     TEXT,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_analyses_session  ON analyses(session_id);
            CREATE INDEX IF NOT EXISTS idx_analyses_created  ON analyses(created_at);
            CREATE INDEX IF NOT EXISTS idx_quiz_session      ON quiz_attempts(session_id);
        """)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def save_analysis(session_id, role, skills, missing, match_score,
                  reliability_score, label, improvements, ai_used=False):
    with get_db() as db:
        cursor = db.execute(
            """INSERT INTO analyses
               (session_id, role, skills, missing, match_score,
                reliability_score, reliability_label, improvements, ai_used)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (session_id, role,
             json.dumps(skills), json.dumps(missing),
             match_score, reliability_score, label,
             json.dumps(improvements), int(ai_used))
        )
        return cursor.lastrowid


def save_quiz_attempt(session_id, role, score, total, answers):
    with get_db() as db:
        cursor = db.execute(
            """INSERT INTO quiz_attempts
               (session_id, role, score, total, answers)
               VALUES (?,?,?,?,?)""",
            (session_id, role, score, total, json.dumps(answers))
        )
        return cursor.lastrowid


def get_history(session_id, limit=10):
    with get_db() as db:
        rows = db.execute(
            """SELECT role, match_score, reliability_score,
                      reliability_label, ai_used, created_at
               FROM analyses
               WHERE session_id = ?
               ORDER BY created_at DESC LIMIT ?""",
            (session_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]


def get_quiz_history(session_id, limit=10):
    with get_db() as db:
        rows = db.execute(
            """SELECT role, score, total,
                      ROUND(score * 100.0 / total) as percent,
                      created_at
               FROM quiz_attempts
               WHERE session_id = ?
               ORDER BY created_at DESC LIMIT ?""",
            (session_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]


def get_score_trend(session_id, role):
    with get_db() as db:
        rows = db.execute(
            """SELECT match_score, reliability_score, created_at
               FROM analyses
               WHERE session_id = ? AND role = ?
               ORDER BY created_at ASC LIMIT 20""",
            (session_id, role)
        ).fetchall()
        return [dict(r) for r in rows]