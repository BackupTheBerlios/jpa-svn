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

import httplib, urlparse, proxytools
import binascii
try:
    import cElementTree as ElementTree
except ImportError:
    from elementtree import ElementTree

# import lib.version
import api

# namespaces
NS_ATOM = '{http://purl.org/atom/ns#}'
NS_BLOGGER = '{http://www.blogger.com/atom/ns#}'
NS_HTML = '{http://www.w3.org/1999/xhtml}'

class BloggerTransport(api.WeblogTransport):
    """Weblog transport that uses Blogger Atom API."""
    
    def __init__(self, userName, passwd, proxyConfig=None, uri=None):
        self.proxy = proxyConfig
        self.userName = userName
        self.passwd = passwd
        self.authCookie = binascii.b2a_base64('%s:%s' % (userName, passwd))
        self.authCookie = self.authCookie.strip() # strip final newline
        self.headers = {
            'Content-type': 'application/atom+xml',
            'Authorization': 'BASIC %s' % self.authCookie,
            #'UserAgent': '%s' % lib.version.AGENT,
            'UserAgent': 'JPA-1.0', # temporary for tests
            }
        if proxyConfig:
            # we do not support proxies with authentication at this time
            self.path = 'https://www.blogger.com/atom%s'
            self.host = '%s:%s' % (proxyConfig['host'], proxyConfig['port'])
        else:
            self.path = '/atom%s'
            self.host = 'www.blogger.com'
    
    @classmethod
    def getMetadata(self):
        """Return transport's metadata for use in service definitions."""
        meta = {}
        meta['name'] = 'Blogger (Atom)'
        meta['description'] = _('Blogger.com transport using new Atom API')
        meta['proto'] = 'HTTPS'
        meta['uri'] = 'https://www.blogger.com/atom'
        return meta

    def getBlogList(self):
        """This method returns dictionary of user's blog names (keys) and
        their identifiers (values), suitable for use in blog inquiries and
        operations."""
        if self.proxy:
            connection = proxytools.ProxyHTTPSConnection(self.proxy['host'],
                self.proxy['port'])
        else:
            connection = httplib.HTTPSConnection(self.host)
        path = self.path % ''
        try:
            connection.request('GET', path, headers=self.headers)
            response = connection.getresponse()
            if response.status  >= 500:
                raise api.ServiceUnavailabeError('Blogger server error')
            document = response.read()
        finally:
            connection.close()
        tree = ElementTree.fromstring(document)
        links = tree.findall(NS_ATOM + 'link')
        blogs = {}
        for link in links:
            href = link.get('href')
            (scheme, loc, path, query, frag) = urlparse.urlsplit(href)
            blogs[link.get('title')] = path.split('/')[-1]
        return blogs
