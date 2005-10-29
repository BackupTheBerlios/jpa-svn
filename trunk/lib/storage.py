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

"""Data storage."""

__revision__ = '$Id$'

import time
import os, os.path as op
import pickle # cann't use cPickle, we'll store unicode objects


def checkAvailableStorage():
    """Check what storage engines are available, return tuple of what is
    installed."""
    engines = []
    try:
        # try metakit
        import metakit
        engines.append('metakit')
    except ImportError:
        pass
    try:
        # try new pysqlite (pysqlite2)
        import pysqlite2
        engines.append('sqlite2')
    except ImportError:
        pass
    try:
        # try old pysqlite (pysqlite1)
        import sqlite
        engines.append('sqlite1')
    except ImportError:
        pass
    # the next two should be always available
    engines.append('bsddb')
    engines.append('shelve')
    return tuple(engines)
        


def getStorage(config):
    """Factory method to get instance of storage, based on configuration
    option."""
    if config.getOption('internal', 'storage', 'metakit') == 'metakit':
        import metakit
        return MetakitStorage()


class Storage:
    """Abstract base class for all storage implementations."""
    
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
        """Insert or delete entry.
        If Id is not specified, the entry will be inserted."""
        raise NotImplementedError
    
    def close(self):
        """Close storage engine. A good place to clean up."""
        raise NotImplementedError


class MetakitStorage(Storage):
    """Main storage of application data, based on metakit."""

    def __init__(self):
        fileName = op.join(os.environ['HOME'], '.jpa2', 'entries')
        if op.isfile(fileName):
            self.storage = metakit.storage(fileName, 1)
            self.entries = self.storage.view('entries')
        else:
            self.initStorage(fileName)

    def initStorage(self, fileName):
        dirName = op.dirname(fileName)
        if not op.isdir(dirName):
            os.makedirs(dirName)
        self.storage = metakit.storage(fileName, 1)
        self.entries = self.storage.getas('entries[eid:S,created:I,sent:S,'
            'edited:S,title:S,body:S,year:I,month:I]')
    
    def getEntriesList(self, entryYear, entryMonth):
        view = self.entries.select(year=entryYear, month=entryMonth)
        return view.project(metakit.property('S', 'eid'))
    
    def getEntries(self, entryYear, entryMonth):
        return self.entries.select(year=entryYear, month=entryMonth)

    def getEntry(self, entryId):
        entry = {}
        row = self.entries.find(eid=entryId)
        if row:
            entry['eid'] = row.eid
            entry['created'] = row.created
            entry['sent'] = pickle.loads(row.sent)
            entry['edited'] = pickle.loads(row.edited)
            entry['title'] = row.title
            entry['body'] = row.body
        return entry

    def setEntry(self, entry, entryId=None):
        if entryId:
            row = self.entries.find(eid=entryId)
            row.created = pickle.dumps(entry['created'], 2)
            row.sent = pickle.dumps(entry['sent'], 2)
            row.edited = pickle.dumps(entry['edited'], 2)
            row.title = entry['title']
            row.body = entry['body']
        else:
            entry['eid'] = time.strftime('%Y%m%d%H%M%S', entry['created'])
            entry.year = entry['created'][0]
            entry.month = entry['created'][1]
            self.entries.append(**entry)

    def close(self):
        self.storage.commit()
        self.storage = None