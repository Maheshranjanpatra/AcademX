from flask import Blueprint, render_template
from flask import send_from_directory, current_app

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/about")
def about():
    return render_template("about.html")

@pages_bp.route("/contact")
def contact():
    return render_template("contact.html")

@pages_bp.route("/policy")
def policy():
    return render_template("policy.html")

@pages_bp.route("/offline")
def offline():
    return render_template("offline.html")
    
@pages_bp.route("/sw.js")
def service_worker():
    return send_from_directory(current_app.static_folder, "sw.js", mimetype="application/javascript")
