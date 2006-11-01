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

"""Transport initialization routines"""

__revision__ = '$Id$'

import blogger, xmlrpcblogger, blox, metaweblog
#import jogger

from api import ServiceError, ResourceNotFoundError,\
    ServiceAuthorizationError, ServiceInternalError, ServiceUnavailableError

AVAILABLE = [
    'blogger (Atom)',
    #'jogger.pl',
    'blogger (XML-RPC)',
    'blox.pl',
    'MetaWeblog',
]

TRANSPORTS = {
    'blogger (Atom)': blogger.BloggerTransport,
    #'jogger.pl': jogger.JoggerTransport,
    'blogger (XML-RPC)': xmlrpcblogger.BloggerTransport,
    'blox.pl': blox.BloxTransport,
    'MetaWeblog': metaweblog.MetaWeblogTransport,
}

FEATURES = {
    'blogger (Atom)': ('discovery', 'blogID', 'auth'),
    #'jogger.pl': (),
    'blogger (XML-RPC)': ('discovery', 'blogID', 'auth'),
    'blox.pl': ('discovery', 'blogID', 'auth', 'category', 'media'),
    'MetaWeblog': ('discovery', 'blogID', 'auth', 'categories', 'media'),
}