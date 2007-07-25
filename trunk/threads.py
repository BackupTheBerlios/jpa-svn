# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Program threads library"""

__revision__ = '$Id$'

import threading

import const
import transport
import signals

class EntriesRetrieverThread(threading.Thread):

    def __init__(self, blog, service):
        threading.Thread.__init__(self)
        self.blog = blog
        self.service = service

    def run(self):
        blog_id = self.blog['id']
