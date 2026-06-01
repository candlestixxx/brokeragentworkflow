import re

# update app.py
with open("app.py", "r") as f:
    app_content = f.read()

app_content = app_content.replace(
    "from blueprints.webhooks import webhooks_bp",
    "from blueprints.webhooks import webhooks_bp\nfrom blueprints.analytics import analytics_bp"
)
app_content = app_content.replace(
    "app.register_blueprint(webhooks_bp)",
    "app.register_blueprint(webhooks_bp)\napp.register_blueprint(analytics_bp)"
)

with open("app.py", "w") as f:
    f.write(app_content)

# update models.py
with open("models.py", "r") as f:
    models_content = f.read()

# analytics function
analytics_code = """
# --- Analytics ---
def get_user_analytics(user_id=1, db_path=None):
    session = _get_session(db_path)

    total_goals = session.query(Goal).filter_by(user_id=user_id).count()
    completed_goals = session.query(Goal).filter_by(user_id=user_id, status="completed").count()
    pending_goals = session.query(Goal).filter_by(user_id=user_id, status="pending").count()

    completion_percentage = 0
    if total_goals > 0:
        completion_percentage = round((completed_goals / total_goals) * 100)

    # Calculate streak (simplified: consecutive days with at least one completed goal)
    completed_dates = session.query(func.date(Goal.created_at)).filter_by(user_id=user_id, status="completed").group_by(func.date(Goal.created_at)).order_by(func.date(Goal.created_at).desc()).all()

    streak = 0
    import datetime
    current_date = datetime.date.today()

    for date_tuple in completed_dates:
        # Check SQLite or Postgres format gracefully
        try:
            d_obj = datetime.datetime.strptime(str(date_tuple[0]), "%Y-%m-%d").date()
        except ValueError:
            break

        if d_obj == current_date:
            streak += 1
            current_date -= datetime.timedelta(days=1)
        elif d_obj == current_date - datetime.timedelta(days=1):
            streak += 1
            current_date -= datetime.timedelta(days=2) # Account for yesterday
        else:
            break

    session.close()

    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "pending_goals": pending_goals,
        "completion_percentage": completion_percentage,
        "streak": streak
    }
"""
if "# --- Analytics ---" not in models_content:
    models_content += analytics_code

with open("models.py", "w") as f:
    f.write(models_content)

# update frontend/src/components/NavBar.vue
with open("frontend/src/components/NavBar.vue", "r") as f:
    nav_content = f.read()

nav_content = nav_content.replace(
    '<router-link to="/settings"',
    '<router-link to="/" class="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300 transition duration-150 font-medium" active-class="text-blue-600 dark:text-blue-400">Dashboard</router-link>\n            <router-link to="/analytics" class="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300 transition duration-150 font-medium" active-class="text-blue-600 dark:text-blue-400">Analytics</router-link>\n            <router-link to="/settings"'
)

with open("frontend/src/components/NavBar.vue", "w") as f:
    f.write(nav_content)
