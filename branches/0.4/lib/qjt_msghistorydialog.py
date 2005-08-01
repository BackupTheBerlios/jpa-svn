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

import time

from qt import *

from msghistorydialog_impl import MsgHistoryDialogImpl

def showMessageHistory(parent, message):
    dlg = MsgHistoryDialog(message, parent=parent)
    dlg.exec_loop()


class MsgHistoryDialog(MsgHistoryDialogImpl):

    def __init__(self, message, parent=None, name=None, modal=0, fl=0):
        MsgHistoryDialogImpl.__init__(self, parent, name, modal, fl)
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.lbCreated.setText(time.strftime('%Y-%m-%d %H:%M:%S',
                message['created']))
            edited = []
            for entry in message['edited']:
                edited.append(time.strftime('%Y-%m-%d %H:%M:%S', entry))
            self.lbxEdited.insertStrList(edited)
            self.lbxEdited.sort(False)
            self.lbxEdited.setCurrentItem(0)
            self.lbxEdited.setSelected(0, True)
            if message.has_key('sent'):
                sent = []
                for entry in message['sent']:
                    sent.append(time.strftime('%Y-%m-%d %H:%M:%S', entry))
                if len(sent) > 0:
                    self.lbxSent.insertStrList(sent)
                    self.lbxSent.sort(False)
                    self.lbxSent.setCurrentItem(0)
                    self.lbxSent.setSelected(0, True)
        finally:
            qApp.restoreOverrideCursor()
