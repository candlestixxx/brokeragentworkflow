from celery import Celery
from celery.schedules import crontab
from notifications import notify_all
import models
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)


@celery_app.task
def trigger_morning_prompt():
    """Trigger a daily morning prompt for each user if they have pending goals."""
    users = models.list_users_for_notifications()
    for user_info in users:
        uid = user_info["id"]
        pending = models.list_pending_goals(user_id=uid)
        if not pending:
            continue

        goal_count = len(pending)
        notify_all(
            subject="Morning Goal Prompt",
            body=f"Good morning! You have {goal_count} pending One-Minute goals for today.",
            speakable_message=f"Good morning! You have {goal_count} pending goals today. Let's make it happen.",
        )
        print(
            f"Triggered morning prompt for {user_info['username']} ({goal_count} goals)."
        )


@celery_app.task
def trigger_quarterly_reminder():
    """Trigger a weekly reminder about upcoming quarterly initiatives for each user."""
    users = models.list_users_for_notifications()
    for user_info in users:
        uid = user_info["id"]
        pending = models.list_pending_initiatives(user_id=uid)
        if not pending:
            continue

        init_count = len(pending)
        notify_all(
            subject="Quarterly Initiative Look-Ahead",
            body=f"Reminder: You have {init_count} pending quarterly initiatives. Are your systems in place?",
            speakable_message=f"Reminder: You have {init_count} pending quarterly initiatives. Plan ahead.",
        )
        print(
            f"Triggered quarterly reminder for {user_info['username']} ({init_count} initiatives)."
        )


@celery_app.task
def trigger_weekly_goal_template():
    """Trigger a weekly prompt to remind agents to set their One-Minute Goals."""
    users = models.list_users_for_notifications()
    for user_info in users:
        notify_all(
            subject="Weekly One-Minute Goal Template",
            body="It's time to set your top 3 needle-moving goals for the week. Log into your dashboard to set your focus.",
            speakable_message="It's time to set your top 3 needle-moving goals for the week. Log into your dashboard to set your focus.",
        )
        print(f"Triggered weekly goal template for {user_info['username']}.")


@celery_app.task
def trigger_90_day_lookahead_alerts():
    """Trigger a 90-day look-ahead alert for major events (e.g., Oct 1 holiday prep)."""
    users = models.list_users_for_notifications()
    for user_info in users:
        notify_all(
            subject="Action Required: Order Holiday Client Gifts Today",
            body="As part of your 3-Month Look-Ahead, please finalize and order client holiday gifts today to prepare for Q4.",
            speakable_message="As part of your 3-Month Look-Ahead, please finalize and order client holiday gifts today to prepare for Q4.",
        )
        print(f"Triggered 90-day look-ahead alert for {user_info['username']}.")


celery_app.conf.beat_schedule = {
    "morning-prompt-every-day": {
        "task": "tasks.trigger_morning_prompt",
        "schedule": crontab(hour=8, minute=0),
    },
    "quarterly-reminder-every-monday": {
        "task": "tasks.trigger_quarterly_reminder",
        "schedule": crontab(day_of_week="mon", hour=9, minute=0),
    },
    "weekly-goal-template-every-monday": {
        "task": "tasks.trigger_weekly_goal_template",
        "schedule": crontab(day_of_week="mon", hour=9, minute=0),
    },
    "october-first-lookahead-alert": {
        "task": "tasks.trigger_90_day_lookahead_alerts",
        "schedule": crontab(month_of_year=10, day_of_month=1, hour=9, minute=0),
    },
}
celery_app.conf.timezone = "UTC"
