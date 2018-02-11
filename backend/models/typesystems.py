from apistar import typesystem
from apistar.exceptions import TypeSystemError


class DropRateTypeSystem(object):
    errors = {
        'invalid': 'Must be null or number.',
    }

    def __new__(cls, value: object):
        if (value is None) or (isinstance(value, float)):
            return value
        raise TypeSystemError(cls=cls, code='invalid')


class Item(typesystem.Object):
    properties = {
        'name': typesystem.String,
        'url': typesystem.String,
        'img': typesystem.String,
        'steam_url': typesystem.String,
        'steam_price': typesystem.Number,
        'drop_rate': DropRateTypeSystem,
        'created_at': typesystem.String
    }


class Crate(typesystem.Object):
    properties = {
        'id': typesystem.Integer,
        'url': typesystem.String,
        'name': typesystem.String,
        'img': typesystem.String,
        'steam_url': typesystem.String,
        'steam_price': typesystem.Number,
        'items': typesystem.array(items=Item),
        'need_key': typesystem.Boolean,
        'created_at': typesystem.String
    }


class SpiderData(typesystem.Array):
    items = Crate
    min_items = 1
    description = "The data passed by crawler"
