# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Application data model and support routines - SQLAlchemy based attempt."""

__revision__ = '$Id$'

import os
import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

import const


# these are our mapped objects
class Weblog(object):

    def __init__(self, name, blogger_id):
        self.name = name
        self.blogger_id = blogger_id

    def __repr__(self):
        return u'%s (%s)' % (self.name, self.blogger_id)


class Entry(object):

    def __repr__(self):
        return self.title


class Publication(object):

    def __init__(self, entry, weblog, assigned_url):
        self.entry = entry
        self.weblog = weblog
        self.assigned_url = assigned_url

    def __repr__(self):
        return u'%s - %s' % (self.publication_date.isoformat(), self.assigned_url)

# module initialization section
_db_filename = os.path.abspath(os.path.join(const.USER_DIR, 'jpa.db'))
_metadata = sa.BoundMetaData('sqlite:///%s' % _db_filename)
_debug = getattr(const, 'DEBUG', False)
_metadata.engine.echo = _debug
weblogs_table = sa.Table('weblog', _metadata,
    sa.Column('weblog_id', sa.Integer, primary_key=True),
    sa.Column('blogger_id', sa.Unicode, nullable=False, unique=True),
    sa.Column('name', sa.Unicode(80), index=True),
    sa.Column('description', sa.Unicode),
)
weblogs_table.create(checkfirst=True)
entries_table = sa.Table('entry', _metadata,
    sa.Column('entry_id', sa.Integer, primary_key=True),
    sa.Column('created', sa.DateTime, default=datetime.datetime.utcnow(),
        index=True),
    sa.Column('title', sa.Unicode(100), nullable=False),
    sa.Column('text', sa.Unicode),
    sa.Column('content_type', sa.Unicode(20), default=u'markdown'),
    sa.Column('labels', sa.Unicode),
    sa.Column('is_draft', sa.Boolean, default=False),
)
entries_table.create(checkfirst=True)
publications_table = sa.Table('publication', _metadata,
    sa.Column('publication_id', sa.Integer, primary_key=True),
    sa.Column('date', sa.DateTime, default=datetime.datetime.utcnow(),
        index=True),
    sa.Column('weblog_id', sa.Integer, sa.ForeignKey('weblog.weblog_id')),
    sa.Column('entry_id', sa.Integer, sa.ForeignKey('entry.entry_id')),
    sa.Column('assigned_url', sa.Unicode),
)
publications_table.create(checkfirst=True)

orm.clear_mappers()
orm.mapper(Weblog, weblogs_table, properties={
    'publications': orm.relation(Publication),
})
orm.mapper(Publication, publications_table, properties={
    'weblog': orm.relation(Weblog),
    'entry': orm.relation(Entry),
})
orm.mapper(Entry, entries_table, properties={
    'publications': orm.relation(Publication),
})
session = orm.create_session()
