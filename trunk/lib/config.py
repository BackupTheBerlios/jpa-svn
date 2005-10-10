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

"""Global configuration maintenance."""

__revision__ = '$Id$'

import os.path

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

class AppConfig(SafeConfigParser):
    """Based on ConfigParser, this class is generic configuration processor.
    Only few new methods were added."""

    def __init__(self, fileName):
        SafeConfigParser.__init__(self)
        self.fileName = fileName
        self.optionxform = str
        if os.path.exists(fileName):
            fp = open(fileName, 'r')
            try:
                self.readfp(fp)
            finally:
                fp.close()

    def saveConfig(self, fileName=None):
        """Save configuration file. If name was given, use it instead of
        default."""
        if fileName is None:
            saveTo = self.fileName
        else:
            saveTo = fileName
        fp = open(saveTo, 'w')
        try:
            self.write(fp)
        finally:
            fp.close()

    def getOption(self, section, option, default=None):
        """Get option value. Don't raise any exception if option or
        section does not exists, just return default value."""
        try:
            return self.get(section, option)
        except (NoSectionError, NoOptionError):
            return default

    def setOption(self, section, option, value):
        """Set option value. If section does not exists, add it."""
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, option, value)