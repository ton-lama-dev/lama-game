from quart import Quart, request, jsonify, render_template
from quart_cors import cors
import telegram
from telegram import Bot, error
from datetime import datetime
from random import randint
import database as db
import config as cf

app = Quart(__name__)
cors(app)

bot = Bot(token=cf.BOT_TOKEN)


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/main")
async def master():
    user_id = int(request.args.get("user_id"))
    referrer_id = int(request.args.get("referrer_id")) if request.args.get("referrer_id") != "null" and request.args.get("referrer_id") != None and request.args.get("referrer_id") != user_id else 0
    name = request.args.get("name")
    if db.is_new(user_id):
        db.register_user(user_id=user_id, referrer_id=referrer_id, name=name)

    energy_available = db.get("energy_available", user_id=user_id) + get_refilled_energy(user_id=user_id)
    energy_level = db.get(item="energy_level", user_id=user_id)
    energy_max = energy_level * cf.ENERGY_LEVELS[energy_level - 1]
    tap_power = cf.TAP_LEVELS[int(db.get(item="tap_level", user_id=user_id)) - 1]
    if energy_available >= energy_max:
        energy_available = energy_max
    balance = db.get("balance", user_id=user_id)
    db.login_user(user_id=user_id)
    return await render_template("main.html", energy_available=energy_available, energy_max=energy_max, balance=balance, tap_power=tap_power)

def get_refilled_energy(user_id: int) -> int:
    current_time = datetime.utcnow().replace(microsecond=0)
    last_login_time = datetime.strptime(db.get(item="last_login", user_id=user_id), "%Y-%m-%d %H:%M:%S")
    time_difference_seconds = (current_time - last_login_time).total_seconds()
    refill_level = db.get(item="refill_level", user_id=user_id)
    return round(time_difference_seconds * refill_level * cf.REFILL_LEVELS[refill_level - 1])


@app.route("/friends")
async def friends():
    user_id = int(request.args.get("user_id"))
    revenue_percent = int(db.get(item="revenue_percent", user_id=user_id))
    data = dict()
    friends_ids = db.get_friends_ids(user_id=user_id)
    for id in friends_ids:
        revenue = int(round(db.get(item="balance", user_id=id) / 100 * revenue_percent))
        name = db.get(item="name", user_id=id)
        data[id] = {"revenue": revenue,
                    "name": name}
    return await render_template("friends.html", data=data, revenue_percent=revenue_percent)


@app.route("/upgrade")
async def upgrade():
    user_id = int(request.args.get("user_id"))
    balance = db.get("balance", user_id=user_id)
    tap_level = db.get("tap_level", user_id=user_id)
    energy_level = db.get("energy_level", user_id=user_id)
    refill_level = db.get("refill_level", user_id=user_id)
    tap_upgrade_price = cf.TAP_POWER_UPGRADE_COST[tap_level - 1]
    energy_upgrade_price = cf.ENERGY_UPGRADE_COST[energy_level - 1]
    refill_upgrade_price = cf.REFILL_SPEED_UPGRADE_COST[refill_level - 1]

    return await render_template("upgrade.html", balance=balance, tap_upgrade_price=tap_upgrade_price, energy_upgrade_price=energy_upgrade_price,
                           refill_upgrade_price=refill_upgrade_price, tap_level=tap_level, energy_level=energy_level, refill_level=refill_level)


@app.route("/daily")
async def daily():
    user_id = int(request.args.get("user_id"))
    streak = int(db.get(item="streak", user_id=user_id))
    last_claim_and_today_difference = db.get_last_claim_and_today_difference(user_id=user_id)

    days = dict()
    for i in range(1, 13):
        days[i] = dict()
        if i == streak:
            if streak == 1:
                days[i]["status"] = "active"
                days[i]["reward"] = cf.DAILY_REWARDS[i - 1]
                continue
            elif last_claim_and_today_difference == 1:
                days[i]["status"] = "active"
            elif last_claim_and_today_difference > 1:
                db.set(item="streak", value=1, user_id=user_id)
                days[1]["status"] = "active"
            elif last_claim_and_today_difference == 0:
                days[i]["status"] = "default"
            else:
                days[i]["status"] = "passive"
        elif i < streak:
            days[i]["status"] = "passive"
        else:
            days[i]["status"] = "default"
        days[i]["reward"] = cf.DAILY_REWARDS[i - 1]

    button_status = "enabled" if last_claim_and_today_difference == 1 or streak == 1 else "disabled"

    return await render_template("daily.html", days=days, button_status=button_status)

@app.route('/claim', methods=['POST'])
async def claim():
    data = await request.json
    user_id = int(data.get('user_id'))

    streak = int(db.get(item="streak", user_id=user_id))
    new_streak = streak + 1
    db.set(item="streak", value=new_streak, user_id=user_id)

    balance = int(db.get(item="balance", user_id=user_id))
    num = cf.DAILY_REWARDS[streak - 1]
    new_balance = balance + num
    db.set(item="balance", value=new_balance, user_id=user_id)

    db.set(item="last_claim", value="CURRENT_TIMESTAMP", user_id=user_id)
    if streak >= 12:
        db.set(item="streak", value=1, user_id=user_id)

    referrer_id = int(db.get(item="referrer_id", user_id=user_id))
    if not referrer_id == 0:
        referrer_revenue = int(db.get(item="revenue_percent", user_id=referrer_id))
        referrer_reward = round(num * referrer_revenue / 100)
        db.reward_user(user_id=referrer_id, num=referrer_reward)

    return "200"


@app.route("/tasks")
async def tasks():
    user_id = int(request.args.get("user_id"))
    tasks_ids = db.get_tasks_ids(user_id=user_id)
    data = get_tasks_data(tasks_ids=tasks_ids, user_id=user_id)
    return await render_template("tasks.html", data=data)


def get_tasks_data(tasks_ids: list, user_id=0):
    data = dict()
    if not user_id == 0:
        for id in tasks_ids:
            description = db.tasks_get(item="description", task_id=id)
            name = db.tasks_get(item="name", task_id=id)
            reward = int(db.tasks_get(item="reward", task_id=id))
            link = db.tasks_get(item="link", task_id=id)
            img_link = db.tasks_get(item="img_link", task_id=id)
            task_id = int(db.tasks_get(item="id", task_id=id))
            public_link = db.tasks_get(item="public_link", task_id=id)
            times_done = int(db.tasks_get(item="times_done", task_id=id))
            needs_checking = db.tasks_get(item="needs_checking", task_id=id)
            is_active = db.tasks_get(item="is_active", task_id=id)
            is_done = db.task_is_done(task_id=id, user_id=user_id)
            data[id] = {"description": description,
                        "name": name,
                        "reward": reward,
                        "link": link,
                        "img_link": img_link,
                        "task_id": task_id,
                        "public_link": public_link,
                        "times_done": times_done,
                        "needs_checking": needs_checking,
                        "is_active": is_active,
                        "is_done": is_done}
    else:
        for id in tasks_ids:
            description = db.tasks_get(item="description", task_id=id)
            name = db.tasks_get(item="name", task_id=id)
            reward = int(db.tasks_get(item="reward", task_id=id))
            link = db.tasks_get(item="link", task_id=id)
            img_link = db.tasks_get(item="img_link", task_id=id)
            task_id = int(db.tasks_get(item="id", task_id=id))
            public_link = db.tasks_get(item="public_link", task_id=id)
            times_done = int(db.tasks_get(item="times_done", task_id=id))
            needs_checking = db.tasks_get(item="needs_checking", task_id=id)
            is_active = db.tasks_get(item="is_active", task_id=id)
            data[id] = {"description": description,
                        "name": name,
                        "reward": reward,
                        "link": link,
                        "img_link": img_link,
                        "task_id": task_id,
                        "public_link": public_link,
                        "times_done": times_done,
                        "needs_checking": needs_checking,
                        "is_active": is_active}

    return data

def get_users_data() -> dict:
    raw_data = db.get_users_data()
    balances = list()
    now = datetime.now()
    today, week, month, dau, wau = 0, 0, 0, 0, 0

    for i in raw_data:
        balance = int(i[0])
        last_login = datetime.strptime(i[1], "%Y-%m-%d %H:%M:%S")
        now_and_last_login_difference = (now - last_login).days
        if now_and_last_login_difference <= 1:
            dau += 1
            wau += 1
        elif now_and_last_login_difference <= 6:
            wau += 1
        reg_date = datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S")
        now_and_reg_date_difference = (now - reg_date).days
        if now_and_reg_date_difference == 0:
            today += 1
            week += 1
            month += 1
        elif now_and_reg_date_difference <= 6:
            week += 1
            month += 1
        elif now_and_reg_date_difference <= 30:
            month += 1
        balances.append(balance)

    total_balance = sum(balances)
    number_of_users = len(balances)
    average_balance = total_balance / number_of_users

    result = {"all": number_of_users,
              "today": today,
              "week": week,
              "month": month,
              "dau": dau,
              "wau": wau,
              "total_balance": total_balance,
              "average_balance": average_balance}
    return result


@app.route("/pre-swap")
async def pre_swap():
    return await render_template("pre-swap.html")


@app.route("/swap")
async def swap():
    user_id = int(request.args.get("user_id"))
    
    if db.is_new(user_id):
        db.register_user(user_id=user_id, name="name")
    
    claimed = int(db.bot_get(item="claimed", user_id=user_id))
    bot_balance = int(db.bot_get(item="balance", user_id=user_id))
    reward = int(db.bot_get(item="balance", user_id=user_id) / 100)
    if not claimed:
        return await render_template("swap.html", bot_balance=bot_balance, reward=reward, button_status="active"), 200
    else:
        return await render_template("swap.html", button_status="passive", bot_balance=bot_balance, reward=reward), 200

@app.route('/reward', methods=['POST'])
async def reward():
    data = await request.json
    user_id = int(data.get('user_id'))
    claimed = int(db.bot_get(item="claimed", user_id=user_id))
    if not claimed:
        balance = int(db.get(item="balance", user_id=user_id))
        reward = int(db.bot_get(item="balance", user_id=user_id) / 100)
        new_balance = balance + reward
        db.set(item="balance", value=new_balance, user_id=user_id)
        db.bot_set(item="claimed", value=1, user_id=user_id)
        return "success", 200
    else:
        return "error", 400


@app.route('/check_subscription', methods=['POST'])
async def check_subscription():
    data = await request.json
    user_id = int(data.get('user_id'))
    task_id = int(data.get('task_id'))
    needs_checking = int(db.tasks_get(item="needs_checking", task_id=task_id)) == 1
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    if not needs_checking:
        finish_task(user_id=user_id, task_id=task_id)
        return jsonify({"subscribed": True}), 200

    try:
        public_link = db.get_channel_public_link(task_id=task_id)
        member_status = await bot.get_chat_member(chat_id=public_link, user_id=user_id)
        if member_status.status in ['member', 'administrator', 'creator']:
            finish_task(user_id=user_id, task_id=task_id)
            return jsonify({"subscribed": True}), 200
        else:
            return jsonify({"subscribed": False}), 410
    except error.TelegramError as e:
        return jsonify({"error": str(e)}), 420

def finish_task(user_id: int, task_id: int):
    db.subscribe_user(task_id=task_id, user_id=user_id)
    reward = int(db.tasks_get(item="reward", task_id=task_id))
    db.reward_user(user_id=user_id, num=reward)
    referrer_id = int(db.get(item="referrer_id", user_id=user_id))
    if not referrer_id == 0:
        referrer_revenue = int(db.get(item="revenue_percent", user_id=referrer_id))
        referrer_reward = round(reward * referrer_revenue / 100)
        db.reward_user(user_id=referrer_id, num=referrer_reward)


