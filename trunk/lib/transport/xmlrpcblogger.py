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
            blogs[blogData['blogName']] = blogData['blogid']
        return blogs
    
    def getEntry(self, entryId):
        s = self._getServerProxy()
        ret = s.blogger.getPost(APPKEY, entryId, self.userName, self.passwd)
