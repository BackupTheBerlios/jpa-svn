#! /usr/bin/env python
# -*- coding: ISO8859-2 -*-

# This file is part of JPA.
# Copyright: (C) 2003, 2004 Jarek Zgoda <jzgoda@gazeta.pl>
#
# JPA is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JPA; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

__PIPE = '/tmp/xmms-info'

import os

import id3reader

import jt_cfg

def getTrack():
    try:
        f = open(__PIPE)
        try:
            lines = f.read().strip().split('\n')
        finally:
            f.close()
    except IOError:
        # nothing to read
        pass
    else:
        k, v = lines[-1].split(':', 1)
        fileName = v.strip()
        # check, if "filename" is real file -- sometimes it can be URL!
        if os.path.isfile(fileName):
            id3 = id3reader.Reader(fileName)
            performer = id3.getValue('performer')
            title = id3.getValue('title')
            if not None in (performer, title):
                return (performer, title)

def getTrackInfo(pattern):
    if pattern:
        info = getTrack()
        if info is not None:
            return pattern % (info)
