from .client import SharePointSoapClient
from .lists import SharePointLists
from .users import SharePointUsers
from .xml import namespaces, OUT


class SharePointSite(object):
    def __init__(self, client: SharePointSoapClient):
        self._lists = None
        self._users = None
        self.client = client

    @property
    def lists(self):
        if not hasattr(self, '_lists') or self._lists is None:
            self._lists = SharePointLists(self.client)
        return self._lists

    @property
    def users(self):
        if not hasattr(self, '_users') or self._users is None:
            self._users = SharePointUsers(self.client)
        return self._users

    def as_xml(self, include_lists=False, include_users=False, **kwargs):
        xml = OUT.site(url=self.client.base_url)
        if include_lists or kwargs.get('list_names'):
            xml.append(self.lists.as_xml(**kwargs))
        if include_users:
            if 'user_ids' not in kwargs:
                kwargs['user_ids'] = set(xml.xpath('.//sharepoint:user/@id', namespaces=namespaces))
            xml.append(self.users.as_xml(**kwargs))
        return xml
