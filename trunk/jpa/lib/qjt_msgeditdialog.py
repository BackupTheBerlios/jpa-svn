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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JPA; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import time
try:
    import myspell
except ImportError:
    has_myspell = False
else:
    has_myspell = True

from qt import *

from msgeditdialog_impl import MsgEditDialogImpl
import jt_const, qjt_msgpreviewdialog, jt_xmmsinfo, qjt_spellcheckdialog

def msgNew(parent, config):
    tm = time.localtime()
    msg = {'msgid': time.strftime('%Y%m%d%H%M%S', tm), \
        'created': tm, \
        'edited': [], \
        'title': '', \
        'body': '', \
        'level': '0', \
        'content-type': 'textile', \
        'eid': ''}
    pattern = config.getData('misc', 'xmms_pattern', '')
    if len(pattern) > 0:
        info = jt_xmmsinfo.getTrackInfo(pattern)
        if info is not None:
            msg['body'] = '\n\n' + info
    dlg = MsgEditDialog(msg, parent=parent)
    if (dlg.exec_loop() == 1):
        title = unicode(dlg.edTitle.text()).strip()
        body = unicode(dlg.teBody.text()).strip()
        bodyType = unicode(dlg.cbxMsgType.currentText()).strip()
        level = unicode(dlg.sbxLevel.text())
        if (len(title) > 0) or (len(body) > 0):
            msg['title'] = title
            msg['body'] = body
            msg['edited'].append(time.localtime())
            msg['content-type'] = bodyType
            msg['level'] = level
            return msg

def msgEdit(parent, message):
    dlg = MsgEditDialog(message, parent=parent)
    if (dlg.exec_loop() == 1):
        title = unicode(dlg.edTitle.text()).strip()
        body = unicode(dlg.teBody.text()).strip()
        bodyType = unicode(dlg.cbxMsgType.currentText()).strip()
        level = unicode(dlg.sbxLevel.text())
        if (len(title) > 0) or (len(body) > 0):
            message['title'] = title
            message['body'] = body
            message['edited'].append(time.localtime())
            message['content-type'] = bodyType
            message['level'] = level
            for k, v in jt_const.EMPTY_MSG.items():
                if not k in message:
                    message[k] = v
            return message


class MsgEditDialog(MsgEditDialogImpl):

    def __init__(self, message, parent, name=None, modal=0, fl=0):
        MsgEditDialogImpl.__init__(self, parent, name, modal, fl)
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.parent = parent
            self.msg = message
            self.edTitle.setText(message['title'])
            self.teBody.setText(message['body'])
            self.cbxMsgType.setCurrentText(message['content-type'])
            if message.has_key('level'):
                self.sbxLevel.setValue(int(message['level']))
            self.btnSpellCheck.setEnabled(has_myspell)
        finally:
            qApp.restoreOverrideCursor()

    def previewClick(self):
        msg = {}
        msg['title'] = unicode(self.edTitle.text()).strip()
        msg['body'] = unicode(self.teBody.text()).strip()
        msg['content-type'] = unicode(self.cbxMsgType.currentText()).strip()
        qjt_msgpreviewdialog.msgPreview(self, msg)
    
    def checkClick(self):
        curText = unicode(self.teBody.text())
        newText = qjt_spellcheckdialog.checkSpelling(curText, self)
        if newText != curText:
            self.teBody.setText(newText)

    def closeEvent(self, e):
        pass
