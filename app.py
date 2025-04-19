import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
from auth import login_user, register_user, User
from flask_login import login_required, LoginManager, UserMixin, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from db import save_message, get_messages_between
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'database/chat_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'doc', 'docx', 'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    from db import get_user_by_id
    user = get_user_by_id(user_id)
    if user:
        return User(user['id'], user['username'])
    return None

@app.route('/')
@login_required
def home():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/ai')
@login_required
def ai():
    return render_template('ai.html', username=session.get('username'))

@app.route('/team', methods=['GET'])
@login_required
def team():
    from db import get_all_team_members
    team_members = get_all_team_members()
    return render_template('team.html', team_members=team_members, username=session.get('username'))

@app.route('/team/<username>', methods=['GET'])
@login_required
def team_member(username):
    from db import get_team_member_by_username
    member = get_team_member_by_username(username)
    if not member:
        flash('Teammitglied nicht gefunden.', 'danger')
        return redirect(url_for('team'))
    return render_template('team_member.html', member=member, username=current_user.username)

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', username=session.get('username'))

@app.route('/projects')
@login_required
def projects():
    return render_template('projects.html', username=session.get('username'))

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            session['username'] = username
            flash('Login erfolgreich!', 'success')
            return redirect(url_for('home'))
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

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('Erfolgreich abgemeldet!', 'success')
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html', username=session.get('username'))

@app.route('/api/avatar/<username>', methods=['GET'])
def get_avatar(username):
    avatar_path = f'database/avatars/'
    avatar_file = f"{username}.png"
    if os.path.exists(os.path.join(avatar_path, avatar_file)):
        return send_from_directory(avatar_path, avatar_file)
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
    from auth import verify_password, update_password
    if verify_password(session['username'], current_password):
        if update_password(session['username'], new_password):
            flash('Passwort erfolgreich geändert!', 'success')
        else:
            flash('Fehler beim Ändern des Passworts.', 'danger')
    else:
        flash('Aktuelles Passwort ist falsch.', 'danger')
    return redirect(url_for('settings'))

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    from db import get_team_member_by_username
    member = get_team_member_by_username(session['username'])
    if not member or member.get('role') != 'admin':
        flash('Zugriff verweigert. Nur Administratoren dürfen diese Seite sehen.', 'danger')
        return redirect(url_for('home'))
    return render_template('admin.html', username=session.get('username'))

@app.route('/chat/<recipient>', methods=['GET'])
@login_required
def get_chat_messages(recipient):
    messages = get_messages_between(current_user.username, recipient)
    messages_list = [
        {'id': msg['id'], 'sender': msg['sender'], 'recipient': msg['recipient'],
         'content': msg['content'], 'message_type': msg['message_type'],
         'file_url': msg['file_url'], 'timestamp': msg['timestamp']}
        for msg in messages
    ]
    return jsonify(messages_list)

@app.route('/upload_chat_file', methods=['POST'])
@login_required
def upload_chat_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        try:
            file.save(filepath)
            file_url = url_for('download_chat_file', filename=unique_filename, _external=True)
            print(f"File saved: {filepath}, URL: {file_url}")
            return jsonify({'file_url': file_url, 'filename': original_filename}), 200
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': 'Failed to save file'}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download_chat_file/<filename>')
@login_required
def download_chat_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        flash('File not found.', 'danger')
        return redirect(request.referrer or url_for('home'))

@socketio.on('connect')
@login_required
def handle_connect():
    join_room(current_user.username)
    print(f'Client {current_user.username} ({request.sid}) connected and joined room {current_user.username}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client ({request.sid}) disconnected')

@socketio.on('send_message')
@login_required
def handle_send_message(data):
    sender = current_user.username
    recipient = data['recipient']
    message_type = data.get('message_type', 'text')
    content = data['message']
    file_url = data.get('file_url')

    save_message(sender, recipient, content, message_type, file_url)

    message_data = {
        'sender': sender,
        'recipient': recipient,
        'content': content,
        'message_type': message_type,
        'file_url': file_url,
        'timestamp': 'now'
    }

    emit('receive_message', message_data, room=recipient)
    emit('receive_message', message_data, room=sender)

    if message_type == 'file':
        notification_content = f"Sent you a file: {content}"
    else:
        notification_content = content

    notification_data = {
        'sender': sender,
        'message_snippet': notification_content[:30] + ('...' if len(notification_content) > 30 else ''),
        'message_type': message_type
    }
    emit('new_message_notification', notification_data, room=recipient)

    print(f"Message ({message_type}) from {sender} to {recipient}: {content}")
    if file_url:
        print(f"  File URL: {file_url}")
    if message_type != 'text':
        print(f"Sent notification to {recipient}")

if __name__ == '__main__':
    print("Starting SocketIO server...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
