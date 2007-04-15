# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Application data model and support routines."""

__revision__ = '$Id$'

import os
import datetime

import sqlobject as so

import const


BODY_TYPES = ['plain', 'markdown', 'HTML']


class Label(so.SQLObject):
    title = so.UnicodeCol(alternateID=True, notNone=True)
    entries = so.RelatedJoin('Entry')


class Weblog(so.SQLObject):
    name = so.UnicodeCol(alternateID=True)
    weblog_id = so.UnicodeCol(default=None)
    is_active = so.BoolCol(default='t', notNone=True)
    active_idx = so.DatabaseIndex(is_active)


class Entry(so.SQLObject):
    created = so.DateTimeCol(default=datetime.datetime.utcnow)
    title = so.UnicodeCol()
    text = so.UnicodeCol()
    text_type = so.EnumCol(enumValues=BODY_TYPES, default='plain')
    is_draft = so.BoolCol(default='f')
    publications = so.MultipleJoin('Publication', orderBy='-published')
    labels = so.RelatedJoin('Label')
    created_idx = so.DatabaseIndex(created)
    title_idx = so.DatabaseIndex(title)


class Publication(so.SQLObject):
    published = so.DateTimeCol(notNone=True,
        default=datetime.datetime.utcnow)
    entry = so.ForeignKey('Entry')
    weblog = so.ForeignKey('Weblog')
    assigned_id = so.UnicodeCol()
    pub_idx = so.DatabaseIndex(published)


# module initialization
def init_model():
    _db_filename = os.path.abspath(os.path.join(const.USER_DIR, 'jpa.db'))
    schema_empty = False
    if not os.access(_db_filename, os.F_OK):
        schema_empty = True
        root, tail = os.path.split(_db_filename)
        if not os.path.isdir(root):
            os.makedirs(root)
    if os.name == 'nt':
        uri = _db_filename.replace(':', '|').replace('\\', '/')
        uri = 'sqlite:///%s' % uri
    else:
        uri = 'sqlite://%s' % _db_filename
    connection = so.connectionForURI(uri)
    so.sqlhub.processConnection = connection
    Entry.createTable(ifNotExists=True)
    Label.createTable(ifNotExists=True)
    Publication.createTable(ifNotExists=True)
    Weblog.createTable(ifNotExists=True)
