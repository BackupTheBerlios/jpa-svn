# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003 - 2006 Jarek Zgoda <jzgoda@o2.pl>
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

"""Webservice client framework.

User web identity (credentials, authorization, etc.)."""

__revision__ = '$Id$'


class Identity:
    """User identity at web service hub."""

    def __init__(self, name, user_credentials):
        self.name = name
        self.credentials = user_credentials

    def authorize(self):
        """Authorize user at service. All needed data should be already
        available in credentials dictionary."""
        raise NotImplementedError

    def get_services(self, service_type='all'):
        """Get list of user web services of specified type or all user
        services."""
        raise NotImplementedError
