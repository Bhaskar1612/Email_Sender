from celery import Celery
from celery.schedules import crontab
from backend.tasks import send_pending_emails # Import your task

# Create a Celery instance (this is the Celery application)
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# Celery configuration
celery_app.conf.update(
    result_backend='redis://localhost:6379/0',
    timezone='UTC',  # You can adjust the timezone as per your needs
    beat_schedule={
        # Define periodic tasks here
        'send-pending-emails-every-minute': {
            'task': 'backend.tasks.send_pending_emails',  # Name of the task
            'schedule': crontab(minute='*/1'),  # Run every minute (change as needed)
        },
    },
)




