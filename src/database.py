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
                       done_tasks TEXT DEFAULT '',
                       streak INTEGER DEFAULT 0,
                       last_claim DATETIME DEFAULT '2000-01-01 00:00:00',
                       last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
                       tap_level INTEGER DEFAULT 1,
                       energy_level INTEGER DEFAULT 1,
                       refill_level INTEGER DEFAULT 1)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                       description TEXT DEFAULT 'follow in telegram',
                       name TEXT,
                       reward INTEGER,
                       link TEXT,
                       img_link TEXT,
                       needs_checking INTEGER DEFAULT 0,
                       is_active INTEGER DEFAULT 0)""")
        conn.commit()


def register_user(user_id, referrer_id=0, name="name"):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (tg_id, referrer_id, name) VALUES (?, ?, ?)", (user_id, referrer_id, name))
        conn.commit()


def login_user(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE tg_id = ?", (user_id, ))
        conn.commit()


def is_new(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tg_id FROM users WHERE tg_id = ?", (user_id, ))
        result = cursor.fetchone()
        return result == None


def get_friends_ids(user_id: int) -> list[int]:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tg_id FROM users WHERE referrer_id = ?", (user_id, ))
        data = cursor.fetchall()
        print("data:", data)
        result = [i[0] for i in data]
        print("result", result)
        return result


def get(item: str, user_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {item} FROM users WHERE tg_id = ?", (user_id, ))
        return cursor.fetchone()[0]


def set(item: str, value, user_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {item} = {value} WHERE tg_id = ?", (user_id, ))
        conn.commit()
