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

Service model and basic implementations."""

__revision__ = '$Id$'


class WebService:
    """Web service abstract prototype"""
    pass


class Weblog(WebService):
    """Remote access to weblog service"""

    def post_entry(self, entry):
        """Post new entry to weblog service."""
        raise NotImplementedError

    def post_modified(self, entry):
        """Post updated entry to weblog service"""
        raise NotImplementedError

    def get_latest_entries(self, num_entries=20):
        """Retrieve list of recently published entries"""
        raise NotImplementedError

    def get_entry(self, entry_id):
        """Retrieve single entry from weblog service"""
        raise NotImplementedError

    def delete_entry(self, entry_id):
        """Delete single entry from weblog service"""
        raise NotImplementedError
