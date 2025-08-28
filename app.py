from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
from services.budget import calculate_budget
from utils.decorators import login_required
from utils.users import create_or_update_user


def load_configs():
    # Load config
    with open("config.json") as f:
        config_ = json.load(f)
    # Load translations
    with open("language.json") as f:
        translations_ = json.load(f)
    return config_, translations_


config, translations = load_configs()
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
        if nickname in USERS and USERS[nickname].get('password') == password:
            session["user"] = nickname
            session["role"] = USERS[nickname].get('role')
            return redirect(url_for("home"))
        return render_template("login.html", error=TRANSLATIONS.get(session.get('lang', 'en'))
                               .get('errors').get('invalid_credentials'),
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
@login_required
def budget():
    result = None
    if request.method == "POST":
        data = {k: float(v) if v and not isinstance(v, str) else v for k, v in request.form.items()}
        result = calculate_budget(data, SETTINGS, translations=TRANSLATIONS.get(session.get('lang', 'en')))

    return render_template("budget.html", result=result, translations=TRANSLATIONS.get(session.get('lang', 'en')))


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        role = request.form.get("role", "read")
        if not nickname or not password:
            flash("Nickname and Password are required", "error")
        else:
            create_or_update_user(nickname, password, role)
            reload_configs()
            flash(f"User '{nickname}' created/updated successfully.", "success")
    return render_template("user_form.html", translations=TRANSLATIONS.get(session.get('lang', 'en')))



@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("role", None)
    return redirect(url_for("login"))


@app.route("/reload-configs")
def reload_configs():
    global USERS, SERVICES, SETTINGS, TRANSLATIONS
    config_, translations_ = load_configs()
    USERS = config_["users"]
    SERVICES = config_["services"]
    SETTINGS = config_["settings"]
    TRANSLATIONS = translations_
    return {"status": "OK", "message": "configs reloaded"}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
