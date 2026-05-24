from flask import Flask, jsonify
from flask_login import LoginManager
import models
import os
from extensions import socketio

# Import Blueprints
from blueprints.views import views_bp
from blueprints.auth import auth_bp
from blueprints.goals import goals_bp
from blueprints.initiatives import initiatives_bp
from blueprints.webhooks import webhooks_bp
from blueprints.habits import habits_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-default-key-for-flashes")

from flask_socketio import join_room, leave_room
from flask_login import current_user

# Initialize SocketIO
socketio.init_app(app)

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('join')
def on_join(data):
    user_id = data.get('user_id')
    if user_id:
        join_room(str(user_id))

@socketio.on('disconnect')
def handle_disconnect():
    pass

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized"}), 401


@login_manager.user_loader
def load_user(user_id):
    return models.get_user_by_id(user_id)


# Register Blueprints
app.register_blueprint(views_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(initiatives_bp)
app.register_blueprint(webhooks_bp)
app.register_blueprint(habits_bp)

# Ensure DB is initialized before first request
with app.app_context():
    models.init_db()


def get_db_path():
    """Temporary backwards compatibility function. `models.get_db_url` handles the actual config."""
    return os.getenv("DATABASE_PATH", "goals.db")


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
