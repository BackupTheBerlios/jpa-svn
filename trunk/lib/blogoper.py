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
    
    def __init__(self, eventQueue, weblog, entry=None, categories=[], updates=None):
        self.queue = eventQueue
        self.updates = updates
        self.weblog = weblog
        self.entry = entry
        self.categories = categories
        threading.Thread.__init__(self)


class BlogSenderThread(BlogOperatorThread):
    """Sender thread"""
    
    def __init__(self, eventQueue, weblog, entry, categories, updates):
        BlogOperatorThread.__init__(self, eventQueue, weblog, entry, categories, updates)
    
    def run(self):
        self.entry.publish(self.weblog, self.categories, self.queue, self.updates)


class EntryUpdaterThread(BlogOperatorThread):
    """Thread sending updated entry"""
    
    def __init__(self, eventQueue, weblog, entryId, entry, categories, updates):
        self.entryId = entryId
        BlogOperatorThread.__init__(self, eventQueue, weblog, entry, categories, updates)
    
    def run(self):
        self.entry.postUpdate(self.weblog, self.entryId, self.categories, self.queue, self.updates)
