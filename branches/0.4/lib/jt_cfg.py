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

import os, sys
import ConfigParser

class AppConfig(ConfigParser.RawConfigParser):

    def __init__(self, fileName=None):
        ConfigParser.RawConfigParser.__init__(self)
        self.optionxform = str
        if fileName is not None:
            self.confFileName = fileName
        else:
            self.confFileName = os.path.expanduser('~/.jtrc')
        try:
            f = open(self.confFileName)
            try:
                self.readfp(f)
            finally:
                f.close()
        except IOError:
            # ignore error, when config file does not exists
            pass

    def saveConfig(self):
        f = open(self.confFileName, 'w')
        try:
            self.write(f)
        finally:
            f.close()

    def getOption(self, section, item, default=''):
        try:
            return self.get(section, item)
        except ConfigParser.NoSectionError:
            self.add_section(section)
            return default
        except ConfigParser.NoOptionError:
            return default

    def setOption(self, section, option, value):
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, option, str(value))

    def getFont(self, viewName):
        if not self.cp.has_section('fonts'):
            self.cp.add_section('fonts')
        if self.cp.has_option('fonts', viewName):
            return self.cp.get('fonts', viewName)
        else:
            return self.defFont

    def getWindowSize(self, windowName):
        if self.has_section(windowName):
            return (self.getint(windowName, 'width'),
                self.getint(windowName, 'height'))
        else:
            return (640, 480)

    def getWindowPos(self, windowName):
        if self.has_section(windowName):
            return (self.getint(windowName, 'top'),
                self.getint(windowName, 'left'))
        else:
            return (150, 150)

    def setWindowSize(self, windowName, width, height):
        if not self.has_section(windowName):
            self.add_section(windowName)
        self.set(windowName, 'width', str(width))
        self.set(windowName, 'height', str(height))

    def setWindowPos(self, windowName, left, top):
        if not self.has_section(windowName):
            self.add_section(windowName)
        self.set(windowName, 'left', str(left))
        self.set(windowName, 'top', str(top))

    def getWindowGeometry(self, windowName):
        pos = self.getWindowPos(windowName)
        size = self.getWindowSize(windowName)
        return (pos[1], pos[0], size[0], size[1])

    def setWindowGeometry(self, windowName, geom):
        self.setWindowPos(windowName, geom[0], geom[1])
        self.setWindowSize(windowName, geom[2], geom[3])

    def getDataDir(self, default):
        try:
            return self.get('dirs', 'data')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return default

    def setDataDir(self, dataDir):
        if not self.has_section('dirs'):
            self.add_section('dirs')
        self.set('dirs', 'data', dataDir)

    def getImageDir(self, default):
        try:
            return self.get('dirs', 'images')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return default
        
    def setImageDir(self, imageDir):
        if not self.has_section('dirs'):
            self.add_section('dirs')
        self.set('dirs', 'images', imageDir)
    
    def getDocDir(self, default):
        try:
            return self.get('dirs', 'doc')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return default

    def setDocDir(self, docDir):
        if not self.has_section('dirs'):
            self.add_section('dirs')
        self.set('dirs', 'doc', docDir)

    def getJabberUser(self):
        return self.getOption('jabber', 'username')
    
    def setJabberUser(self, userName):
        self.setOption('jabber', 'username', userName)
   
    def getJabberPasswd(self):
        return self.getOption('jabber', 'passwd')
    
    def setJabberPasswd(self, passwd):
        self.setOption('jabber',  'passwd', passwd)
    
    def getJabberServer(self):
        return self.getOption('jabber', 'server')

    def setJabberServer(self, server):
        self.setOption('jabber', 'server', server)

    def getJoggerAddress(self):
        return self.getOption('jogger', 'address')

    def setJoggerAddress(self, address):
        self.setOption('jogger', 'address', address)


if __name__ == '__main__':
    c = AppConfig()
