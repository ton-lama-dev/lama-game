import sqlite3


def connect_db():
    return sqlite3.connect("data.db")


def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                       tg_id INTEGER PRIMARY KEY,
                       balance INTEGER DEFAULT 0,
                       energy_available INTEGER DEFAULT 944,
                       referrer_id INTEGER,
                       reg_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                       done_tasks TEXT DEFAULT '',
                       streak INTEGER DEFAULT 0,
                       last_claim TIMESTAMP DEFAULT '2000-01-01 00:00:00',
                       last_login TIMESTAMP DEFAULT '2000-01-01 00:00:00',
                       tap_power INTEGER DEFAULT 1,
                       energy_level INTEGER DEFAULT 1,
                       refill_speed INTEGER DEFAULT 1)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                       description TEXT DEFAULT 'follow in telegram',
                       name TEXT,
                       reward INTEGER,
                       link TEXT,
                       img_link TEXT,
                       needs_checking INTEGER DEFAULT 0,
                       is_active INTEGER DEFAULT 0)""")
        conn.commit()


def register_user(user_id, referrer_id=0):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (tg_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id))
        conn.commit()


def is_new(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tg_id FROM users WHERE tg_id = ?", (user_id, ))
        result = cursor.fetchone()
        return result == None


def get(item, user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {item} FROM users WHERE tg_id = ?", (user_id, ))
        return cursor.fetchone()[0]
