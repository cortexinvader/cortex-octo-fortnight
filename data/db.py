import sqlite3
from flask import g
from config import SQLITE_DB

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB)
        db.row_factory = sqlite3.Row  # Makes results easier to work with
    return db

def init_db():
    db = sqlite3.connect(SQLITE_DB)
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chatlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT DEFAULT 'Guest',
            user_message TEXT,
            bot_response TEXT,
            error_in_function_call TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    db.commit()
    db.close()

def prune_user_history(username):
    """
    Keep only the last 10 messages per user. Delete older ones. (^√^)
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        DELETE FROM chatlog
        WHERE id NOT IN (
            SELECT id FROM chatlog
            WHERE username = ?
            ORDER BY created_at DESC
            LIMIT 10
        ) AND username = ?
    """, (username, username))
    db.commit()

def get_conversation_history(db, username, limit=10):
    db.row_factory = Row
    rows = db.execute(
        "SELECT user_message, bot_response FROM chatlog WHERE username = ? ORDER BY id DESC LIMIT ?",
        (username, limit)
    ).fetchall()
    rows.reverse()  # To maintain chronological order
    return "\n".join(
        f"User: {r['user_message']}\nAssistant: {r['bot_response']}" for r in rows if r['user_message'] and r['bot_response']
    )
