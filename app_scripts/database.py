# init the databse or do other actions

import sqlite3


# ---------------------------
# |        Datenbank        | 2 tabellen kreieren (usertabelle, posts)
# ---------------------------

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # FOLGENDE ZEILEN AUSKOMMENTIEREN WENN MAN DIE DATENBANK WIPEN MÖCHTE
    #c.execute('DROP TABLE IF EXISTS users')
    #c.execute('DROP TABLE IF EXISTS posts')

    # Create users table with 'is_active' column for soft deletion
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    reset_token TEXT,
                    username TEXT UNIQUE,
                    password TEXT,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER DEFAULT -1,
                    is_admin BOOLEAN DEFAULT 0)''')  # Default is_active = 1 (active)

    # Create posts table with 'is_active' column for soft deletion
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT,
                    birthday TEXT, 
                    color TEXT, 
                    food TEXT, 
                    greenFlags TEXT, 
                    redFlags TEXT,
                    pinterest TEXT,
                    Name TEXT,
                    Personnality TEXT, 
                    Zoe TEXT, 
                    Interest TEXT, 
                    Desinterest TEXT, 
                    Lernen TEXT, 
                    Idol TEXT, 
                    Serie TEXT, 
                    Musik TEXT, 
                    Fashion TEXT, 
                    Zukunft TEXT, 
                    Love TEXT, 
                    Date TEXT, 
                    Pleasure TEXT,
                    Regret TEXT, 
                    Party_Movie TEXT,
                    Ski_Snowboard TEXT,
                    Wg_Alleine TEXT,
                    Hund_Katze TEXT,
                    Regen_Sonne TEXT,
                    Spotify TEXT,
                    image_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()



# ---------------------------------
# |        Helperfunctions        | 
# ---------------------------------

# Helper function to get DB connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn