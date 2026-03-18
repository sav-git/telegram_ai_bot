import sqlite3
import os
from datetime import datetime

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
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_history (timestamp)')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def save_user_message(user_id, role, message):
    """Save a message to the database"""
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
        ORDER BY timestamp ASC
        LIMIT ?
    ''', (user_id, limit))
    history = cursor.fetchall()
    history = [{'role': row['role'], 'content': row['message']} for row in history]
    conn.close()
    return history

def get_all_user_history(limit=100):
    """Retrieve all user message history from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, role, message, timestamp FROM chat_history
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    all_history = cursor.fetchall()
    all_history = [dict(row) for row in all_history]
    conn.close()
    return all_history

def clear_user_history(user_id):
    """Clear user message history from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount

def clear_all_user_history():
    """Clear all user message history from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_history')
    conn.commit()
    conn.close()
    return cursor.rowcount

def delete_old_records(days=30):
    """
    Delete records older than specified number of days.
    Returns number of deleted rows.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM chat_history WHERE timestamp < datetime("now", ?)',
        (f'-{days} days',)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted