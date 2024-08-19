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
    if energy_available >= energy_max:
        energy_available = energy_max
    balance = db.get("balance", user_id=user_id)
    db.login_user(user_id=user_id)
    return await render_template("main.html", energy_available=energy_available, energy_max=energy_max, balance=balance)

def get_refilled_energy(user_id: int) -> int:
    current_time = datetime.utcnow().replace(microsecond=0)
    last_login_time = datetime.strptime(db.get(item="last_login", user_id=user_id), "%Y-%m-%d %H:%M:%S")
    time_difference_seconds = (current_time - last_login_time).total_seconds()
    refill_level = db.get(item="refill_level", user_id=user_id)
    return round(time_difference_seconds * refill_level * cf.REFILL_LEVELS[refill_level - 1])

@app.route("/friends")
async def friends():
    user_id = int(request.args.get("user_id"))
    data = dict()
    friends_ids = db.get_friends_ids(user_id=user_id)
    for id in friends_ids:
        revenue = round(db.get(item="balance", user_id=id) / 100 * int(db.get(item="revenue_percent", user_id=user_id)))
        name = db.get(item="name", user_id=id)
        data[id] = {"revenue": revenue,
                    "name": name}
    return await render_template("friends.html", data=data)

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
    return await render_template("daily.html")

@app.route("/tasks")
async def tasks():
    user_id = int(request.args.get("user_id"))
    tasks_ids = db.get_tasks_ids(user_id=user_id)
    data = get_tasks_data(tasks_ids=tasks_ids)
    return await render_template("tasks.html", data=data)

def get_tasks_data(tasks_ids: list):
    data = dict()
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

@app.route('/check_subscription', methods=['POST'])
async def check_subscription():
    data = await request.json
    user_id = int(data.get('user_id'))
    task_id = int(data.get('task_id'))
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        public_link = db.get_channel_public_link(task_id=task_id)
        member_status = await bot.get_chat_member(chat_id=public_link, user_id=user_id)
        print(member_status.status)
        if member_status.status in ['member', 'administrator', 'creator']:
            return jsonify({"subscribed": True}), 200
        else:
            return jsonify({"subscribed": False}), 410
    except error.TelegramError as e:
        return jsonify({"error": str(e)}), 420

@app.route("/update", methods=["POST"])
async def update():
    data = await request.json
    user_id = data.get("user_id")
    balance = data.get("balance")
    energy_available = data.get("energy_available")
    db.set(item="balance", value=balance, user_id=user_id)
    db.set(item="energy_available", value=energy_available, user_id=user_id)
    return "200"

@app.route("/admin")
async def admin():
    tasks_ids = db.get_all_tasks_ids()
    data = get_tasks_data(tasks_ids=tasks_ids)
    return await render_template("admin.html", data=data)

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
    password = request.form.get("password")
    description = request.form.get('description')
    name = request.form.get('name')
    reward = int(request.form.get('reward'))
    public_link = request.form.get('public_link')
    link = request.form.get('link')
    img_link = request.form.get('img_link')
    needs_checking = int('needs_checking' in request.form)
    id = randint(111111, 999999)
    if password == cf.ADMIN_PASS:
        db.add_task(id=id, description=description, name=name, reward=reward, public_link=public_link,
                    link=link, img_link=img_link, needs_checking=needs_checking)
        return "<h1>task added successfully</h1>"
    return "<h1>error</h1>"

if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
