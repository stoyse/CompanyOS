# CompanyOS

CompanyOS ist eine webbasierte Anwendung zur Verwaltung von Teams, Aufgaben und Projekten. Sie bietet Funktionen wie Benutzerregistrierung, Login, Teamverwaltung und ein Dashboard.

## Features

- Benutzerregistrierung und -authentifizierung
- Teamverwaltung mit Rollen und Avataren
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
   ```bash
   pip install -r requirements.txt
   ```

3. **Datenbank einrichten**:
   Führe die SQL-Skripte im Ordner `database` aus, um die Datenbanktabellen zu erstellen:
   ```bash
   sqlite3 database/database.db < database/schema.sql
   sqlite3 database/database.db < database/tasks_setup.sql
   ```

4. **Umgebungsvariablen konfigurieren**:
   Erstelle eine `.env`-Datei basierend auf der bereitgestellten `.env`-Vorlage und passe die Werte an.

5. **Server starten**:
   ```bash
   python app.py
   ```

6. **Zugriff auf die Anwendung**:
   Öffne einen Browser und navigiere zu `http://localhost:5000`.

## Nutzung

- **Registrierung**: Erstelle ein Benutzerkonto über die Registrierungsseite.
- **Login**: Melde dich mit deinem Benutzernamen und Passwort an.
- **Dashboard**: Verwalte Aufgaben, Projekte und Teammitglieder.
- **Admin-Bereich**: Zugriff auf administrative Funktionen (nur für Benutzer mit Admin-Rolle).

## Projektstruktur

- `templates/`: HTML-Vorlagen für die Benutzeroberfläche
- `static/`: Statische Dateien wie CSS und Bilder
- `database/`: SQL-Skripte und Datenbankdateien
- `app.py`: Hauptanwendung
- `auth.py`: Authentifizierungslogik
- `db.py`: Datenbankoperationen

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der Datei `LICENSE`.

