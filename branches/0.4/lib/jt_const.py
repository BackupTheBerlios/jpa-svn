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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JPA; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

__revision__ = '$Id$'

import locale

PARENT = None

PATHS = {}

enc = locale.getdefaultlocale()[1]

MSGTEMPLATE = '<html><head>'\
    '<meta http-equiv="Content-Type" content="text/html; '\
    'charset=' + enc + '">'\
    '<title>%s</title>'\
    '</head>'\
    '<body>%s</body>'\
    '</html>'

PATHS = {}

APP_OBJECT = None

EMPTY_MSG = {'msgid': '', \
    'created': '', \
    'edited': [], \
    'sent': [], \
    'title': '', \
    'body': '', \
    'level': '0', \
    'content-type': 'textile', \
    'eid': ''}

TRUE_VALUES = (True, 'True', 1, '1', 'Yes', 'On', 'yes', 'true', 'on')

AS_URL = 'http://ws.audioscrobbler.com/1.0/user/%s/recenttracks.xml'

