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

# $Id$

"""Data storage."""

import os, os.path as op
import metakit

__revision__ = '$Revision$'

class Storage:
    """Main storage of application data."""

    def __init__(self):
        fileName = op.expanduser('~/.jpa2/entries')
        if not op.isfile(fileName):
            self.initStorage(fileName)
        self.storage = metakit.storage(fileName, 1)
        self.entries = self.storage.getas('entries[eid:S,created:S,sent:S,'
            'title:S,body:S,year:I,month:I]')

    def initStorage(self, fileName):
        dirName = op.dirname(fileName)
        if not op.isdir(dirName):
            os.makedirs(dirName)
    
    def getEntriesList(self, year, month):
        view = self.entries.select({'year': year}, {'month': month})
        entries = view.project(metakit.property('S', 'eid'))
        ret = []
        for e in entries:
            ret.append(e.eid)
        return ret
    
    def getEntries(self, year, month):
        pass

    def close(self):
        self.storage.commit()
        self.storage = None