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

import threading

from qt import *

import jt_transport2

class Sender:

    threads = []
    
    def __init__(self, receiver):
        self.receiver = receiver
        self.locks = []

    def send(self, message):
        if message['msgid'] in self.locks:
            raise IOError, qApp.translate('Misc', 
                'Already sending this message.', None)
        else:
            self.locks.append(message['msgid'])
            sender = MessageSender(message, self.receiver, self.locks)
            self.threads.append(sender)
            sender.start()

        
class MessageSender(threading.Thread):

    def __init__(self, message, receiver, locks=None):
        threading.Thread.__init__(self, name=message['msgid'])
        self.cfg = receiver.cfg
        self.queue = receiver.events
        self.message = message
        self.locks = locks
        self.status = 'ready'
        
    def run(self):
        transport = jt_transport2.getTransport(self.cfg.getJoggerAddress(),
            self.cfg.getJabberServer(), self.cfg.getJabberUser(),
            self.cfg.getJabberPasswd())
        self.queue.put_nowait(Event(10001))
        transport.send(self.message)
        self.receiver.data.writeMessage(self.message)
        del self.locks[self.locks.index(self.message['msgid'])]
        event = Event(10000)
        event.setData(transport.message)
        self.queue.put_nowait(event)
        self.status = transport.status
        transport.close()

class Event:

    def __init__(self, text):
        self.text = text
        
    def setData(self, data):
        self.eventData = data
        
    def data(self):
        return self.eventData