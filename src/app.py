from flask import Flask, render_template, request

import database


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
def main():
    user_id = request.args.get("user_id")
    if database.is_new(user_id):
        database.register_user(user_id=user_id)
    energy_available = database.get("energy_available", user_id=user_id)
    energy_max = database.get("energy_level", user_id=user_id) * 1000
    balance = database.get("balance", user_id=user_id)
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


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)