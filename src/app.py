from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"


@app.route("/friends")
def friends():
    return render_template("friends.html")


if __name__ == "__main__":
    app.run(debug=True)