@app.route("/update", methods=["POST"])
async def update():
    data = await request.json
    user_id = data.get("user_id")
    balance = int(data.get("balance"))
    old_balance = int(db.get(item="balance", user_id=user_id))
    energy_available = data.get("energy_available")
    db.set(item="balance", value=balance, user_id=user_id)
    db.set(item="energy_available", value=energy_available, user_id=user_id)
    referrer_id = int(db.get(item="referrer_id", user_id=user_id))
    if not referrer_id == 0:
        difference = balance - old_balance
        referrer_revenue = int(db.get(item="revenue_percent", user_id=referrer_id))
        referrer_reward = round(difference * referrer_revenue / 100)
        db.reward_user(user_id=referrer_id, num=referrer_reward)
    return "200"


@app.route("/UQBg5Ame1AjU9wp0DhyAHPvgSgj6fsQWxquA25DNq_gO8kpE")
async def admin():
    tasks_ids = db.get_all_tasks_ids()
    data = get_tasks_data(tasks_ids=tasks_ids)
    users = get_users_data()
    return await render_template("admin.html", data=data, users=users)


@app.route("/upgrade_tap", methods=["POST"])
async def upgrade_tap():
    data = await request.json
    user_id = data.get("user_id")
    db.upgrade_tap(user_id=user_id)
    return "200"


@app.route("/upgrade_energy", methods=["POST"])
async def upgrade_energy():
    data = await request.json
    user_id = data.get("user_id")
    db.upgrade_energy(user_id=user_id)
    return "200"


@app.route("/upgrade_refill", methods=["POST"])
async def upgrade_refill():
    data = await request.json
    user_id = data.get("user_id")
    db.upgrade_refill(user_id=user_id)
    return "200"


@app.route("/add_task", methods=["POST"])
async def add_task():
    form_data = await request.form
    password = form_data.get("password")
    description = form_data.get('description')
    name = form_data.get('name')
    reward = int(form_data.get('reward'))
    public_link = form_data.get('public_link')
    link = form_data.get('link')
    img_link = form_data.get('img_link')
    needs_checking = int('needs_checking' in form_data)
    id = randint(111111, 999999)

    if password == cf.ADMIN_PASS:
        db.add_task(id=id, description=description, name=name, reward=reward, public_link=public_link,
                    link=link, img_link=img_link, needs_checking=needs_checking)
        return "<h1>task added successfully</h1>"
    return "<h1>error</h1>"

@app.route("/delete_task", methods=["POST"])
async def delete_task():
    form_data = await request.form
    password = form_data.get("password")
    task_id = int(form_data.get("task_id"))

    if password == cf.ADMIN_PASS:
        try:
            db.del_task(id=task_id)
            return "<h1>task deleted successfully</h1>"
        except:
            return "<h1>database error</h1>"
    return "<h1>error</h1>"

@app.route("/set_revenue", methods=["POST"])
async def set_revenue():
    form_data = await request.form
    password = form_data.get("password")
    user_id = int(form_data.get("user_id"))
    new_revenue = int(form_data.get("percent"))

    if password == cf.ADMIN_PASS:
        try:
            db.set(item="revenue_percent", value=new_revenue, user_id=user_id)
            return "<h1>revenue set successfully</h1>"
        except:
            return "<h1>database error</h1>"
    return "<h1>error</h1>"

@app.route("/db_set", methods=["POST"])
async def db_set():
    form_data = await request.form
    password = form_data.get("password")
    id = int(form_data.get("user_id"))
    table = form_data.get("table")
    column = form_data.get("column")
    value = form_data.get("value")
    print(value)

    if password == cf.ADMIN_PASS:
        # try:
            if table == "tasks":
                db.tasks_set(item=column, value=value, task_id=id)
            elif table == "users":
                db_set(item=column, value=value, user_id=id)
            else:
                return "<h1>there is no such table</h1>"
            return "<h1>revenue set successfully</h1>"
        # except Exception as e:
        #     print(e)
        #     return "<h1>database error</h1>"
    return "<h1>error</h1>"
    

if __name__ == "__main__":
    db.init_db()
    while True:
        try:
            app.run(debug=True)
        except Exception as e:
            print("Exception it the main loop:")
            print(e)
