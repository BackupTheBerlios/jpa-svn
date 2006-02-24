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

"""Definition of generic weblog transport interface."""

__revision__ = '$Id$'

import xmlrpclib

import proxytools

# service errors
class ServiceError(Exception):
    """Base class for all service errors"""
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message


class ResourceNotFoundError(ServiceError): pass
class ServiceAuthorizationError(ServiceError): pass
class ServiceInternalError(ServiceError): pass
class ServiceUnavailableError(ServiceError): pass

class WeblogTransport:
    """Nearly-abstract class, specifying base transport functionality"""
    
    def __init__(self, userName, passwd, proxyConfig=None, uri=None):
        self.proxy = proxyConfig
        self.userName = userName
        self.passwd = passwd
        self.uri = uri

    def getBlogList(self): raise NotImplementedError

    def postNew(self, blogId, entry, categories): raise NotImplementedError

    def postModified(self, blogId, entryId, entry, categories): raise NotImplementedError

    def getEntry(self, entryId): raise NotImplementedError

    def deleteEntry(self, blogId, entryId): raise NotImplementedError
    
    def getCategories(self, blogId): raise NotImplementedError
    
    def putMediaObject(self, blogId, mediaFileName): raise NotImplementedError


class XmlRpcTransport(WeblogTransport):

    def getServerProxy(self):    
        kw = {}
        if self.proxy:
            kw['transport'] = proxytools.ProxyTransport(self.proxy['host'], self.proxy['port'])
        kw['encoding'] = 'utf-8'
        return xmlrpclib.ServerProxy(self.uri, **kw)

