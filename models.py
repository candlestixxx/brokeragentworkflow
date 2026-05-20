import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_path():
    return os.getenv("DATABASE_PATH", "goals.db")

def init_db(db_path=None):
    if db_path is None:
        db_path = get_db_path()
    """Initialize the database with required tables."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS quarterly_initiatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quarter TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# --- Daily Goals ---
def add_goal(description, db_path=None):
    if db_path is None: db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO goals (description) VALUES (?)', (description,))
    goal_id = c.lastrowid
    conn.commit()
    conn.close()
    return goal_id

def list_pending_goals(db_path=None):
    if db_path is None: db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, description FROM goals WHERE status = "pending"')
    goals = c.fetchall()
    conn.close()
    return goals

def complete_goal(goal_id, db_path=None):
    if db_path is None: db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE goals SET status = "completed" WHERE id = ?', (goal_id,))
    success = c.rowcount > 0
    conn.commit()
    conn.close()
    return success

# --- Quarterly Initiatives ---
def add_initiative(quarter, description, db_path=None):
    if db_path is None: db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO quarterly_initiatives (quarter, description) VALUES (?, ?)', (quarter, description))
    initiative_id = c.lastrowid
    conn.commit()
    conn.close()
    return initiative_id

def list_pending_initiatives(db_path=None):
    if db_path is None: db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, quarter, description FROM quarterly_initiatives WHERE status = "pending" ORDER BY quarter ASC')
    initiatives = c.fetchall()
    conn.close()
    return initiatives

def complete_initiative(initiative_id, db_path=None):
    if db_path is None: db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE quarterly_initiatives SET status = "completed" WHERE id = ?', (initiative_id,))
    success = c.rowcount > 0
    conn.commit()
    conn.close()
    return success
