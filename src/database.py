import sqlite3


def connect_db():
    return sqlite3.connect("data.db")


def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                       td_id INTEGER PRIMARY KEY,
                       balance INTEGER DEFAULT 0,
                       referrer_id INTEGER,
                       reg_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                       done_tasks TEXT,
                       streak INTEGER DEFAULT 0,
                       last_claim TIMESTAMP,
                       tap_power INTEGER DEFAULT 1,
                       energy INTEGER DEFAULT 1,
                       refill_speed INTEGER DEFAULT 1)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                       type TEXT DEFAULT 'follow in telegram',
                       name TEXT,
                       reward INTEGER,
                       link TEXT,
                       img_link TEXT,
                       needs_checking INTEGER DEFAULT 0,
                       is_active INTEGER DEFAULT 0)""")