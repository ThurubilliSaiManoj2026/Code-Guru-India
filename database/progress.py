# database/progress.py
import sqlite3
from datetime import datetime

DB_PATH = "progress.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Progress table
    c.execute('''CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        subject TEXT,
        topic TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    # Chat sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        question TEXT,
        answer TEXT,
        language TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def save_progress(student_name, subject, topic):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO progress (student_name, subject, topic) VALUES (?, ?, ?)",
        (student_name, subject, topic)
    )
    conn.commit()
    conn.close()

def get_progress(student_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM progress WHERE student_name=?",
        (student_name,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def save_chat_session(student_name, question, answer, language):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_sessions (student_name, question, answer, language) VALUES (?, ?, ?, ?)",
        (student_name, question, answer, language)
    )
    conn.commit()
    conn.close()

def get_chat_sessions(student_name, limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, question, answer, language, timestamp FROM chat_sessions WHERE student_name=? ORDER BY timestamp DESC LIMIT ?",
        (student_name, limit)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def delete_all_sessions(student_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM chat_sessions WHERE student_name=?", (student_name,))
    c.execute("DELETE FROM progress WHERE student_name=?", (student_name,))
    conn.commit()
    conn.close()