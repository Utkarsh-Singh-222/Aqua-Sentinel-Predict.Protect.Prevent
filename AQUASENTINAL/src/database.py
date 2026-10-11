import sqlite3
import pandas as pd
from datetime import datetime
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS community_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            area TEXT,
            category TEXT,
            severity TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_report(area, category, severity, description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO community_reports (timestamp, area, category, severity, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, area, category, severity, description))
    conn.commit()
    conn.close()

def get_all_reports():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM community_reports ORDER BY timestamp DESC", conn)
    conn.close()
    return df
