DROP TABLE IF EXISTS chat_messages; -- Lösche die alte Tabelle, falls sie existiert (für einfache Entwicklung)

CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    content TEXT NOT NULL, -- Für Textnachrichten der Inhalt, für Dateien der Dateiname
    message_type TEXT NOT NULL DEFAULT 'text', -- 'text' oder 'file'
    file_url TEXT, -- URL oder Pfad zur Datei, NULL für Textnachrichten
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);