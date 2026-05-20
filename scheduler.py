from apscheduler.schedulers.background import BackgroundScheduler
from notifications import notify_all
import models
import time
import os
from dotenv import load_dotenv

load_dotenv()

def trigger_morning_prompt():
    """Trigger a daily morning prompt if there are pending goals."""
    goals = models.list_pending_goals()
    if not goals:
        return

    goal_count = len(goals)
    notify_all(
        subject="Morning Goal Prompt",
        body=f"Good morning! You have {goal_count} pending One-Minute goals for today.",
        speakable_message=f"Good morning! You have {goal_count} pending goals today. Let's make it happen."
    )
    print(f"Triggered morning prompt for {goal_count} goals.")

def trigger_quarterly_reminder():
    """Trigger a weekly reminder about upcoming quarterly initiatives."""
    initiatives = models.list_pending_initiatives()
    if not initiatives:
        return

    init_count = len(initiatives)
    notify_all(
        subject="Quarterly Initiative Look-Ahead",
        body=f"Reminder: You have {init_count} pending quarterly initiatives. Are your systems in place?",
        speakable_message=f"Reminder: You have {init_count} pending quarterly initiatives. Plan ahead."
    )
    print(f"Triggered quarterly reminder for {init_count} initiatives.")

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Run the morning prompt every day at 8:00 AM
    scheduler.add_job(trigger_morning_prompt, 'cron', hour=8, minute=0)

    # Run the quarterly reminder every Monday at 9:00 AM
    scheduler.add_job(trigger_quarterly_reminder, 'cron', day_of_week='mon', hour=9, minute=0)

    scheduler.start()
    print("Scheduler started. Waiting for jobs...")

    try:
        # Keep the main thread alive to allow background jobs to execute
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()
