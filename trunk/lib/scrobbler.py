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

"""Audioscrobbler user data retrieval"""

__revision__ = '$Id$'

import urllib
try:
    import cElementTree as ElementTree
except ImportError:
    from elementtree import ElementTree

AS_URL = 'http://ws.audioscrobbler.com/1.0/user/%s/recenttracks.xml'

def getLastTrack(userName, proxyConfig=None):
    proxy = {}
    if proxyConfig:
        proxy['http'] = 'http://%(host)s:%(port)d' % proxyConfig
    fp = urllib.urlopen(AS_URL % userName, proxies=proxy)
    doc = fp.read()
    tree = ElementTree.fromstring(doc)
    last = tree.find(u'track')
    if last is not None:
        ret = {}
        ret['artist'] = last.find(u'artist').text
        ret['track'] = last.find(u'name').text
        ret['url'] = last.find(u'url').text
        return ret