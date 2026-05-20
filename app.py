from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from notifications import notify_all
import models
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-default-key-for-flashes")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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

# Inject version globally into all templates
@app.context_processor
def inject_version():
    return dict(app_version=get_app_version())

def get_db_path():
    """Temporary backwards compatibility function. `models.get_db_url` handles the actual config."""
    return os.getenv("DATABASE_PATH", "goals.db")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = models.get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('dashboard'))
        flash("Invalid username or password.")
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if models.get_user_by_username(username):
            flash("Username already exists.")
        else:
            user_id = models.create_user(username, password)
            if user_id:
                flash("Registration successful. Please log in.")
                return redirect(url_for('login'))
            flash("Registration failed.")
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route("/")
@login_required
def dashboard():
    """Render the main web dashboard."""
    goals = models.list_pending_goals(user_id=current_user.id)
    initiatives = models.list_pending_initiatives(user_id=current_user.id)
    return render_template("dashboard.html", goals=goals, initiatives=initiatives)

@app.route("/goal/add", methods=['POST'])
@login_required
def add_goal_route():
    description = request.form.get("description")
    if description:
        models.add_goal(description, user_id=current_user.id)
        notify_all(
            subject="New Goal Added",
            body=f"You added a new goal: {description}",
            speakable_message=f"You added a new goal: {description}"
        )
        flash(f"Added goal: '{description}'")
    return redirect(url_for('dashboard'))

@app.route("/goal/complete/<int:goal_id>", methods=['POST'])
@login_required
def complete_goal_route(goal_id):
    success = models.complete_goal(goal_id, user_id=current_user.id)
    if success:
        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}."
        )
        flash(f"Goal {goal_id} marked as completed! Excellent work.")
    else:
        flash(f"No goal found with ID {goal_id}.")
    return redirect(url_for('dashboard'))

@app.route("/initiative/add", methods=['POST'])
@login_required
def add_initiative_route():
    quarter = request.form.get("quarter")
    description = request.form.get("description")
    if quarter and description:
        models.add_initiative(quarter, description, user_id=current_user.id)
        notify_all(
            subject="New Initiative Added",
            body=f"You added a new initiative for {quarter}: {description}",
            speakable_message=f"You added a new quarterly initiative for {quarter}: {description}"
        )
        flash(f"Added quarterly initiative for {quarter}: '{description}'")
    return redirect(url_for('dashboard'))

@app.route("/initiative/complete/<int:initiative_id>", methods=['POST'])
@login_required
def complete_initiative_route(initiative_id):
    success = models.complete_initiative(initiative_id, user_id=current_user.id)
    if success:
        notify_all(
            subject="Initiative Completed!",
            body=f"Great job completing quarterly initiative {initiative_id}.",
            speakable_message=f"Great job completing quarterly initiative {initiative_id}."
        )
        flash(f"Initiative {initiative_id} marked as completed!")
    else:
        flash(f"No initiative found with ID {initiative_id}.")
    return redirect(url_for('dashboard'))

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
    app.run(debug=True, port=5000)
