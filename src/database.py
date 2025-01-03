import sqlite3

import config as cf


def connect_db():
    return sqlite3.connect("data.db")

def connect_bot_db():
    return sqlite3.connect("bot.db")


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


def add_task(id: int, description: str, name: str, reward: int,
             link: str, img_link: str, needs_checking: int, public_link: str):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (id, public_link, description, name, reward, link, img_link, needs_checking) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (id, public_link, description, name, reward, link, img_link, needs_checking))
        conn.commit()

def del_task(id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (id, ))
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


def task_is_done(task_id: int, user_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT done_tasks FROM users WHERE tg_id = ?", (user_id, ))
        string = cursor.fetchone()[0]
        if string:
            done_tasks = [int(num) for num in string.split(',')]
            return task_id in done_tasks


def subscribe_user(task_id: int, user_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT done_tasks FROM users WHERE tg_id = ?", (user_id, ))
        done_tasks_old = cursor.fetchone()[0]

        cursor.execute("SELECT times_done FROM tasks WHERE id = ?", (task_id, ))
        times_done_old = cursor.fetchone()[0]
        times_done_new = times_done_old + 1
        cursor.execute("UPDATE tasks SET times_done = ? WHERE id = ?", (times_done_new, task_id))

        done_tasks_new = done_tasks_old + "," + str(task_id)
        cursor.execute("UPDATE users SET done_tasks = ? WHERE tg_id = ?", (done_tasks_new, user_id))

        conn.commit()


def reward_user(user_id: int, num: int) -> None:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE tg_id = ?", (user_id, ))
        current_balance = int(cursor.fetchone()[0])
        new_balance = current_balance + num
        cursor.execute("UPDATE users SET balance = ? WHERE tg_id = ?", (new_balance, user_id))
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


def get_last_claim_and_today_difference(user_id: int) -> int:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT JULIANDAY('now') - JULIANDAY(last_claim) AS days_difference FROM users WHERE tg_id = ?", (user_id, ))
        result = int(cursor.fetchone()[0])
        return result


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


def get_users_data() -> tuple:
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance, last_login, reg_date FROM users")
        data = cursor.fetchall()

        return data


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


def bot_get(item: str, user_id: int) -> any:
    with connect_bot_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {item} FROM rewards WHERE id = ?", (user_id, ))
        result = cursor.fetchone()
        return result[0] if result else None
    
def bot_set(item: str, value: any, user_id: int):
    with connect_bot_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE rewards SET {item} = {value} WHERE id = ?", (user_id, ))
        conn.commit()


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

def tasks_set(item: str, value, task_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE tasks SET {item} = ? WHERE id = ?", (value, task_id))
        conn.commit()


def set(item: str, value, user_id: int):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {item} = {value} WHERE tg_id = ?", (user_id, ))
        conn.commit()
