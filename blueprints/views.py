from flask import Blueprint, send_from_directory
import os

views_bp = Blueprint('views', __name__)

@views_bp.route("/", defaults={'path': ''})
@views_bp.route("/<path:path>")
def serve_vue_app(path):
    """Serve the compiled Vue application and its static assets."""
    # Assuming Vite builds to 'dist' directory at the project root
    dist_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')

    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)

    return send_from_directory(dist_dir, 'index.html')
