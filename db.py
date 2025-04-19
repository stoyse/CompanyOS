import sqlite3
import os
from dotenv import load_dotenv
import random

load_dotenv()

MAIL_DOMAIN = os.getenv('MAIL_DOMAIN', 'example.com')
# Setze den Standardwert für MAIL_DOMAIN auf 'example.com', wenn er nicht gesetzt is

DATABASE = os.getenv('DATABASE_PATH', '/database/database.db')  # Ensure the correct default path

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    print(f"Connected to database at {DATABASE}")
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def create_user(username, password):
    id = random.randint(1000, 9999)  # Generate a random ID
    conn = get_db_connection()
    conn.execute('INSERT INTO users (id, username, password) VALUES (?, ?, ?)', (id, username, password))
    # Provide a default email value for team_members
    default_email = f"{username}@{MAIL_DOMAIN}"
    conn.execute('INSERT INTO team_members (id, full_name, email) VALUES (?, ?, ?)', (id, username, default_email))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

# Functions for the team_members table
def get_team_member_by_id(member_id):
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM team_members WHERE id = ?', (member_id,)).fetchone()
    conn.close()
    return member

def get_team_member_by_username(username):
    conn = get_db_connection()
    query = "SELECT full_name AS username, email, role FROM team_members WHERE full_name = ?"
    member = conn.execute(query, (username,)).fetchone()
    conn.close()
    return dict(member) if member else None

def create_team_member(full_name, email, role, avatar_url=None):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO team_members (full_name, email, role, avatar_url) VALUES (?, ?, ?, ?)',
        (full_name, email, role, avatar_url)
    )
    conn.commit()
    conn.close()

def get_all_team_members():
    conn = get_db_connection()
    query = "SELECT full_name, email, role FROM team_members"  # Abfrage für Teammitglieder
    rows = conn.execute(query).fetchall()
    conn.close()
    # Konvertiere die Ergebnisse in eine Liste von Dictionaries
    return [{'username': row['full_name'], 'email': row['email'], 'role': row['role']} for row in rows]

def get_avatar_by_username(username):
    # Beispiel: Abrufen des Avatars aus einer Datenbank oder einem Speicher
    # Ersetze dies durch die tatsächliche Implementierung
    avatars = {
        'user1': 'https://example.com/avatars/user1.png',
        'user2': 'https://example.com/avatars/user2.png'
    }
    return avatars.get(username)

def update_user_password(username, new_password):
    """
    Aktualisiert das Passwort eines Benutzers in der Datenbank.
    """
    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()
    return True


def save_message(sender, recipient, content, message_type='text', file_url=None):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO chat_messages (sender, recipient, content, message_type, file_url) VALUES (?, ?, ?, ?, ?)',
        (sender, recipient, content, message_type, file_url)
    )
    conn.commit()
    conn.close()

def get_messages_between(user1, user2):
    conn = get_db_connection()
    messages = conn.execute(
        '''
        SELECT id, sender, recipient, content, message_type, file_url, timestamp FROM chat_messages
        WHERE (sender = ? AND recipient = ?)
           OR (sender = ? AND recipient = ?)
        ORDER BY id ASC
        ''',
        (user1, user2, user2, user1)
    ).fetchall()
    conn.close()
    return messages