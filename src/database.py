import sqlite3

import config as cf


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


def add_task(id: int, description: str, name: str, reward: int,
             link: str, img_link: str, needs_checking: int, public_link: str):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (id, public_link, description, name, reward, link, img_link, needs_checking) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (id, public_link, description, name, reward, link, img_link, needs_checking))
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


def upgrade_tap(user_id: int) -> bool:
    with connect_db() as conn:
        cursor = conn.cursor()
        old_level = cursor.execute("SELECT tap_level FROM users WHERE tg_id = ?", (user_id, ))
        old_level = cursor.fetchone()[0]
        upgrade_price = cf.TAP_POWER_UPGRADE_COST[old_level - 1]
        balance = int(get(item="balance", user_id=user_id))
        if balance < upgrade_price:
            return False
        cursor.execute("UPDATE users SET tap_level = ? WHERE tg_id = ?", (old_level + 1, user_id))
        cursor.execute("UPDATE users SET balance = ? WHERE tg_id = ?", (balance - upgrade_price, user_id))
        conn.commit()
        return True
    
def upgrade_energy(user_id: int) -> bool:
    with connect_db() as conn:
        cursor = conn.cursor()
        old_level = cursor.execute("SELECT energy_level FROM users WHERE tg_id = ?", (user_id, ))
        old_level = cursor.fetchone()[0]
        upgrade_price = cf.ENERGY_UPGRADE_COST[old_level - 1]
        balance = int(get(item="balance", user_id=user_id))
        if balance < upgrade_price:
            return False
        cursor.execute("UPDATE users SET energy_level = ? WHERE tg_id = ?", (old_level + 1, user_id))
        cursor.execute("UPDATE users SET balance = ? WHERE tg_id = ?", (balance - upgrade_price, user_id))
        conn.commit()
        return True
    
def upgrade_refill(user_id: int) -> bool:
    with connect_db() as conn:
        cursor = conn.cursor()
        old_level = cursor.execute("SELECT refill_level FROM users WHERE tg_id = ?", (user_id, ))
        old_level = cursor.fetchone()[0]
        upgrade_price = cf.REFILL_SPEED_UPGRADE_COST[old_level - 1]
        balance = int(get(item="balance", user_id=user_id))
        if balance < upgrade_price:
            return False
        cursor.execute("UPDATE users SET refill_level = ? WHERE tg_id = ?", (old_level + 1, user_id))
        cursor.execute("UPDATE users SET balance = ? WHERE tg_id = ?", (balance - upgrade_price, user_id))
        conn.commit()
        return True


def get_friends_ids(user_id: int) -> list[int]:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tg_id FROM users WHERE referrer_id = ?", (user_id, ))
        data = cursor.fetchall()
        result = [i[0] for i in data]
        return result


def get_tasks_ids(user_id: int) -> list[int]:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks WHERE is_active = ?", (1, ))
        data = cursor.fetchall()
        result = [i[0] for i in data]

        return result


def get_all_tasks_ids() -> list[int]:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks")
        data = cursor.fetchall()
        result = [i[0] for i in data]

        return result


def get_channel_public_link(task_id: int) -> str:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT public_link FROM tasks WHERE id = ?", (task_id, ))
        return cursor.fetchone()[0]


def get(item: str, user_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {item} FROM users WHERE tg_id = ?", (user_id, ))
        return cursor.fetchone()[0]

def tasks_get(item: str, task_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {item} FROM tasks WHERE id = ?", (task_id, ))
        return cursor.fetchone()[0]

def set(item: str, value, user_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {item} = {value} WHERE tg_id = ?", (user_id, ))
        conn.commit()
