# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2004 Jarek Zgoda <jzgoda@gazeta.pl>
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

import os
import os.path as op
import cPickle

try:
    # try to use more advanced PyBSDDB
    import bsddb3 as bsddb
except ImportError:
    # stick to default
    import bsddb

class Storage:

    def __init__(self, fileName):
        dirName = op.dirname(fileName)
        if not op.isdir(dirName):
            os.makedirs(dirName)
        self.fileName = fileName
        self.__data = bsddb.hashopen(fileName, 'c')

    def getMessage(self, msgId):
        return cPickle.loads(self.__data[msgId])

    def writeMessage(self, message):
        self.__data[message['msgid']] = cPickle.dumps(message, -1)

    def deleteMessage(self, msgId):
        del self.__data[msgId]

    def flush(self):
        self.__data.sync()

    def close(self):
        self.__data.close()

    def loadFile(self, fileName):
        self.__data.close()
        self.fileName = fileName
        self.__data = bsddb.hashopen(fileName, 'c')

    def getEntries(self):
        tmp = self.__data.keys()
        if tmp:
            tmp.sort()
            return tmp
        else:
            return []

    def export(self, fileName, encoding):
        f = open(fileName, 'w')
        try:
            ids = self.getEntries()
            first = True
            for msgId in ids:
                msg = self.getMessage(msgId)
                if first:
                    f.write(msg['title'].encode(encoding) + '\n')
                    first = False
                else:
                    f.write('\f\n' + msg['title'].encode(encoding) + '\n')
                f.write(msg['body'].encode(encoding) + '\n\n')
        finally:
            f.close()

    def __del__(self):
        if self.__data is not None:
            self.__data.close()

