# -*- coding: UTF-8 -*-

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

import locale, time

import pyxmpp
import pyxmpp.jabber

import textile

class TransportError(Exception):
    """Any network-related problem."""
    pass


class JabberTransport(pyxmpp.jabber.Client):

    def __init__(self, address, serverName, userName, passwd):
        l = locale.getlocale()
        if l[0] is None:
            l = locale.getdefaultlocale()
        self.enc = l[1]
        self.address = address
        self.serverName = serverName
        self.JID = pyxmpp.JID(userName + '/JPA')
        self.passwd = passwd
        self.status = 'ready'
        self.message = None
        self.timeout = 30 # ticks
        self.connected = False

    def send(self, message):
        if not self.connected:
            self.status = 'connecting'
            try:
                self.conn.connect()
                self.status = 'connected'
                self.connected = True
                self.conn.registerHandler('message', self.msgCallback)
                self.conn.setDisconnectHandler(self.closeCallback)
            except IOError, e:
                self.status = 'error'
                self.message = str(e)
                exit()
        msg = self.prepareMsg(message)
        self.status = 'logging in'
        if self.conn.auth(self.userName, self.passwd, 'JPA'):
            self.status = 'logged in'
            self.conn.sendInitPresence()
            p = jabber.Presence()
            p.setPriority('9')
            try:
                self.conn.send(p)
            except Exception, e:
                raise TransportError, e
        else:
            raise TransportError, 'Could not authorize user'
        self.conn.send(msg)
        self.status = 'message sent'
        if not message.has_key('sent'):
            message['sent'] = []
        message['sent'].append(time.localtime())
        i = 0
        while (i <= self.timeout) and (self.status != 'message received'):
            i = i + 1
            self.conn.process(1)
        if i == self.timeout:
            self.status = 'timed out'

    def prepareMsg(self, message):
        msg = jabber.Message(to=self.address)
        msg.setSubject(message['title'].strip())
        if message['content-type'] == 'textile':
            body = textile.textile(message['body'].strip())
        else:
            body = message['body'].strip()
        if message.has_key('level') and (message['level'] != '-1'):
            body = '<LEVEL%s>%s' % (message['level'], body.strip())
        msg.setBody(body)
        return msg

    def setTimeout(self, value):
        self.timeout = value
        
    def close(self):
        self.conn.disconnect()


def getTransport(address, serverName, userName, passwd):
    return JabberTransport(address, serverName, userName, passwd)
