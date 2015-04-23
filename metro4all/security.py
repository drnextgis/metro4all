from pyramid.security import Allow
from pyramid.security import Everyone


class Root(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'group:admin', 'edit'),
    ]

    def __init__(self, request):
        self.request = request


USERS = {'admin': 'admin'}
GROUPS = {'admin': ['group:admin']}


def groupfinder(user_id, request):
    if user_id in USERS:
        return GROUPS.get(user_id, [])