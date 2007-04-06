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


class Weblog(object):

    def __repr__(self):
        return u'%s (%s)' % (self.name, self.blogger_id)


class Entry(object):

    def __repr__(self):
        return self.title


class Publication(object):

    def __repr__(self):
        return u'%s - %s' % (self.publication_date.isoformat(), self.assigned_url)


class Data(object):

    def __init__(self):
        db_filename = os.path.abspath(os.path.join(const.USER_DIR, 'jpa.db'))
        self.metadata = sa.BoundMetaData('sqlite:///%s' % db_filename)
        self.metadata.engine.echo = True
        self.weblogs_table = sa.Table('weblog', self.metadata,
            sa.Column('weblog_id', sa.Integer, primary_key=True),
            sa.Column('blogger_id', sa.Unicode, nullable=False, unique=True),
            sa.Column('name', sa.Unicode(80), index=True),
            sa.Column('description', sa.Unicode),
        )
        self.publications_table = sa.Table('publication', self.metadata,
            sa.Column('publication_id', sa.Integer, primary_key=True),
            sa.Column('date', sa.DateTime, default=datetime.datetime.utcnow(),
                index=True),
            sa.Column('weblog_id', sa.Integer, sa.ForeignKey('weblog.weblog_id')),
            sa.Column('entry_id', sa.Integer, sa.ForeignKey('entry.entry_id')),
            sa.Column('assigned_url', sa.Unicode),
        )
        self.entries_table = sa.Table('entry', self.metadata,
            sa.Column('entry_id', sa.Integer, primary_key=True),
            sa.Column('created', sa.DateTime, default=datetime.datetime.utcnow(),
                index=True),
            sa.Column('title', sa.Unicode(100), nullable=False),
            sa.Column('text', sa.Unicode),
            sa.Column('content_type', sa.Unicode(20), default=u'markdown'),
            sa.Column('labels', sa.Unicode),
            sa.Column('is_draft', sa.Boolean, default=False),
        )

    def init_tables(self):
        self.weblogs_table.create()
        self.entries_table.create()
        self.publications_table.create()

    def init_mappers(self):
        orm.mapper(Weblog, self.weblogs_table, properties={
            'publications': orm.relation(Publication),
        })
        orm.mapper(Publication, self.publications_table, properties={
            'weblog': orm.relation(Weblog),
            'entry': orm.relation(Entry),
        })
        orm.mapper(Entry, self.entries_table, properties={
            'publications': orm.relation(Publication),
        })
        self.session = orm.create_session()
