# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
import os

# Main cronjob function.
from main import send_commits_on_review, \
    create_schedule_by_settings

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler(timezone='Europe/Kiev')

if os.environ.get("LOCAL", 0) == 0:
    schedule = create_schedule_by_settings()
    scheduler.add_job(
        send_commits_on_review,
        'cron',
        day_of_week=schedule.day_of_week(),
        hour=schedule.hours(),
        minute=schedule.minutes()
    )
else:
    scheduler.add_job(
        send_commits_on_review,
        'interval',
        seconds=30
    )

scheduler.start()
