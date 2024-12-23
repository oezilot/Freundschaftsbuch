# test büro 4


import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create log_changes table
    c.execute('''CREATE TABLE IF NOT EXISTS log_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT,
                    change_type TEXT,
                    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Create a trigger for logging INSERT changes in users table
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_users_insert
        AFTER INSERT ON users
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('users', 'INSERT');
        END;
    ''')

    # Create a trigger for logging UPDATE changes in users table
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_users_update
        AFTER UPDATE ON users
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('users', 'UPDATE');
        END;
    ''')

    # Create a trigger for logging DELETE changes in users table
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_users_delete
        AFTER DELETE ON users
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('users', 'DELETE');
        END;
    ''')

    # Repeat the same for posts table
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_posts_insert
        AFTER INSERT ON posts
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('posts', 'INSERT');
        END;
    ''')

    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_posts_update
        AFTER UPDATE ON posts
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('posts', 'UPDATE');
        END;
    ''')

    c.execute('''
        CREATE TRIGGER IF NOT EXISTS after_posts_delete
        AFTER DELETE ON posts
        BEGIN
            INSERT INTO log_changes (table_name, change_type)
            VALUES ('posts', 'DELETE');
        END;
    ''')

    conn.commit()
    conn.close()

init_db()
