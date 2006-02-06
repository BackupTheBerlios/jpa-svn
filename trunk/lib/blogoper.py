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
    
    def __init__(self, eventQueue, operation, weblog, entry=None):
        self.queue = eventQueue
        self.operation = operation
        self.weblog = weblog
        self.entry = entry
        threading.Thread.__init__(self)

    def run(self):
        if self.operation == 'new':
            self.entry.publish(self.weblog, self.queue)
        elif self.operation == 'edit':
            pass
        elif self.operation == 'delete':
            pass
        elif self.operation == 'get':
            pass
