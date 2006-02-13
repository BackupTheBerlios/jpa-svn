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

"""Weblog operation thread"""

__revision__ = '$Id$'

import threading

class BlogOperatorThread(threading.Thread):
    """Generic class for weblog operations."""
    
    def __init__(self, weblog, entry=None, categories=[], parent=None):
        self.weblog = weblog
        self.entry = entry
        self.categories = categories
        self.parent = parent
        threading.Thread.__init__(self)


class BlogSenderThread(BlogOperatorThread):
    """Sender thread"""
    
    def __init__(self, weblog, entry, categories, parent):
        BlogOperatorThread.__init__(self, weblog, entry, categories, parent)
    
    def run(self):
        self.entry.publish(self.weblog, self.categories, self.parent)


class EntryUpdaterThread(BlogOperatorThread):
    """Thread sending updated entry"""
    
    def __init__(self, weblog, entryId, entry, categories, parent):
        self.entryId = entryId
        BlogOperatorThread.__init__(self, weblog, entry, categories, parent)
    
    def run(self):
        self.entry.postUpdated(self.weblog, self.entryId, self.categories, self.parent)


class CategorySynchronizerThread(BlogOperatorThread):
    """Thread that downloads category descriptions from weblog service"""
    
    def __init__(self, weblog, identity, parent):
        BlogOperatorThread.__init__(self, weblog, parent=parent)
        self.identity = identity
    
    def run(self):
        self.weblog.getCategories(self.identity, self.parent)
