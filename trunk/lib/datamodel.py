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

"""Application data model"""

__revision__ = '$Id$'

import datetime, os
import Queue

from sqlobject import *
from sqlobject.sqlbuilder import *

import appconst, transport

BODY_TYPES = ['plain', 'textile', 'markdown', 'HTML']
try:
    import docutils.core
    BODY_TYPES.insert(3, 'ReST')
except ImportError:
    # no docutils installed, sorry
    pass

def initModel():
    isSchemaEmpty = False
    if not os.access(appconst.PATHS['data'], os.F_OK):
        isSchemaEmpty = True
        root, tail = os.path.split(appconst.PATHS['data'])
        if not os.path.isdir(root):
            os.makedirs(root)
    connection = connectionForURI(appconst.DB_URI)
    sqlhub.processConnection = connection
    Entry.createTable(ifNotExists=True)
    Category.createTable(ifNotExists=True)
    Publication.createTable(ifNotExists=True)
    Identity.createTable(ifNotExists=True)
    Weblog.createTable(ifNotExists=True)
    if isSchemaEmpty:
        fillTables()

def fillTables():
    Category(name=_('Miscellaneous'),
        description=_('Miscellaneous category'))

def getEntriesList(year, month):
    return Entry.select(
        AND(Entry.q.year==year, Entry.q.month==month),
        orderBy='created'
    ).reversed()

class Entry(SQLObject):
    """
    Object that represents single entry.
    """
    created = DateTimeCol(default=datetime.datetime.utcnow)
    title = UnicodeCol()
    body = UnicodeCol()
    bodyType = EnumCol(enumValues=BODY_TYPES, default='plain')
    visibilityLevel = IntCol(default=0)
    month = IntCol(default=datetime.datetime.now().month)
    year = IntCol(default=datetime.datetime.now().year)
    categories = RelatedJoin('Category')
    isDraft = BoolCol(default='f')
    publications = MultipleJoin('Publication', orderBy='-published')
    # indexes
    createdIdx = DatabaseIndex(created)
    titleIdx = DatabaseIndex(title)
    
    def publish(self, weblog, events, updates):
        """Method to publish entry to specified weblog"""
        transportType = weblog.identity.transportType
        login = weblog.identity.login
        password = weblog.identity.password
        uri = weblog.identity.serviceURI
        if appconst.CFG.getOption('network', 'use_proxy', '0') == '1':
            host = appconst.CFG.getOption('network', 'proxy_host', '')
            port = int(appconst.CFG.getOption('network', 'proxy_port', '0'))
            proxy = {'host': host, 'port': port}
        else:
            proxy = None
        transportClass = transport.TRANSPORTS[transportType]
        transportObj = transportClass(login, password, proxy, uri)
        try:
            msg = _('Started sending entry "%s" to weblog %s') % \
                (self.title, weblog.name)
            events.put_nowait(('sending', msg))
            assignedId = transportObj.postNew(weblog.weblogID, self)
            msg = _('Entry "%s" published to weblog %s') % \
                (self.title, weblog.name)
            events.put_nowait(('sending', msg))
            pubDate = datetime.datetime.now()
            updates.put_nowait((self, weblog, pubDate, assignedId))
        except transport.ServiceError, e:
            msg = _('Error while sending entry "%s" to weblog %s: %s') %\
                (self.title, weblog.name, e)
            events.put.nowait(('sending', msg))
    
    def updatePublication(self, weblog, pubDate, assignedId):
        Publication(published=pubDate,
            entry=self,
            weblog=weblog,
            assignedId=assignedId
        )


class Category(SQLObject):
    """
    Object that represents entry category.
    """
    name = UnicodeCol(alternateID=True, notNone=True)
    description = UnicodeCol()
    entries = RelatedJoin('Entry')


class Publication(SQLObject):
    """
    Object that holds information on entry publication.
    """
    published = DateTimeCol(notNone=True)
    entry = ForeignKey('Entry')
    weblog = ForeignKey('Weblog')
    assignedId = UnicodeCol()
    # indexes
    pubIdx = DatabaseIndex(published)


class Identity(SQLObject):
    """
    Object that holds user identity (service account data)
    """
    name = UnicodeCol(alternateID=True)
    transportType = UnicodeCol()
    login = UnicodeCol()
    password = UnicodeCol()
    serviceProtocol = UnicodeCol(default='xmpp')
    serviceURI = UnicodeCol(dbName='service_uri')
    postURI = UnicodeCol(default=None, dbName='post_uri')
    editURI = UnicodeCol(default=None, dbName='edit_uri')
    deleteURI = UnicodeCol(default=None, dbName='delete_uri')
    getURI = UnicodeCol(default=None, dbName='get_uri')
    servicePort = IntCol(default=0)
    weblogs = MultipleJoin('Weblog')


class Weblog(SQLObject):
    """
    Object that contains weblog configuration data
    """
    name = UnicodeCol(alternateID=True)
    identity = ForeignKey('Identity')
    weblogID = UnicodeCol(default=None)
    isActive = BoolCol(default='t', notNone=True)
    # indexes
    activeIdx = DatabaseIndex(isActive)
