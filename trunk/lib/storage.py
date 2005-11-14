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

"""Application data storage."""

__revision__ = '$Id$'

import os

# Check storage availability
engines = []
try:
    import pysqlite2
    from pysqlite2 import dbapi2 as sqlite
    engines.append('sqlite')
except ImportError:
    # not available, we'll try older one
    try:
        import sqlite
        engines.append('sqlite')
    except ImportError:
        # not available, we'll move on
        pass
import bsddb
engines.append('bsddb')
import shelve
engines.append('shelve')
# for the sake of code cleanliness
engines = tuple(engines)


def getStorage(config):
    """Factory method to get instance of storage, based on configuration
    option.
    The default option is the lowest common denominator, the standard Python's
    shelve module."""
    storageType = config.getOption('internal', 'storage', 'shelve')
    if storageType == 'sqlite':
        return SQLiteStorage()
    elif storageType == 'bsddb':
        return DBStorage()
    else:
        return ShelveStorage()


class Storage:
    """Abstract base class for all storage implementations. All other methods
    should be privatised to keep the interface clean."""
    
    def getEntriesList(self, entryYear, entryMonth):
        """Get list of Id's for entries in year and month."""
        raise NotImplementedError
    
    def getEntries(self, entryYear, entryMonth):
        """Get list of all entries in year and month."""
        raise NotImplementedError
    
    def getEntry(self, entryId):
        """Get single entry by its Id."""
        raise NotImplementedError
    
    def setEntry(self, entry, isNew):
        """Insert or update entry. If isNew, the entry will be inserted."""
        raise NotImplementedError
    
    def deleteEntry(self, entryId):
        """Permanently remove entry from storage."""
        raise NotImplementedError

    def close(self):
        """Close storage engine. A good place to clean up."""
        raise NotImplementedError


class SQLiteStorage(Storage):
    """Base for storages with SQLite (1 and 2) backends"""
    
    fileName = os.path.join(os.path.expanduser('~'), '.jpa2', 'entries')
    columnNames = ('eid', 'level', 'content_type', 'category', 'title', 'body', 
        'created', 'edited', 'sent', 'year', 'month')
    
    def __init__(self):
        self.engineLevel = sqlite.version_info[0]
        runInit = not os.access(self.fileName, os.F_OK)
        self.conn = sqlite.connect(self.fileName, client_encoding='utf-8')
        self.cur = self.conn.cursor()
        if runInit:
            self.initDB()
    
    def initDB(self):
        self.cur.execute('''create table entries (
                eid unicode not null primary key,
                level integer not null,
                content_type unicode not null,
                category unicode,
                title unicode not null,
                body unicode, 
                created integer not null, 
                edited unicode,
                sent unicode, 
                year integer not null,
                month integer not null)''')
        self.conn.commit()
    
    def getEntriesList(self, entryYear, entryMonth):
        if self.engineLevel == 1:
            qry = 'select eid from entries where year = %d and month = %d'
        else:
            qry = 'select eid from entries where year = ? and month = ?'
        self.cur.execute(qry, (entryYear, entryMonth))
        rows = []
        row = self.cur.fetchone()
        while row:
            rows.append(row[0])
        return rows

    def getEntry(self, entryId):
        if self.engineLevel == 1:
            qry = 'select * from entries where eid = %s'
        else:
            qry = 'select * from entries where eid = ?'
        self.cur.execute(qry, entryId)
        row = self.cur.fetchone()
        if row:
            return dict(zip(self.columnNames, row))

    def getEntries(self, entryYear, entryMonth):
        if self.engineLevel == 1:
            qry = 'select * from entries where year = %d and month = %d \
                order by 0 desc'
        else:
            qry = 'select * from entries where year = ? and month = ? \
                order by 0 desc'
        self.cur.execute(qry, (entryYear, entryMonth))
        rows = []
        row = self.cur.fetchone()
        while row:
            rows.append(dict(zip(self.columnNames, row)))
        return rows

    def setEntry(self, entry, isNew):
        if isNew:
            if self.engineLevel == 1:
                qry = 'insert into entries values \
                    (%s, %d, %s, %s, %s, %s, %d, %s, %s, %d, %d)'
            else:
                qry = 'insert into entries values \
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        else:
            if self.engineLevel == 1:
                pass
            else:
                pass


class DBStorage(Storage):
    """Common storage class for all BerkeleyDB storages."""
    pass


class ShelveStorage(Storage):
    """Main storage with shelve backend. Use as a last resort."""
    pass