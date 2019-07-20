from sharepoint.client import SharePointSoapClient
from sharepoint.lists.definitions import LIST_WEBSERVICE
from sharepoint.xml import namespaces, SP


class SharePointAttachments(object):
    def __init__(self, client: SharePointSoapClient, list_id, row_id):
        self.client = client
        self.list_id, self.row_id = list_id, row_id

    def __iter__(self):
        """
        Returns an iterator over attachments for a list item.

        Implements http://msdn.microsoft.com/en-us/library/websvclists.lists.getattachmentcollection.aspx
        """
        xml = SP.GetAttachmentCollection(SP.listName(self.list_id),
                                         SP.listItemID(str(self.row_id)))
        response = self.client.post_soap(
            LIST_WEBSERVICE, xml,
            soapaction='http://schemas.microsoft.com/sharepoint/soap/GetAttachmentCollection')
        for url in response.xpath('//sp:Attachment', namespaces=namespaces):
            yield SharePointAttachment(self, url.text)

    def delete(self, url):
        raise NotImplementedError

    def add(self, filename, content):
        raise NotImplementedError

    def open(self, url):
        return self.client.open(url)


class SharePointAttachment(object):
    def __init__(self, attachments, url):
        self.attachments, self.url = attachments, url

    def delete(self):
        self.attachments.delete(self.url)

    def open(self):
        return self.attachments.open(self.url)

    def __unicode__(self):
        return self.url

    def __repr__(self):
        return "<{0} '{1}'>".format(type(self).__name__, self.url)
