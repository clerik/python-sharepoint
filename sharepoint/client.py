import functools

import requests
from lxml import etree
from requests import HTTPError
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

        if 200 >= response.status_code < 400:
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            xml = response.text.encode('utf-8')
            doc = etree.fromstring(xml, parser=parser)
            return doc.xpath('/soap:Envelope/soap:Body/*', namespaces=namespaces)[0]
        else:
            raise HTTPError(response.status_code)
