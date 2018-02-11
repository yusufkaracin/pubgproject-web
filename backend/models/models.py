#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apistar import reverse_url

from django.core.cache import cache

from models.typesystems import Crate as CrateType

OPEN = 'Open'
SELL = 'Sell'


def open_or_sell(crate):
    data = {
        'cheap': {'count': None, 'items': [], 'percent': None},
        'expensive': {'count': None, 'items': [], 'percent': None},
        'count': None,
        'decision': None
    }
    items = crate['items']
    crate_price = crate['steam_price']

    for item in items:
        if item['steam_price'] < crate_price:
            data['cheap']['items'].append(item)
        else:
            data['expensive']['items'].append(item)

    cheap_items_len = len(data['cheap']['items'])
    expensive_items_len = len(data['expensive']['items'])
    total_len = cheap_items_len + expensive_items_len
    cheap_drop_chance = 100 / total_len * cheap_items_len
    expensive_drop_chance = 100 / total_len * expensive_items_len

    data['cheap']['count'] = cheap_items_len
    data['expensive']['count'] = expensive_items_len
    data['cheap']['percent'] = round(cheap_drop_chance, 2)
    data['expensive']['percent'] = round(expensive_drop_chance, 2)
    data['count'] = total_len

    decision = OPEN
    if cheap_items_len > expensive_items_len:
        decision = SELL
    data['decision'] = decision

    return data


class Crate(object):
    """
    Save crawled data in cache as below structure:
    {
        <_name>: {
            <pk>: <typesystems.Crate>,
            <pk>: <typesystems.Crate>,
            ...
        }
    }
    """
    _name = 'crates'

    @classmethod
    def get(cls, pk: int):
        obj = cache.get(cls._name, {})
        crate = obj.get(pk, {})
        return crate

    @classmethod
    def create(cls, pk: int, crate: CrateType):
        crate.update({
            'absolute_url': reverse_url('crate_detail', crate_id=pk),
            'items': open_or_sell(crate=crate)
        })

        crates = cache.get(cls._name, {})
        crates[pk] = crate
        cache.set(cls._name, crates)

        return crates[pk]

    @classmethod
    def all(cls):
        crates = cache.get(cls._name, {})
        res = []
        for pk, crate in crates.items():
            res.append(crate)
        return res
