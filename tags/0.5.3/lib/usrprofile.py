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

"""User profile settings maintenance."""

__revision__ = '$Id$'

class UserProfile:
    """User profile maintenance."""
    
    def __init__(self, name, default=False):
        self.name = name
        self.default = default
        self.weblog = {}
        self.user = {}

    def readProfile(self, cfg):
        """Read profile data from ConfigParser object."""
        #FIXME: implement real profile system based on subsections
        for (key, value) in cfg.items(self.name):
            if key[:4] == 'log.':
                self.weblog[key] = value
            elif key[:4] == 'usr.':
                self.user[key] = value

    def writeProfile(self, cfg):
        """Write profile data into ConfigParser object."""
        for (option, value) in self.weblog.items():
            cfg.set(self.name, option, value)
        for (option, value) in self.user.items():
            cfg.set(self.name, option, value)
        if self.default:
            cfg.set('weblogs', 'default', self.name)
