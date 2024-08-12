from flask import Flask, render_template, request
from flask_cors import CORS

from datetime import datetime

import database as db
import config as cf


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
def master():
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
    return render_template("main.html", energy_available=energy_available, energy_max=energy_max, balance=balance)

def get_refilled_energy(user_id: int) -> int:
    current_time = datetime.utcnow().replace(microsecond=0)
    last_login_time = datetime.strptime(db.get(item="last_login", user_id=user_id), "%Y-%m-%d %H:%M:%S")
    time_difference_seconds = (current_time - last_login_time).total_seconds()
    refill_level = db.get(item="refill_level", user_id=user_id)
    return round(time_difference_seconds * refill_level * cf.REFILL_LEVELS[refill_level - 1])


@app.route("/friends")
def friends():
    user_id = int(request.args.get("user_id"))
    data = dict()
    friends_ids = db.get_friends_ids(user_id=user_id)
    print("friends ids:", friends_ids)
    for id in friends_ids:
        revenue = round(db.get(item="balance", user_id=id) / 100 * int(db.get(item="revenue_percent", user_id=user_id)))
        name = db.get(item="name", user_id=id)
        data[id] = {"revenue": revenue,
                    "name": name}
    print(data)
    return render_template("friends.html", data=data)


@app.route("/upgrade")
def upgrade():
    return render_template("upgrade.html")


@app.route("/daily")
def daily():
    return render_template("daily.html")


@app.route("/tasks")
def tasks():
    return render_template("tasks.html")


@app.route("/update", methods=["POST"])
def exit():
    data = request.json
    user_id = data.get("user_id")
    balance = data.get("balance")
    energy_available = data.get("energy_available")
    db.set(item="balance", value=balance, user_id=user_id)
    db.set(item="energy_available", value=energy_available, user_id=user_id)
    return "200"


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)