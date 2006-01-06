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

from sqlobject import *
from sqlobject.sqlbuilder import *

import appconst

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
    created = DateTimeCol(default=datetime.datetime.now)
    title = UnicodeCol()
    body = UnicodeCol()
    bodyType = EnumCol(enumValues=BODY_TYPES, default='plain')
    visibilityLevel = IntCol(default=0)
    month = IntCol(default=datetime.datetime.now().month)
    year = IntCol(default=datetime.datetime.now().year)
    categories = RelatedJoin('Category')
    isDraft = BoolCol(default='f')
    # indexes
    createdIdx = DatabaseIndex(created)
    titleIdx = DatabaseIndex(title)


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
    serviceURI = UnicodeCol()
    servicePort = IntCol(default=0)


class Weblog(SQLObject):
    """
    Object that contains weblog configuration data
    """
    name = UnicodeCol(alternateID=True)
    identity = ForeignKey('Identity')
    weblogID = UnicodeCol()
    isActive = BoolCol(default='t', notNone=True)
    # indexes
    activeIdx = DatabaseIndex(isActive)
