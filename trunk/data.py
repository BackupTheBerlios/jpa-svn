# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Data storage for JPA application"""

__revision__ = '$Id$'

import os
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Storage(object):

    def __init__(self, filename=None):
        if filename is None:
            import const
            self.filename = os.path.join(const.USER_DIR, 'queue')
        else:
            self.filename = filename
        if os.path.isfile(self.filename):
            fp = open(self.filename, 'b')
            try:
                self.items = pickle.load(fp)
            finally:
                fp.close()
        else:
            self.items = []

    def save(self):
        fp = open(self.filename, 'wb')
        try:
            pickle.dump(self.items, fp, -1)
        finally:
            fp.close()
