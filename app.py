import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory  # Importiere session und send_from_directory
from auth import login_user, register_user, User  # Importiere User aus auth.py
from flask_login import login_required, LoginManager, UserMixin  # Import login_required, LoginManager, and UserMixin from flask_login

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Setze eine geheime Schlüsselvariable

login_manager = LoginManager()
login_manager.init_app(app)  # Initialisiere LoginManager mit der Flask-App
login_manager.login_view = 'login'  # Setze die Login-Route

@login_manager.user_loader
def load_user(user_id):
    from db import get_user_by_id  # Importiere hier, um zirkuläre Importe zu vermeiden
    user = get_user_by_id(user_id)
    if user:
        return User(user['id'], user['username'])
    return None

@app.route('/')
@login_required
def home():
    return render_template('index.html', username=session.get('username'))  # Übergebe den Benutzernamen an die Vorlage

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            session['username'] = username  # Speichere den Benutzernamen in der Session
            flash('Login erfolgreich!', 'success')
            return redirect(url_for('home'))  # Stelle sicher, dass die 'home'-Route korrekt aufgerufen wird
        else:
            flash('Ungültige Anmeldedaten.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        if register_user(full_name, password):
            flash('Registrierung erfolgreich! Bitte loggen Sie sich ein.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Benutzername bereits vergeben.', 'danger')
    return render_template('register.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html', username=session.get('username'))

@app.route('/api/avatar/<username>', methods=['GET'])
def get_avatar(username):
    avatar_path = f'database/avatars/'  # Verzeichnis, in dem die Avatare gespeichert sind
    avatar_file = f"{username}.png"  # Erstelle den Dateinamen basierend auf dem Benutzernamen
    if os.path.exists(os.path.join(avatar_path, avatar_file)):
        return send_from_directory(avatar_path, avatar_file)  # Sende die Avatar-Datei zurück
    else:
        return 'Avatar nicht gefunden', 404

@app.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        flash('Keine Datei ausgewählt.', 'danger')
        return redirect(url_for('settings'))
    file = request.files['avatar']
    if file.filename == '':
        flash('Keine Datei ausgewählt.', 'danger')
        return redirect(url_for('settings'))
    if file and file.filename.endswith(('.png', '.jpg', '.jpeg')):
        avatar_path = f'database/avatars/{session["username"]}.png'
        file.save(avatar_path)
        flash('Avatar erfolgreich hochgeladen!', 'success')
    else:
        flash('Ungültiges Dateiformat. Bitte PNG oder JPEG verwenden.', 'danger')
    return redirect(url_for('settings'))

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    from auth import verify_password, update_password  # Importiere notwendige Funktionen
    if verify_password(session['username'], current_password):
        if update_password(session['username'], new_password):
            flash('Passwort erfolgreich geändert!', 'success')
        else:
            flash('Fehler beim Ändern des Passworts.', 'danger')
    else:
        flash('Aktuelles Passwort ist falsch.', 'danger')
    return redirect(url_for('settings'))

@app.route('/team', methods=['GET'])
@login_required
def team():
    from db import get_all_team_members  # Importiere Funktion, um Teammitglieder aus der Datenbank abzurufen
    team_members = get_all_team_members()  # Holt die Teammitglieder aus der Tabelle `team_members`
    return render_template('team.html', team_members=team_members)  # Übergibt die Teammitglieder an die Vorlage

@app.route('/team/<username>', methods=['GET'])
@login_required
def team_member(username):
    from db import get_team_member_by_username  # Importiere Funktion, um Teammitglied-Daten zu holen
    member = get_team_member_by_username(username)
    if not member:
        flash('Teammitglied nicht gefunden.', 'danger')
        return redirect(url_for('team'))
    return render_template('team_member.html', member=member)

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    from db import get_team_member_by_username  # Importiere Funktion, um Teammitglied-Daten zu holen
    member = get_team_member_by_username(session['username'])
    if not member or member.get('role') != 'admin':  # Überprüfe, ob der Benutzer die Rolle 'admin' hat
        flash('Zugriff verweigert. Nur Administratoren dürfen diese Seite sehen.', 'danger')
        return redirect(url_for('home'))
    return render_template('admin.html', username=session.get('username'))  # Rendere die Admin-Seite

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
