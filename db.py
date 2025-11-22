import sqlite3
import os

def get_db_connection():
    """Get a connection to the SQLite database"""
    db_path = os.getenv("DATABASE_URL", "chat_history.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON chat_history (user_id)')
    conn.commit()
    conn.close()

def save_user_message(user_id, role, message):
    """Save a user message to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (user_id, role, message)
        VALUES (?, ?, ?)
    ''', (user_id, role, message))
    conn.commit()
    conn.close()

def get_user_history(user_id, limit=20):
    """Retrieve user message history from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, message FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, limit))
    history = cursor.fetchall()
    history = [{'role': row['role'], 'content': row['message']} for row in history]
    conn.close()
    return history

def clear_user_history(user_id):
    """Clear user message history from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
