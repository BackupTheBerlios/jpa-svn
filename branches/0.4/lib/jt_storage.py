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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JPA; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os, glob
import shelve

def listFiles(directory, pattern='*.*', revOrder=True):
    tmp = glob.glob(os.path.join(directory, pattern))
    tmp.sort()
    if revOrder:
        tmp.reverse()
    return tmp


class Storage:
    def __init__(self, fileName):
        self.fileName = fileName
        self.__s = shelve.open(fileName, 'c')
    
    def getMsg(self, msgId):
        if self.__s.has_key(msgId):
            return self.__s[msgId]
    
    def writeMsg(self, message):
        self.__s[message.msgId] = message
    
    def deleteMsg(self, msgId):
        del self.__s[msgId]
    
    def flush(self):
        self.__s.close()
        self.__s = shelve.open(self.fileName)
    
    def openFile(self, fileName):
        self.__s.close()
        self.fileName = fileName
        self.__s = shelve.open(fileName, 'c')
    
    def close(self):
        self.__s.close()
    
    def getEntries(self):
        tmp = self.__s.keys()
        if tmp:
            tmp.sort()
            return tmp

    def export(self, fileName):
        f = open(fileName, 'w')
        try:
            ids = self.getEntries()
            first = True
            for msgId in ids:
                msg = self.__s[msgId]
                if first:
                    f.write(msg.title + '\n')
                else:
                    f.write('\f\n' + msg.title + '\n')
                f.write(msg.body + '\n\n')
        finally:
            f.close()
    
    def __del__(self):
        if self.__s:
            self.__s.close()

    def __getitem__(self, index):
        return self.__s[index]
    
    def __setitem__(self, index, value):
        self.__s[index] = value

