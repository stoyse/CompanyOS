from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, login_user as flask_login_user
from db import get_user_by_username, create_user, update_user_password

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

def login_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        flask_login_user(User(user['id'], user['username']))  # Logge den Benutzer mit Flask-Login ein
        return True
    return False

def register_user(username, password):
    if get_user_by_username(username):
        return False
    hashed_password = generate_password_hash(password)
    create_user(username, hashed_password)
    return True

def verify_password(username, password):
    user = get_user_by_username(username)
    if user and user['password'] == password:  # Ersetze dies durch eine sichere Passwortprüfung
        return True
    return False

def update_password(username, new_password):
    return update_user_password(username, new_password)
