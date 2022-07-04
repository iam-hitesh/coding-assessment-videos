from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Every week on Monday at 3AM
    "fetch_youtube_videos": {
        "task": "fetch_youtube_videos",
        "schedule": crontab()
    }
}