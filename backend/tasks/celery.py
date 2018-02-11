#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from celery import Celery
from celery.schedules import crontab

from settings.config import env


celery_app = Celery(
    'proj',
    broker=env("CELERY:BROKER", default="redis://localhost:6379/0"),
    backend=env("CELERY:BACKEND", default="redis://localhost"),
    include=['tasks.tasks']
)


celery_app.conf.beat_schedule = {
    'run_spider': {
        'task': 'tasks.tasks.run_spider',
        'schedule': crontab(minute='*/30')
    },
}

if __name__ == '__main__':
    celery_app.start()
