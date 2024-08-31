import sqlite3


def connect_db():
    return sqlite3.connect("data.db")


def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                       tg_id INTEGER PRIMARY KEY,
                       name TEXT,
                       balance INTEGER DEFAULT 0,
                       energy_available INTEGER DEFAULT 1000,
                       referrer_id INTEGER,
                       revenue_percent INTEGER DEFAULT 20,
                       reg_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                       done_tasks TEXT DEFAULT '1',
                       streak INTEGER DEFAULT 1,
                       last_claim DATETIME DEFAULT '2000-01-01 00:00:00',
                       last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
                       tap_level INTEGER DEFAULT 1,
                       energy_level INTEGER DEFAULT 1,
                       refill_level INTEGER DEFAULT 1)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                       id INTEGER PRIMARY KEY,
                       public_link TEXT,
                       times_done INTEGER DEFAULT 0,
                       description TEXT DEFAULT 'follow in telegram',
                       name TEXT,
                       reward INTEGER,
                       link TEXT,
                       img_link TEXT,
                       needs_checking INTEGER DEFAULT 0,
                       is_active INTEGER DEFAULT 1)""")
        conn.commit()


init_db()
