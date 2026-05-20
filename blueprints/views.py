from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

def get_app_version():
    try:
        with open("VERSION.md", "r") as f:
            return f.read().strip()
    except Exception:
        return "unknown"

@views_bp.route("/")
def index():
    """Serve the single page application."""
    return render_template("spa.html", app_version=get_app_version())
