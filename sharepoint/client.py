import functools

import requests
from lxml import etree
from six.moves.urllib.parse import urljoin

from .xml import soap_body, namespaces


class SharePointSoapClient(object):
    """
    Abstraction for fetch SOAP resources.
    """

    def __init__(self, base_url, timeout=None, auth=None):
        if not base_url.endswith('/'):
            base_url += '/'

        self.base_url = base_url
        self.relative = functools.partial(urljoin, base_url)
        self.timeout = timeout
        self.auth = auth

    def open(self, url):
        url = self.relative(url)
        response = requests.request('GET', url, headers={'Translate': 'f'}, auth=self.auth)
        return response.text

    def post_soap(self, url, xml, soapaction=None):
        url = self.relative(url)
        headers = {'Content-type': 'text/xml; charset=utf-8'}
        if soapaction:
            headers['Soapaction'] = soapaction
        response = requests.request('POST', url,
                                    data=etree.tostring(soap_body(xml)),
                                    headers=headers,
                                    timeout=self.timeout,
                                    auth=self.auth)
        return etree.parse(response).xpath('/soap:Envelope/soap:Body/*', namespaces=namespaces)[0]
