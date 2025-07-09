import sqlite3
import os
from datetime import datetime

def init_db(db_path="logs/faces.db"):
    os.makedirs("logs", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS face_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            face_id TEXT,
            timestamp TEXT,
            image_path TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitor_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            unique_visitor_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def log_to_db(face_id, image_path, db_path="logs/faces.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO face_logs (face_id, timestamp, image_path) VALUES (?, ?, ?)",
              (face_id, timestamp, image_path))
    conn.commit()
    conn.close()

def update_visitor_count(count, db_path="logs/faces.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO visitor_stats (date, unique_visitor_count) VALUES (?, ?)", (today, count))
    conn.commit()
    conn.close()
