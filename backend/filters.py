#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from django.utils.timesince import timesince
from jinja2 import filters

__all__ = ['since', 'current_year']


def since(value) -> str:
    """
    :param value: str
    :return:
    """
    res = ''
    if not value:
        return res

    d = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return timesince(d)


def current_year(value=None):
    return datetime.now().year


filters.FILTERS['since'] = since
filters.FILTERS['current_year'] = current_year
