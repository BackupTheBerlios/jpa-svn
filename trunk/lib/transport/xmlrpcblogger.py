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

"""Old blogger.com API, using XML-RPC. Still used with many services (i.e. blox.pl)
and blogging systems, such as WordPress."""

__revision__ = '$Id$'

import xmlrpclib

import api, proxytools
import lib.renderer
from lib.appconst import DEBUG

APPKEY = 'nobody hears'

class BloggerTransport(api.WeblogTransport):
    
    def __init__(self, userName, passwd, proxyConfig=None, uri=None):
        self.proxy = proxyConfig
        self.userName = userName
        self.passwd = passwd
        self.uri = uri

    @classmethod
    def getMetadata(self):
        """Return transport's metadata for use in service definitions."""
        meta = {}
        meta['name'] = 'Blogger (XML-RPC)'
        meta['description'] = _('Old Blogger.com transport using XML-RPC API')
        meta['proto'] = 'HTTP'
        meta['uri'] = None
        return meta
    
    def _getServerProxy(self):
        kw = {}
        if self.proxy:
            kw['transport'] = proxytools.ProxyTransport(self.proxy['host'], self.proxy['port'])
        kw['encoding'] = 'utf-8'
        return xmlrpclib.ServerProxy(self.uri, **kw)

    def getBlogList(self):
        s = self._getServerProxy()
        ret = s.blogger.getUsersBlogs(APPKEY, self.userName, self.passwd)
        blogs = {}
        for blogData in ret:
            title = blogData['blogName']
            try:
                data = blogs[title]
            except KeyError:
                data = {}
            data['blogID'] = blogData['blogid']
            blogs[title] = data
        return blogs
    
    def postNew(self, blogId, entry):
        if DEBUG:
            print 'started sending'
        s = self._getServerProxy()
        body = []
        body.append(entry.title.encode('utf-8'))
        body.append(lib.renderer.renderBodyAsXML(entry.body.encode('utf-8'),
            entry.bodyType))
        body = '\n'.join(body)
        return s.blogger.newPost(APPKEY, blogId, self.userName, self.passwd,
            body, not entry.isDraft)
    
    def getEntry(self, entryId):
        s = self._getServerProxy()
        ret = s.blogger.getPost(APPKEY, entryId, self.userName, self.passwd)
