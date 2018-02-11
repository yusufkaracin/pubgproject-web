#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapyd_api import ScrapydAPI

from tasks.celery import celery_app
from settings.config import env


@celery_app.task
def run_spider():
    scrapyd = ScrapydAPI(env('SCRAPYD', default='http://0.0.0.0:6800'))
    scrapyd.schedule('default', spider='pubgshowcase')
