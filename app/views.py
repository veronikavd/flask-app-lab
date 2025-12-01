from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/resume")
def resume():
    return render_template("resume.html", title="Моє Резюме")