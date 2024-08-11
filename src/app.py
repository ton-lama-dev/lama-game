from flask import Flask, render_template, request
from flask_cors import CORS

import database as db


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
def master():
    user_id = int(request.args.get("user_id"))
    referrer_id = int(request.args.get("referrer_id")) if request.args.get("referrer_id") != "null" else 0
    if db.is_new(user_id):
        db.register_user(user_id=user_id, referrer_id=referrer_id)
    db.login_user(user_id=user_id)

    energy_available = db.get("energy_available", user_id=user_id)
    energy_max = db.get("energy_level", user_id=user_id) * 1000
    balance = db.get("balance", user_id=user_id)
    return render_template("main.html", energy_available=energy_available, energy_max=energy_max, balance=balance,
                           )


@app.route("/friends")
def friends():
    friends = [{
        "name": "bruh1",
        "revenue": 1.89
    }, 
    {
        "name": "bruh2",
        "revenue": 0.31
    }, 
    {
        "name": "bruh3",
        "revenue": 12
    }]
    return render_template("friends.html", friends=friends)


@app.route("/upgrade")
def upgrade():
    return render_template("upgrade.html")


@app.route("/daily")
def daily():
    return render_template("daily.html")


@app.route("/tasks")
def tasks():
    return render_template("tasks.html")


@app.route("/exit", methods=["POST"])
def exit():
    data = request.json
    user_id = data.get("user_id")
    balance = data.get("balance")
    db.set(item="balance", value=balance, user_id=user_id)
    return "200"


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)