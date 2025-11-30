from app import app
from flask import render_template

@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Моє Резюме")