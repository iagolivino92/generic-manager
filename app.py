from flask import Flask, render_template, request, redirect, url_for, session
import json
from services.budget import calculate_budget

# Load config
with open("config.json") as f:
    config = json.load(f)

# Load config
with open("language.json") as f:
    translations = json.load(f)

USERS = config["users"]
SERVICES = config["services"]
SETTINGS = config["settings"]
TRANSLATIONS = translations

app = Flask(__name__)
app.secret_key = SETTINGS.get("secret_key")


@app.route("/en", methods=["GET"])
def set_english():
    session["lang"] = 'en'
    return redirect(request.referrer)


@app.route("/pt", methods=["GET"])
def set_portuguese():
    session["lang"] = 'pt'
    return redirect(request.referrer)


@app.route("/", methods=["GET", "POST"])
def login():
    if session.get('lang') is None:
        session["lang"] = 'en'
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        if nickname in USERS and USERS[nickname] == password:
            session["user"] = nickname
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid credentials",
                               translations=TRANSLATIONS.get(session.get('lang', 'en')))
    if session.get("user") is not None:
        return redirect(url_for("home"))
    return render_template("login.html", translations=TRANSLATIONS.get(session.get('lang', 'en')))


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", services=SERVICES, translations=TRANSLATIONS.get(session.get('lang', 'en')))


@app.route("/budget", methods=["GET", "POST"])
def budget():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    if request.method == "POST":
        data = {k: float(v) if v and not isinstance(v, str) else v for k, v in request.form.items()}
        result = calculate_budget(data, SETTINGS, translations=TRANSLATIONS.get(session.get('lang', 'en')))

    return render_template("budget.html", result=result, translations=TRANSLATIONS.get(session.get('lang', 'en')))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
