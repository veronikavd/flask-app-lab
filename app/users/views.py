from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import user_bp
from .forms import ContactForm, LoginForm
import json

USER_DATA = {
    "username": "admin",
    "password": "12345"
}

@user_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        log_data = {
            "name": form.name.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "subject": form.subject.data,
            "message": form.message.data
        }
        
        try:
            with open("form_log.txt", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
            flash(f"Повідомлення від {form.name.data} успішно надіслано!", "success")
        except Exception as e:
            flash(f"Помилка запису в лог: {e}", "danger")
            
        return redirect(url_for("users.contact"))
        
    return render_template("contacts.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("users.profile"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == USER_DATA["username"] and password == USER_DATA["password"]:
            session["username"] = username
            flash(f"Ви успішно увійшли! Запам'ятати мене: {remember}", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірний логін або пароль", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html", form=form)


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

@user_bp.route("/hi/<string:name>")
def greetings(name):
    return render_template("users/hi.html", name=name)

@user_bp.route("/admin")
def admin():
    return redirect(url_for("users.greetings", name="administrator", age=45))

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