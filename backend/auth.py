from apistar import http
from apistar.authentication import Authenticated
from apistar.interfaces import Auth

from settings.config import SECRET_KEY


class BasicAuthentication(object):
    def authenticate(self, authorization: http.Header):
        if authorization is None:
            return None

        scheme, token = authorization.split()

        if scheme.lower() != 'bearer':
            return None

        if token != SECRET_KEY:
            return None

        return Authenticated('spider')


class IsAuthenticated(object):
    def has_permission(self, auth: Auth):
        return auth.is_authenticated()
