# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Transport package initialization"""

__revision__ = '$Id$'

from gdata import service as gdataservice

import const

# service singleton
__service = None

def get_service(login, password):
    global __service
    if not __service:
        __service = gdataservice.GDataService(login, password)
        __service.source = 'zgoda-JPA-%s' % const.VERSION_STRING
        __service.service = 'blogger'
        __service.server = 'www.blogger.com'
    return __service
