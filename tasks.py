from celery import Celery
from celery.schedules import crontab
from notifications import notify_all
import models
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery('tasks',
                    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
                    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'))

@celery_app.task
def trigger_morning_prompt():
    """Trigger a daily morning prompt if there are pending goals.
       Note: In a full multi-tenant system with different contact info per user,
       we would iterate through each user. For now, we assume user_id=1 for
       the primary notification receiver, or query it generically.
    """
    goals = models.list_pending_goals(user_id=1)
    if not goals:
        return

    goal_count = len(goals)
    notify_all(
        subject="Morning Goal Prompt",
        body=f"Good morning! You have {goal_count} pending One-Minute goals for today.",
        speakable_message=f"Good morning! You have {goal_count} pending goals today. Let's make it happen."
    )
    print(f"Triggered morning prompt for {goal_count} goals.")

@celery_app.task
def trigger_quarterly_reminder():
    """Trigger a weekly reminder about upcoming quarterly initiatives."""
    initiatives = models.list_pending_initiatives(user_id=1)
    if not initiatives:
        return

    init_count = len(initiatives)
    notify_all(
        subject="Quarterly Initiative Look-Ahead",
        body=f"Reminder: You have {init_count} pending quarterly initiatives. Are your systems in place?",
        speakable_message=f"Reminder: You have {init_count} pending quarterly initiatives. Plan ahead."
    )
    print(f"Triggered quarterly reminder for {init_count} initiatives.")

celery_app.conf.beat_schedule = {
    'morning-prompt-every-day': {
        'task': 'tasks.trigger_morning_prompt',
        'schedule': crontab(hour=8, minute=0),
    },
    'quarterly-reminder-every-monday': {
        'task': 'tasks.trigger_quarterly_reminder',
        'schedule': crontab(day_of_week='mon', hour=9, minute=0),
    },
}
celery_app.conf.timezone = 'UTC'
