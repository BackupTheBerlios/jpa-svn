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
import metakit

class Storage:
    """Main storage of application data."""

    def __init__(self):
        fileName = op.join(op.expanduser('~'), '.jpa2', 'entries')
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
            row.created = pickle.dumps(entry['created'], 
                pickle.HIGHEST_PROTOCOL)
            row.sent = pickle.dumps(entry['sent'], pickle.HIGHEST_PROTOCOL)
            row.edited = pickle.dumps(entry['edited'], pickle.HIGHEST_PROTOCOL)
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