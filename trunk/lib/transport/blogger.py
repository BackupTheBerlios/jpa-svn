# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003 - 2005 Jarek Zgoda <jzgoda@o2.pl>
#
# JPA is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with 
# JPA; if not, write to the Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Blogger.com specific transport, using Blogger Atom API and REST.

The API of Blogger is different that many other weblogging systems, as it uses
REST approach. Very nice, indeed!"""

__revision__ = '$Id$'

import time
import httplib, urlparse
import binascii
try:
    import cElementTree as ElementTree
except ImportError:
    from elementtree import ElementTree

import lib.renderer, lib.version
from lib.appconst import DEBUG
import api, proxytools

# namespaces
NS_ATOM = '{http://purl.org/atom/ns#}'
NS_ATOM_URI = 'http://purl.org/atom/ns#'
NS_BLOGGER = '{http://www.blogger.com/atom/ns#}'
NS_BLOGGER_URI = 'http://www.blogger.com/atom/ns#'
NS_HTML = '{http://www.w3.org/1999/xhtml}'
NS_HTML_URI = 'http://www.w3.org/1999/xhtml'
NS_DRAFT = '{http://purl.org/atom-blog/ns#}'
NS_DRAFT_URI = 'http://purl.org/atom-blog/ns#'

POST = """<?xml version="1.0" encoding="UTF-8" ?>
<entry xmlns="http://purl.org/atom/ns#">
<generator url="%(generatorUrl)s">%(generatorName)s</generator>
<title mode="escaped" type="text/html">%(title)s</title>
<issued>%(issued)s</issued>
<content type="application/xhtml+xml">
<div xmlns="http://www.w3.org/1999/xhtml">%(body)s</div>
</content>
<draft xmlns="http://purl.org/atom-blog/ns#">%(isDraft)s</draft>
</entry>"""

def buildBloggerPost(entry):
    generatorUrl = lib.version.PROG_URL
    generatorName = lib.version.AGENT
    title = entry.title.encode('utf-8')
    issued = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    body = lib.renderer.renderBodyAsXML(entry.body.encode('utf-8'),
        entry.bodyType)
    if entry.isDraft:
        isDraft = 'true'
    else:
        isDraft = 'false'
    data = locals()
    return (POST % data, data)


class BloggerTransport(api.WeblogTransport):
    """Weblog transport that uses Blogger Atom API."""
    
    def __init__(self, userName, passwd, proxyConfig=None, uri=None):
        api.WeblogTransport.__init__(self, userName, passwd, proxyConfig, uri)
        self.authCookie = binascii.b2a_base64('%s:%s' % (userName, passwd))
        self.authCookie = self.authCookie.strip() # strip final newline
        self.headers = {
            'Content-type': 'application/atom+xml',
            'Authorization': 'BASIC %s' % self.authCookie,
            'UserAgent': '%s' % lib.version.AGENT,
            }
        if proxyConfig:
            # we do not support proxies with authentication at this time
            self.path = 'https://www.blogger.com/atom%s'
            self.host = '%s:%s' % (proxyConfig['host'], proxyConfig['port'])
        else:
            self.path = '/atom%s'
            self.host = 'www.blogger.com'
    
    @classmethod
    def getMetadata(cls):
        """Return transport's metadata for use in service definitions."""
        meta = {}
        meta['name'] = 'Blogger (Atom)'
        meta['description'] = _('Blogger.com transport using new Atom API')
        meta['proto'] = 'HTTPS'
        meta['uri'] = 'https://www.blogger.com/atom'
        return meta

    @classmethod
    def supports(cls):
        """Return what transport supports from basic CRUD operations"""
        return 'CRUD'

    def getBlogList(self):
        """This method returns dictionary of user's blog names (keys) and
        their identifiers (values), suitable for use in blog inquiries and
        operations."""
        if self.proxy:
            connection = proxytools.ProxyHTTPSConnection(self.proxy['host'],
                self.proxy['port'])
        else:
            connection = httplib.HTTPSConnection(self.host)
        if DEBUG:
            connection.set_debuglevel(9)
        path = self.path % ''
        try:
            connection.request('GET', path, headers=self.headers)
            response = connection.getresponse()
            document = self._handleResponse(response)
        finally:
            connection.close()
        tree = ElementTree.fromstring(document)
        links = tree.findall(NS_ATOM + 'link')
        blogs = {}
        for link in links:
            href = link.get('href')
            (scheme, loc, path, query, frag) = urlparse.urlsplit(href)
            title = link.get('title')
            try:
                data = blogs[title]
            except KeyError:
                data = {}
            data['blogID'] = path.split('/')[-1]
            blogs[title] = data
        return blogs
    
    def postNew(self, blogId, entry, categories):
        post, data = buildBloggerPost(entry)
        if self.proxy:
            connection = proxytools.ProxyHTTPSConnection(self.proxy['host'],
                self.proxy['port'])
        else:
            connection = httplib.HTTPSConnection(self.host)
        if DEBUG:
            connection.set_debuglevel(9)
        blogPath = '/%s' % blogId
        path = self.path % blogPath
        try:
            connection.request('POST', path, body=post, headers=self.headers)
            response = connection.getresponse()
            content = self._handleResponse(response)
            if DEBUG:
                print content
            tree = ElementTree.fromstring(content)
            links = tree.findall(NS_ATOM + 'link')
            for link in links:
                if link.get('rel') == u'service.edit':
                    return link.get('href').split('/')[-1]
        finally:
            connection.close()
    
    def postModified(self, blogId, entryId, entry, categories):
        post, data = buildBloggerPost(entry)
        if self.proxy:
            connection = proxytools.ProxyHTTPSConnection(self.proxy['host'],
                self.proxy['port'])
        else:
            connection = httplib.HTTPSConnection(self.host)
        if DEBUG:
            connection.set_debuglevel(9)
        entryPath = '/%s/%s' % (blogId, entryId)
        path = self.path % entryPath
        try:
            connection.request('PUT', path, body=post, headers=self.headers)
            response = connection.getresponse()
            content = self._handleResponse(response)
            if DEBUG:
                print content
        finally:
            connection.close()
    
    def deleteEntry(self, blogId, entryId):
        if self.proxy:
            connection = proxytools.ProxyHTTPSConnection(self.proxy['host'],
                self.proxy['port'])
        else:
            connection = httplib.HTTPSConnection(self.host)
        if DEBUG:
            connection.set_debuglevel(9)
        entryPath = '/%s/%s' % (blogId, entryId)
        path = self.path % entryPath
        try:
            connection.request('DELETE', path, headers=self.headers)
            response = connection.getresponse()
            content = self._handleResponse(response)
            if DEBUG:
                print content
        finally:
            connection.close()

    def _handleResponse(self, response):
        if DEBUG:
            print 'received response: ', response.status, response.reason
        content = response.read()
        if response.status in range(200, 300):
            # success
            return content
        else:
            if response.status == 401:
                # authorization failure
                raise api.ServiceAuthorizationError(response.reason)
            elif response.status == 404:
                # resource does not exists
                raise api.ResourceNotFoundError(response.reason)
            elif response.status == 500:
                # internal server error
                lines = []
                lines.append(_('Returned HTTP reason: %s') % response.reason)
                lines.append(_('Received content:'))
                lines.append(content)
                raise api.ServiceInternalError('\n'.join(lines))
            elif response.status == 503:
                # service unavailable
                raise api.ServiceUnavailableError(response.reason)
            else:
                raise api.ServiceError(response.reason)
    

