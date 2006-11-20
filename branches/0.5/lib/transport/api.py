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


### new classes for weblog (and other services) access ###
class WebIdentity:
    """User identity at web service hub."""

    def __init__(self, name, service, user_credentials):
        self.name = name
        self.service = service
        self.credentials = user_credentials

    def authorize(self):
        """Authorize user at service. All needed data should be already
        available in credentials dictionary."""
        raise NotImplementedError

    def get_services(self):
        """Get list of available web services."""
        raise NotImplementedError


class WebService:
    """Web service abstract prototype"""
    pass


class Weblog(WebService):
    """Remote access to weblog service"""

    def post_entry(self, entry):
        """Post new entry to weblog service."""
        raise NotImplementedError

    def post_modified(self, entry):
        """Post updated entry to weblog service"""
        raise NotImplementedError

    def get_latest_entries(self, num_entries=20):
        """Retrieve list of recently published entries"""
        raise NotImplementedError

    def get_entry(self, entry_id):
        """Retrieve single entry from weblog service"""
        raise NotImplementedError

    def delete_entry(self, entry_id):
        """Delete single entry from weblog service"""
        raise NotImplementedError


### old and slowly deprecating class ###
class WeblogTransport:
    """Nearly-abstract class, specifying base transport functionality."""

    def __init__(self, userName, passwd, proxyConfig=None, uri=None):
        self.proxy = proxyConfig
        self.userName = userName
        self.passwd = passwd
        self.uri = uri

    def getBlogList(self): raise NotImplementedError

    def postNew(self, blogId, entry, categories): raise NotImplementedError

    def postModified(self, blogId, entryId, entry, categories): raise NotImplementedError

    def getEntry(self, blogId, entryId): raise NotImplementedError

    def deleteEntry(self, blogId, entryId): raise NotImplementedError

    def getCategories(self, blogId): raise NotImplementedError

    def putMediaObject(self, blogId, mediaFileName): raise NotImplementedError

