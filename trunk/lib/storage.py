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

import time
import os, os.path as op


def checkAvailableStorage():
    """Check what storage engines are available, return tuple of what is
    installed.
    As this function tries to import any of interesting modules, it should't be
    run too often."""
    engines = []
    for storage in ('pysqlite2', 'sqlite', 'bsddb', 'shelve'):
        try:
            __import__(storage)
            engines.append(storage)
        except ImportError:
            pass
    return tuple(engines)


def getStorage(config):
    """Factory method to get instance of storage, based on configuration
    option.
    The default option is the lowest common denominator, the standard Python's
    shelve module."""
    storageType = config.getOption('internal', 'storage', 'shelve')
    if storageType == 'sqlite':
        return SQLite1Storage()
    elif storageType == 'pysqlite2':
        return SQLite2Storage()
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
    
    def setEntry(self, entry, entryId=None):
        """Insert or delete entry. If Id is not specified, the entry will be
        inserted."""
        raise NotImplementedError

    def close(self):
        """Close storage engine. A good place to clean up."""
        raise NotImplementedError


class SQLiteStorage(Storage):
    """Base for storages with SQLite (1 and 2) backends"""
    
    fileName = op.join(op.expanduser('~'), '.jpa2', 'entries')
    
    def getEntriesList(self, entryYear, entryMonth):
        self.cur.execute('select eid from entries where year = %d and month = %d')
        rows = self.cur.fetchall()
        return [row[0] for row in rows]


class SQLite1Storage(SQLiteStorage):
    """Main storage with SQLite1 backend"""
    pass


class SQLite2Storage(SQLiteStorage):
    """Main storage with SQLite2 backend"""
    pass


class DBStorage(Storage):
    """Common storage class for all BerkeleyDB storages."""
    pass


class ShelveStorage(Storage):
    """Main storage with shelve backend. Use as a last resort."""
    pass