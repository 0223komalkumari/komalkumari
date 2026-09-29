import sqlite3
from contextlib import contextmanager
from app.config import settings

SCHEMA = '''
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 email TEXT NOT NULL UNIQUE,
 password_hash TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS recommendations (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER NOT NULL,
 planner_type TEXT NOT NULL,
 request_json TEXT NOT NULL,
 response_json TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
'''

@contextmanager
def get_db():
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as db:
        db.executescript(SCHEMA)

def create_user(email, password_hash):
    with get_db() as db:
        cur = db.execute("INSERT INTO users(email,password_hash) VALUES(?,?)",
                         (email.lower().strip(), password_hash))
        return cur.lastrowid

def get_user_by_email(email):
    with get_db() as db:
        return db.execute("SELECT * FROM users WHERE email=?",
                          (email.lower().strip(),)).fetchone()

def get_user_by_id(user_id):
    with get_db() as db:
        return db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

def save_recommendation(user_id, planner_type, request_json, response_json):
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO recommendations(user_id,planner_type,request_json,response_json) VALUES(?,?,?,?)",
            (user_id, planner_type, request_json, response_json))
        return cur.lastrowid

def list_history(user_id):
    with get_db() as db:
        return db.execute(
            "SELECT id,planner_type,request_json,response_json,created_at "
            "FROM recommendations WHERE user_id=? ORDER BY id DESC", (user_id,)).fetchall()

def get_recommendation(user_id, recommendation_id):
    with get_db() as db:
        return db.execute(
            "SELECT id,planner_type,request_json,response_json,created_at "
            "FROM recommendations WHERE id=? AND user_id=?",
            (recommendation_id, user_id)).fetchone()
