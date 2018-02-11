from apistar import Include, Route

from settings.config import DEBUG
from views.spider import callback
from views.crate import crate_list, crate_detail


routes = [
    Route('/', 'GET', crate_list),
    Route('/crate/{crate_id}', 'GET', crate_detail),
    Route('/spider', 'POST', callback),
]

if DEBUG:
    from apistar.handlers import docs_urls, static_urls

    routes += [
        Include('/docs', docs_urls),
        Include('/static', static_urls),
    ]
