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

# $Id$

"""User profile settings maintenance."""

__revision__ = '$Revision$'

class UserProfile:
    """User profile maintenance."""
    
    def __init__(self, name):
        self.name = name
        self.options = {}

    def readProfile(self, cfg):
        """Read profile data fro ConfigParser object."""
        for (key, value) in cfg.items(self.name):
            self.options[key] = value

    def writeProfile(self, cfg):
        """Write profile data into ConfigParser object."""
        for option in self.options.keys():
            cfg.set(option, self.options[option])

    def getOption(self, option, default=None):
        """Get specified option value, or default if not exists."""
        try:
            return self.options[option]
        except KeyError:
            return default