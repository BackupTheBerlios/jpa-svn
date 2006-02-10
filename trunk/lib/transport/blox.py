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

"""Blox.pl specific transport.

This service is unique in that allows using blogger API along with MetaWeblog API
simultaneously and exchangeably."""

__revision__ = '$Id$'

import datetime
import xmlrpclib

import api, proxytools
from lib.renderer import renderBodyAsXML
from lib.version import AGENT
from lib.appconst import DEBUG

APPKEY = AGENT

class BloxTransport(api.XmlRpcTransport):
    
    @classmethod
    def getMetadata(self):
        """Return transport's metadata for use in service definitions."""
        meta = {}
        meta['name'] = 'Blox.pl'
        meta['description'] = _('Blox.pl specific transport')
        meta['proto'] = 'HTTP'
        meta['uri'] = None
        return meta

    def getBlogList(self):
        s = self.getServerProxy()
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
    
    def postNew(self, blogId, entry, categories):
        if DEBUG:
            print 'started sending'
        s = self.getServerProxy()
        body = {}
        body['flNotOnHomePage'] = False
        body['title'] = entry.title.encode('utf-8')
        body['description'] = renderBodyAsXML(entry.body.encode('utf-8'),
            entry.bodyType)
        body['categories'] = []
        for category in categories:
            body['categories'].append(category.name.encode('utf-8'))
        # publication date turned off as temporary workaround for
        # blox.pl code bug
        #body['pubDate'] = datetime.datetime.now().isoformat()
        body['guid'] = 'allo allo'
        body['author'] = self.userName.encode('utf-8')
        if DEBUG:
            print body
        try:
            assignedId = s.metaWeblog.newPost(blogId, self.userName, self.passwd,
                body, not entry.isDraft)
            return assignedId
        except xmlrpclib.Fault, e:
            raise api.ServiceError(e.faultString)
    
    def postModified(self, blogId, entryId, entry, categories):
        if DEBUG:
            print 'started sending modified entry'
        s = self.getServerProxy()
        body = {}
        body['flNotOnHomePage'] = False
        body['title'] = entry.title.encode('utf-8')
        body['description'] = renderBodyAsXML(entry.body.encode('utf-8'),
            entry.bodyType)
        body['categories'] = []
        for category in categories:
            body['categories'].append(category.name.encode('utf-8'))
        # publication date turned off as temporary workaround for
        # blox.pl code bug
        #body['pubDate'] = datetime.datetime.now().isoformat()
        body['guid'] = 'allo allo'
        body['author'] = self.userName.encode('utf-8')
        try:
            s.metaWeblog.editPost(entryId, self.userName, self.passwd,
                body, not entry.isDraft)
        except xmlrpclib.Fault, e:
            raise api.ServiceError(e.faultString)
