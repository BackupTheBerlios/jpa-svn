# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Application data model and support routines"""

__revision__ = '$Id$'

import os
import datetime

from sqlalchemy import *

import const

class Data(object):

    def __init__(self):
        db_filename = os.path.abspath(os.path.join(const.USER_DIR, 'jpa.db'))
        self.metadata = BoundMetadata('sqlite://%s' % db_filename)
        self.metadata.engine.echo = False
        self.weblogs_table = Table('weblog', metadata,
            Column('weblog_id', Integer, primary_key=True),
            Column('name', Unicode(80)),
            Column('description', Unicode),
        )
        self.entries_table = Table('entry', metadata,
            Column('entry_id', Integer, primary_key=True),
            Column('created', DateTime, default=datetime.datetime.now()),
            Column('title', Unicode(100), nullable=False),
            Column('text', Unicode),
            Column('content_type', Unicode(20), default=u'markdown'),
            Column('labels', Unicode),
        )

    def init_tables():
        weblogs_table.create()
        entries_table.create()
