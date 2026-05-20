from flask import Flask, request, render_template, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from notifications import notify_all
import models
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-default-key-for-flashes")
socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized"}), 401

@login_manager.user_loader
def load_user(user_id):
    return models.get_user_by_id(user_id)

# Ensure DB is initialized before first request
with app.app_context():
    models.init_db()

def get_app_version():
    try:
        with open("VERSION.md", "r") as f:
            return f.read().strip()
    except Exception:
        return "unknown"

def get_db_path():
    """Temporary backwards compatibility function. `models.get_db_url` handles the actual config."""
    return os.getenv("DATABASE_PATH", "goals.db")

# --- SPA Root Route ---
@app.route("/")
def index():
    """Serve the single page application."""
    return render_template("spa.html", app_version=get_app_version())

# --- JSON API Endpoints ---

@app.route("/api/me", methods=['GET'])
def api_me():
    if current_user.is_authenticated:
        return jsonify({"authenticated": True, "username": current_user.username})
    return jsonify({"authenticated": False})

@app.route("/api/login", methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    user = models.get_user_by_username(username)
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in successfully."})
    return jsonify({"error": "Invalid username or password."}), 401

@app.route("/api/register", methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password required."}), 400
    if models.get_user_by_username(username):
        return jsonify({"error": "Username already exists."}), 409

    user_id = models.create_user(username, password)
    if user_id:
        return jsonify({"message": "Registration successful."}), 201
    return jsonify({"error": "Registration failed."}), 500

@app.route("/api/logout", methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out successfully."})

@app.route("/api/goals", methods=['GET'])
@login_required
def api_get_goals():
    goals = models.list_pending_goals(user_id=current_user.id)
    return jsonify({"goals": [{"id": g[0], "description": g[1]} for g in goals]})

@app.route("/api/goals", methods=['POST'])
@login_required
def api_add_goal():
    data = request.get_json() or {}
    description = data.get("description")
    if description:
        goal_id = models.add_goal(description, user_id=current_user.id)
        notify_all(
            subject="New Goal Added",
            body=f"You added a new goal: {description}",
            speakable_message=f"You added a new goal: {description}"
        )
        socketio.emit('data_updated', {"message": "Goal added"})
        return jsonify({"message": "Goal added.", "id": goal_id}), 201
    return jsonify({"error": "Description required."}), 400

@app.route("/api/goals/<int:goal_id>/complete", methods=['POST'])
@login_required
def api_complete_goal(goal_id):
    success = models.complete_goal(goal_id, user_id=current_user.id)
    if success:
        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}."
        )
        socketio.emit('data_updated', {"message": "Goal completed"})
        return jsonify({"message": f"Goal {goal_id} completed."})
    return jsonify({"error": "Goal not found."}), 404

@app.route("/api/initiatives", methods=['GET'])
@login_required
def api_get_initiatives():
    initiatives = models.list_pending_initiatives(user_id=current_user.id)
    return jsonify({"initiatives": [{"id": i[0], "quarter": i[1], "description": i[2]} for i in initiatives]})

@app.route("/api/initiatives", methods=['POST'])
@login_required
def api_add_initiative():
    data = request.get_json() or {}
    quarter = data.get("quarter")
    description = data.get("description")
    if quarter and description:
        init_id = models.add_initiative(quarter, description, user_id=current_user.id)
        notify_all(
            subject="New Initiative Added",
            body=f"You added a new initiative for {quarter}: {description}",
            speakable_message=f"You added a new quarterly initiative for {quarter}: {description}"
        )
        socketio.emit('data_updated', {"message": "Initiative added"})
        return jsonify({"message": "Initiative added.", "id": init_id}), 201
    return jsonify({"error": "Quarter and description required."}), 400

@app.route("/api/initiatives/<int:initiative_id>/complete", methods=['POST'])
@login_required
def api_complete_initiative(initiative_id):
    success = models.complete_initiative(initiative_id, user_id=current_user.id)
    if success:
        notify_all(
            subject="Initiative Completed!",
            body=f"Great job completing quarterly initiative {initiative_id}.",
            speakable_message=f"Great job completing quarterly initiative {initiative_id}."
        )
        socketio.emit('data_updated', {"message": "Initiative completed"})
        return jsonify({"message": f"Initiative {initiative_id} completed."})
    return jsonify({"error": "Initiative not found."}), 404


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    if body and body.lower().strip() == 'list':
        goals = models.list_pending_goals()

        if not goals:
            resp.message("No pending daily goals. Great job!")
        else:
            msg = "Pending Goals:\n"
            for g in goals:
                msg += f"[{g[0]}] {g[1]}\n"
            resp.message(msg)
    else:
        # Determine the right reply for this message
        resp.message("Welcome to One-Minute Manager. Reply 'list' to see pending goals.")

    return str(resp)

@app.route("/voice", methods=['POST'])
def voice_reply():
    """Respond to incoming phone calls."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Hello. I am your One-Minute Manager. You are doing great today. Goodbye.")

    return str(resp)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
