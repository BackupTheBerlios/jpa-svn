# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Data storage for JPA application"""

__revision__ = '$Id$'

import os
import cPickle as pickle
from Queue import Queue, Empty


class Storage(object):

    def __init__(self, filename=None):
        self.items = Queue()
        if filename is None:
            import const
            self.filename = os.path.join(const.USER_DIR, 'queue')
        else:
            self.filename = filename
        if os.path.isfile(self.filename):
            fp = open(self.filename, 'rb')
            try:
                items = pickle.load(fp)
            finally:
                fp.close()
        else:
            items = []
        for item in items:
            self.items.put_nowait(item)

    def save(self):
        items = []
        while 1:
            try:
                items.append(self.items.get_nowait())
            except Empty:
                break
        fp = open(self.filename, 'wb')
        try:
            pickle.dump(items, fp, -1)
        finally:
            fp.close()

    def get_item(self):
        try:
            return self.items.get_nowait()
        except Empty:
            pass

    def add_item(self, item):
        self.items.put_nowait(item)
