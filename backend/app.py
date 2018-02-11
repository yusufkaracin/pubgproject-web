#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apistar.frameworks.wsgi import WSGIApp as App

from settings.routes import routes
from settings.config import settings


app = App(
    routes=routes,
    settings=settings,
)

if __name__ == '__main__':
    app.main()
