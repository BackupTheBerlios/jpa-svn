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

EMPTY_PROFILE = {'name': '', \
    'default': False, \
    'jogger address': '', \
    'jabber server': '', \
    'jabber username': '', \
    'jabber password': '', \
    'jabber port': 5222, \
    'use ssl': False, \
    'replacements': {}\
    }

class AppConfig:

    def __init__(self):
        if sys.platform == 'win32':
            self.confFileName = os.path.join(os.getcwd(), 'jt.ini')
            self.defFont = 'arial|8|9|10|12|14|16|18'
        else:
            self.confFileName = os.path.expanduser('~/.jtrc')
            self.defFont = 'helvetica|8|9|10|12|14|16|18'
        self.profiles = dict()
        self.cp = ConfigParser.ConfigParser()
        try:
            f = open(self.confFileName)
            try:
                self.cp.readfp(f)
            finally:
                f.close()
            self.__loadProfiles()
        except IOError:
            # ignore error, when config file does not exists
            pass
            
    def __loadProfiles(self):
        self.currentProfile = ''
        name = ''
        for section in self.cp.sections():
            if section.startswith('profile_'):
                name = section[8:]
                cfgItems = dict(self.cp.items(section))
                self.profiles[name] = cfgItems.copy()
                self.profiles[name]['name'] = name
                try:
                    if self.profiles[name]['default'] == 'True':
                        self.setCurrentProfile(name)
                except KeyError:
                    # ignore, no profile has been set as default yet
                    pass
        if self.currentProfile == '' and name != '':
            self.setCurrentProfile(name)

    def writeProfile(self, items):
        section = 'profile_' + items['name']
        self.profiles[items['name']] = items
        if not self.cp.has_section(section):
            self.cp.add_section(section)
        # first set other's "default" flag to false if this one
        # should be the default
        try:
            if items['default']:
                for profile in self.profiles.iterkeys():
                    if self.profiles[profile]['name'] == items['name']:
                        pass
                    else:
                        self.profiles[profile]['default'] = False
        except KeyError:
            # ignore errors when reading old configuration files
            pass
        for key in items.iterkeys():
            self.cp.set(section, key, items[key])
            
    def getDefaultProfile(self):
        for section in self.cp.sections():
            try:
                if section.startswith('profile_'):
                    if self.cp.getboolean(section, 'default'):
                        self.defaultProfile = section[8:]
                        break
            except ConfigParser.NoOptionError:
                continue

    def saveConfig(self):
        # write all edits to profiles
        for profile in self.profiles.iterkeys():
            self.writeProfile(self.profiles[profile])
        f = open(self.confFileName, 'w')
        try:
            self.cp.write(f)
        finally:
            f.close()

    def getData(self, section, item, default=''):
        if self.cp.has_option(section, item):
            return self.cp.get(section, item)
        else:
            if not self.cp.has_section(section):
                self.cp.add_section(section)
            self.cp.set(section, item, default)
            return default

    def setOption(self, section, option, value):
        if not self.cp.has_section(section):
            self.addSection(section)
        if not self.cp.has_option(section, option):
            self.cp.add_option(section, option)
        self.cp.set(section, option, str(value))

    def addSection(self, section):
        self.cp.add_section(section)

    def getFont(self, viewName):
        if not self.cp.has_section('fonts'):
            self.cp.add_section('fonts')
        if self.cp.has_option('fonts', viewName):
            return self.cp.get('fonts', viewName)
        else:
            return self.defFont

    def getWindowSize(self, windowName):
        if self.cp.has_section(windowName):
            return (self.cp.getint(windowName, 'width'),
                self.cp.getint(windowName, 'height'))
        else:
            return (640, 480)

    def getWindowPos(self, windowName):
        if self.cp.has_section(windowName):
            return (self.cp.getint(windowName, 'top'),
                self.cp.getint(windowName, 'left'))
        else:
            return (150, 150)

    def setWindowSize(self, windowName, width, height):
        if not self.cp.has_section(windowName):
            self.cp.add_section(windowName)
        self.cp.set(windowName, 'width', str(width))
        self.cp.set(windowName, 'height', str(height))

    def setWindowPos(self, windowName, left, top):
        if not self.cp.has_section(windowName):
            self.cp.add_section(windowName)
        self.cp.set(windowName, 'left', str(left))
        self.cp.set(windowName, 'top', str(top))

    def getWindowGeometry(self, windowName):
        pos = self.getWindowPos(windowName)
        size = self.getWindowSize(windowName)
        return (pos[1], pos[0], size[0], size[1])

    def setWindowGeometry(self, windowName, geom):
        self.setWindowPos(windowName, geom[0], geom[1])
        self.setWindowSize(windowName, geom[2], geom[3])

    def getDataDir(self, default):
        if self.cp.has_option('dirs', 'data'):
            return self.cp.get('dirs', 'data')
        else:
            return default

    def setDataDir(self, dataDir):
        if not self.cp.has_section('dirs'):
            self.cp.add_section('dirs')
        self.cp.set('dirs', 'data', dataDir)

    def getImageDir(self, default):
        if self.cp.has_option('dirs', 'images'):
            return self.cp.get('dirs', 'images')
        else:
            return default
        
    def setImageDir(self, imageDir):
        if not self.cp.has_section('dirs'):
            self.cp.add_section('dirs')
        self.cp.set('dirs', 'images', imageDir)
    
    def getDocDir(self, default):
        if self.cp.has_option('dirs', 'doc'):
            return self.cp.get('dirs', 'doc')
        else:
            return default

    def setDocDir(self, docDir):
        if not self.cp.has_section('dirs'):
            self.cp.add_section('dirs')
        self.cp.set('dirs', 'doc', docDir)

    def getCurrentProfileOption(self, name):
        try:
            return self.profiles[self.currentProfile][name]
        except KeyError:
            # ignore any errors, we build new configuration
            pass

    def setCurrentProfileOption(self, name, value):
        self.profiles[self.currentProfile][name] = value

    def getJabberUser(self):
        return self.getCurrentProfileOption('jabber username')
   
    def getJabberPasswd(self):
        return self.getCurrentProfileOption('jabber password')
    
    def setJabberPasswd(self, passwd):
        self.setCurrentProfileOption('jabber password', passwd)
    
    def getJabberServer(self):
        return self.getCurrentProfileOption("jabber server")
     
    def getJoggerAddress(self):
        return self.getCurrentProfileOption("jogger address")

    def useReplacements(self, text):
        try:
            rDict = eval(self.profiles[self.currentProfile]['replacements'])
        except:
            rDict = dict()
        for regex, repl in rDict.iteritems():
            text = text.replace(regex, repl)
        return text

    def setCurrentProfile(self, name):
        self.currentProfile = name

    def getCurrentProfile(self):
        return self.currentProfile


if __name__ == '__main__':
    c = AppConfig()
