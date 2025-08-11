import sqlite3
import pandas as pd
from datetime import datetime

def create_database():
    conn = sqlite3.connect("carbon_emission_data.db")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_emissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                country TEXT,
                age INTEGER,
                gender TEXT,
                transport REAL,
                electricity REAL,
                diet REAL,
                waste REAL,
                total REAL,
                timestamp TEXT
            )
        """)
    conn.commit()
    conn.close()

def save_user_data(name, country, age, gender, transport, electricity, diet, waste, total):
    conn = sqlite3.connect("carbon_emission_data.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO user_emissions (name, country, age, gender, transport, electricity, diet, waste, total, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, country, age, gender, transport, electricity, diet, waste, total, timestamp))
    conn.commit()
    conn.close()

def get_recent_data(limit=10):
    conn = sqlite3.connect("carbon_emission_data.db")
    df = pd.read_sql_query(f"SELECT * FROM user_emissions ORDER BY timestamp DESC LIMIT {limit}", conn)
    conn.close()
    return df
