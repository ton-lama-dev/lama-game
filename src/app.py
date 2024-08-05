from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


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
    app.run(debug=True)