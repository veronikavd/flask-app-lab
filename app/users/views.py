from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import user_bp

USER_DATA = {
    "username": "admin",
    "password": "123"
}

@user_bp.route("/hi/<string:name>")
def greetings(name):
    return render_template("users/hi.html", name=name)

@user_bp.route("/admin")
def admin():
    return redirect(url_for("users.greetings", name="administrator", age=45))



@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("users.profile"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER_DATA["username"] and password == USER_DATA["password"]:
            session["username"] = username
            flash("Ви успішно увійшли!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірний логін або пароль", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html")


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи", "info")
    return redirect(url_for("users.login"))


@user_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Будь ласка, увійдіть спочатку", "warning")
        return redirect(url_for("users.login"))
    
    return render_template("users/profile.html", username=session["username"])


@user_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    max_age = request.form.get("max_age", type=int) or 3600

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, max_age=max_age)
    flash(f"Кукі '{key}' додано успішно!", "success")
    return resp


@user_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    key = request.form.get("key")
    resp = make_response(redirect(url_for("users.profile")))
    
    if key == "ALL":
        for cookie_key in request.cookies:
            if cookie_key != 'session':
                resp.set_cookie(cookie_key, '', expires=0)
        flash("Всі кукі видалено!", "warning")
    else:
        resp.set_cookie(key, '', expires=0)
        flash(f"Кукі '{key}' видалено!", "info")
        
    return resp


@user_bp.route("/change_theme/<theme>")
def change_theme(theme):
    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("theme", theme)
    return resp