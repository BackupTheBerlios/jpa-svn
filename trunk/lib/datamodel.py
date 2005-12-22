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

import appconst

def initModel():
    if not os.access(appconst.PATHS['data'], os.F_OK):
        root, tail = os.path.split(appconst.PATHS['data'])
        if not os.path.isdir(root):
            os.makedirs(root)
    connection = connectionForURI(appconst.DB_URI)
    sqlhub.processConnection = connection
    Entry.createTable(ifNotExists=True)
    Category.createTable(ifNotExists=True)
    Publication.createTable(ifNotExists=True)
    Weblog.createTable(ifNotExists=True)


class Entry(SQLObject):
    """
    Object that represents single entry.
    """
    created = DateTimeCol(default=datetime.datetime.now)
    title = UnicodeCol()
    body = UnicodeCol()
    bodyType = EnumCol(enumValues=('plain', 'textile', 'ReST', 'HTML'), 
        default='plain', notNone=True)
    visibilityLevel = IntCol(default=0, notNone=True)
    month = IntCol(default=datetime.datetime.now().month)
    year = IntCol(default=datetime.datetime.now().year)
    categories = RelatedJoin('Category')
    # indexes
    createdIdx = DatabaseIndex(created)
    titleIdx = DatabaseIndex(title)
    
    def publish(self, transports):
        """
        Send an entry to weblog.
        """
        for transport in transports:
            transport.send(self)


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


class Weblog(SQLObject):
    """
    Object that contains weblog configuration data
    """
    name = UnicodeCol(alternateID=True)
    transportType = UnicodeCol()
    userName = UnicodeCol()
    password = UnicodeCol()
    isActive = BoolCol(default='t', notNone=True)
    # indexes
    activeIdx = DatabaseIndex(isActive)