
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("myForm.html")


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("pwd", "")

    if not username:
        return "Username cannot be empty.", 400

    if not password:
        return "Password cannot be empty.", 400

    if len(password) < 6:
        return "Password must be at least 6 characters long.", 400

    return render_template("greeting.html", username=username)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
