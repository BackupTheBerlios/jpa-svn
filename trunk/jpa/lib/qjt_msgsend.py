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

from qt import *

import jt_transport2

def sendMessage(message, cfg):
    sender = MessageSender(message, cfg)
    sender.run()


class Sender:

    def __init__(self, receiver):
        self.receiver = receiver
        self.threads = []

    def send(self, message):
        sender = MessageSender(message, self.receiver)
        self.threads.append(sender)
        sender.run()

    def __del__(self):
        # Boudewijn Rempt says it's necessary and he knows PyQt better, than
        # anyone, so I will not try to be smarter...
        for t in self.threads:
            running = t.running()
            t.stop()
            if not t.finished():
                t.wait()


class MessageSender(QThread):

    def __init__(self, msg, receiver):
        QThread.__init__(self)
        self.name = msg['msgid']
        self.receiver = receiver
        self.cfg = receiver.cfg
        self.message = msg
        self.mutex = QMutex()
        self.stopped = False
        self.status = 'ready'
    
    def run(self):
        if not self.mutex.tryLock():
            raise IOError, qApp.translate('Misc', 
                'Already sending this message.', None)
            return
        if not self.stopped:
            transport = jt_transport2.getTransport(self.cfg.getJoggerAddress(),
                self.cfg.getJabberServer(), self.cfg.getJabberUser(),
                self.cfg.getJabberPasswd())
            event = QCustomEvent(10001)
            QThread.postEvent(self.receiver, event)
            transport.send(self.message)
            self.receiver.data.writeMessage(self.message)
            self.mutex.unlock()
            event = QCustomEvent(10000)
            event.setData(transport.message)
            QThread.postEvent(self.receiver, event)
            self.status = transport.status
            transport.close()

    def stop(self):
        self.stopped = True
