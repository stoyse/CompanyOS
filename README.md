# CompanyOS

CompanyOS ist eine webbasierte Anwendung zur Verwaltung von Teams, Aufgaben und Projekten. Sie bietet Funktionen wie Benutzerregistrierung, Login, Teamverwaltung und ein Dashboard.

## Features

- Benutzerregistrierung und -authentifizierung
- Teamverwaltung mit Rollen und Avataren
- **Echtzeit-Chat zwischen Teammitgliedern**
- Aufgaben- und Projektmanagement
- Admin-Bereich für privilegierte Benutzer
- Anpassbares Dashboard

## Installation

1. **Repository klonen**:
   ```bash
   git clone <repository-url>
   cd CompanyOS
   ```

2. **Abhängigkeiten installieren**:
   Stelle sicher, dass du Python 3 und pip installiert hast.
   ```bash
   pip install -r requirements.txt
   ```

3. **Datenbank einrichten**:
   Führe die SQL-Skripte im Ordner `database` aus, um die Datenbanktabellen zu erstellen:
   ```bash
   sqlite3 database/database.db < database/setup.sql # Erstellt users Tabelle (falls noch nicht geschehen)
   sqlite3 database/database.db < database/schema.sql # Erstellt team_members Tabelle
   sqlite3 database/database.db < database/tasks_setup.sql # Erstellt tasks Tabelle
   sqlite3 database/database.db < create_chat_table.sql # Erstellt chat_messages Tabelle
   # Optional: Admin-Benutzer erstellen/aktualisieren
   # sqlite3 database/database.db < database/set_admin_role.sql
   ```

4. **Umgebungsvariablen konfigurieren**:
   Erstelle eine `.env`-Datei basierend auf der bereitgestellten `.env`-Vorlage (falls vorhanden) oder setze die Variablen direkt. Wichtig ist `SECRET_KEY`.
   ```dotenv
   # .env Beispiel
   SECRET_KEY='dein_sehr_geheimer_schluessel'
   DATABASE_PATH='database/database.db'
   MAIL_DOMAIN='company.local'
   ```

5. **Server starten**:
   Da wir Flask-SocketIO mit `eventlet` verwenden, starte die App wie folgt:
   ```bash
   python app.py
   ```
   Der Server läuft standardmäßig auf `http://0.0.0.0:5000`.

6. **Zugriff auf die Anwendung**:
   Öffne einen Browser und navigiere zu `http://localhost:5000` oder der entsprechenden IP/Port.

## Nutzung

- **Registrierung**: Erstelle ein Benutzerkonto über die Registrierungsseite.
- **Login**: Melde dich mit deinem Benutzernamen und Passwort an.
- **Dashboard**: Verwalte Aufgaben, Projekte und Teammitglieder.
- **Admin-Bereich**: Zugriff auf administrative Funktionen (nur für Benutzer mit Admin-Rolle).
- **Chat**: Navigiere zum Profil eines Teammitglieds, um einen Echtzeit-Chat zu starten.

## Projektstruktur

- `templates/`: HTML-Vorlagen für die Benutzeroberfläche
- `static/`: Statische Dateien wie CSS und Bilder
- `database/`: SQL-Skripte und Datenbankdateien
- `app.py`: Hauptanwendung
- `auth.py`: Authentifizierungslogik
- `db.py`: Datenbankoperationen
- `create_chat_table.sql`: SQL-Skript für die Chat-Tabelle

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der Datei `LICENSE`.

