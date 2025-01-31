import sqlite3
import os
from datetime import datetime
import shutil
import time

# Ordner für alle Datenbankfiles definieren
backupfile_ordner = '/home/zvowevan/Projects/Freundschaftsbuch/Backup-Files'

# Pfad des Datenbankfiles definieren
datenbank_file = '/home/zvowevan/Projects/Freundschaftsbuch/database.db'

# Backupordner erstellen, falls noch keiner existiert
if not os.path.exists(backupfile_ordner):
    os.makedirs(backupfile_ordner)

# Backupfiles organisieren und limitierten
def get_backup_files():
    """Aktualisiere und gebe die Liste der Backupfiles zurück."""
    return sorted(os.listdir(backupfile_ordner))  # Nach Namen sortieren, älteste zuerst

print(f"Backup-Files vor dem Kopieren: {get_backup_files()}\nAnzahl Backup-Files: {len(get_backup_files())}")

max_backupfiles = 30  # Beispiel: Begrenze auf maximal 3 Backups

# Überschüssige Files löschen (die Fileanzahl sollte konstant bleiben)
def regulate():
    try:
        liste_backupfiles = get_backup_files()
        anzahl_backupfiles = len(liste_backupfiles)

        if anzahl_backupfiles > max_backupfiles:
            anzahl_deletable = anzahl_backupfiles - max_backupfiles
            deletable = liste_backupfiles[:anzahl_deletable]  # Nur die ältesten Dateien
            print(f"\nÜberschüssige Files: {deletable}")

            for file in deletable:
                os.remove(os.path.join(backupfile_ordner, file))
                print(f"\nGelöschte Datei: {file}")
        else:
            print("\nEs besteht kein File-Überschuss!")
    except Exception as e:
        print(f"\nFehler in der Regulierung: {e}")

# Datenbankfiles in den vordefinierten Pfad kopieren als Backup
def make_copy():
    try:
        # Erzeugt einen Zeitstempel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backupfile_path = os.path.join(backupfile_ordner, f"datenbank_backup_{timestamp}.db")

        # Eine Kopie der richtigen Datenbank erstellen und dem vordefinierten Pfad zuordnen
        copied_file = shutil.copy2(datenbank_file, backupfile_path)
        print(f"\nBackup erfolgreich erstellt: {copied_file}")

        # Regulierung der Backups aufrufen
        regulate()

        # Zeige aktuelle Backups an
        liste_backupfiles = get_backup_files()
        print(f"\nBackup-Files nach dem Kopieren: {liste_backupfiles}\nAnzahl Backupfiles: {len(liste_backupfiles)}")

    except Exception as e:
        print(f"\nFehler beim Erstellen des Backups: {e}")

# initialer aufruf
#make_copy()


def init_db():
    conn = sqlite3.connect('/home/zvowevan/Projects/Freundschaftsbuch/database.db')
    c = conn.cursor()

    # Log-Tabelle erstellen
    c.execute('''CREATE TABLE IF NOT EXISTS log_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT,
                    change_type TEXT,
                    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Beispiel-Tabellen erstellen
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT)''')

    # Trigger für INSERT in users
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_users_insert
        AFTER INSERT ON users
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('users', 'INSERT');
        END;
    ''')

    # Trigger für UPDATE in users
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_users_update
        AFTER UPDATE ON users
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('users', 'UPDATE');
        END;
    ''')

    # Trigger für DELETE in users
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_users_delete
        AFTER DELETE ON users
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('users', 'DELETE');
        END;
    ''')

    conn.commit()
    conn.close()

def monitor_changes():
    """Überwacht die log_changes-Tabelle und erstellt Backups."""
    last_logged_id = 0  # Speichert das letzte verarbeitete Log

    while True:
        try:
            conn = sqlite3.connect('/home/zvowevan/Projects/Freundschaftsbuch/database.db')
            c = conn.cursor()

            # Prüfe auf neue Einträge in log_changes
            c.execute('SELECT id, table_name, change_type, change_time FROM log_changes WHERE id > ?', (last_logged_id,))
            rows = c.fetchall()

            # Wenn neue Einträge gefunden werden
            if rows:
                for row in rows:
                    print(f"Log erkannt: {row}")
                    last_logged_id = row[0]  # Aktualisiere die letzte ID

                    # Erstelle ein Backup
                    make_copy()

            conn.close()
        except Exception as e:
            print(f"Fehler bei der Überwachung: {e}")

        time.sleep(5)  # Warte 5 Sekunden, bevor erneut geprüft wird

if __name__ == '__main__':
    # Initialisiere die Datenbank (Tabellen und Trigger erstellen)
    init_db()

    # Starte die Überwachung
    print("Überwachung gestartet. Änderungen in der Datenbank werden protokolliert und Backups erstellt.")
    monitor_changes()
