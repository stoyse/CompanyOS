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
    query = "SELECT id, full_name, email, role FROM team_members"  # Füge 'id' zur Abfrage hinzu
    rows = conn.execute(query).fetchall()
    conn.close()
    # Konvertiere die Ergebnisse in eine Liste von Dictionaries, einschließlich der ID
    return [{'id': row['id'], 'username': row['full_name'], 'email': row['email'], 'role': row['role']} for row in rows]

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

def get_user_profile(username):
    # Beispiel: Datenbankabfrage, um Benutzerprofilinformationen abzurufen
    query = "SELECT full_name, email, role, joined_at FROM team_members WHERE full_name = ?"
    conn = get_db_connection()
    result = conn.execute(query, (username,)).fetchone()
    conn.close()
    return dict(result) if result else None

def get_all_tasks():
    conn = get_db_connection()
    query = """
        SELECT tasks.id AS id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, 
               team_members.full_name AS assigned_to
        FROM tasks
        LEFT JOIN team_members ON tasks.assigned_to = team_members.id
    """  # Füge tasks.id explizit als 'id' hinzu
    rows = conn.execute(query).fetchall()
    conn.close()
    # Konvertiere die Ergebnisse in eine Liste von Dictionaries
    return [dict(row) for row in rows]

def create_task(title, description, status, priority, due_date, assigned_to):
    conn = get_db_connection()
    try:
        print(f"Attempting to insert task: title={title}, description={description}, status={status}, priority={priority}, due_date={due_date}, assigned_to={assigned_to}")  # Debugging-Ausgabe
        conn.execute(
            '''
            INSERT INTO tasks (title, description, status, priority, due_date, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (title, description, status, priority, due_date, assigned_to)
        )
        conn.commit()
        print("Task successfully inserted into database.")  # Debugging-Ausgabe
    except Exception as e:
        print(f"Error inserting task into database: {e}")  # Debugging-Ausgabe
    finally:
        conn.close()

def delete_task(task_id):
    """
    Löscht eine Aufgabe basierend auf der ID.
    """
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        print(f"Task {task_id} successfully deleted.")  # Debugging-Ausgabe
    except Exception as e:
        print(f"Error deleting task {task_id}: {e}")  # Debugging-Ausgabe
    finally:
        conn.close()

def update_task_status(task_id, new_status):
    """
    Aktualisiert den Status einer Aufgabe basierend auf der ID.
    """
    conn = get_db_connection()
    try:
        conn.execute('UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (new_status, task_id)) # Add updated_at
        conn.commit()
        print(f"Task {task_id} status updated to {new_status}.")  # Debugging-Ausgabe
    except Exception as e:
        print(f"Error updating task {task_id} status: {e}")  # Debugging-Ausgabe
    finally:
        conn.close()

def update_task(task_id, title, description, status, priority, due_date, assigned_to):
    """
    Aktualisiert alle Felder einer Aufgabe basierend auf der ID.
    """
    conn = get_db_connection()
    try:
        # Stelle sicher, dass assigned_to ein Integer ist oder NULL, falls leer
        assigned_to_id = int(assigned_to) if assigned_to else None

        print(f"Updating task {task_id}: title={title}, desc={description}, status={status}, prio={priority}, due={due_date}, assigned={assigned_to_id}") # Debugging
        conn.execute(
            '''
            UPDATE tasks
            SET title = ?, description = ?, status = ?, priority = ?, due_date = ?, assigned_to = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (title, description, status, priority, due_date, assigned_to_id, task_id)
        )
        conn.commit()
        print(f"Task {task_id} successfully updated.") # Debugging
        return True
    except ValueError:
        print(f"Error updating task {task_id}: Invalid assigned_to value '{assigned_to}'. Must be an integer or empty.") # Debugging
        return False
    except Exception as e:
        print(f"Error updating task {task_id}: {e}") # Debugging
        return False
    finally:
        conn.close()