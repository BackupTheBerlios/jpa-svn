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

import os, time
import os.path as op
import copy

from qt import *

from msgimport_impl import MsgImportDialogImpl

import asynchttp
import jt_storage2, jt_const

def importMessages(parent, config):
    dlg = MsgImportDialog(config, parent=parent)
    dlg.show()

class MsgImportDialog(MsgImportDialogImpl):

    def __init__(self, config, parent=None, name=None, modal=0, fl=0):
        MsgImportDialogImpl.__init__(self, parent, name, modal, fl)
        self.cfg = config
        # the "import mode" maps directly to source selection
        self.importMode = 0

    def typeClick(self, buttonId):
        self.importMode = buttonId
        self.btnSelectFile.setEnabled(buttonId != 1)

    def selectFileClick(self):
        startDir = op.expanduser('~/')
        if self.importMode == 0:
            # 2004-01-26
            # Sparrow has something to do in Jogger -- we will work here later
            fileFilter = ''
        else:
            # importing from old (0.3.x) JPA database
            fileFilter = self.__tr('Data files (*.dat);;All files (*.*)')
        fileName = QFileDialog.getOpenFileName(startDir, fileFilter, self,
            None, self.__tr('Open file'), None, True)
        self.edFileLoc.setText(fileName)

    def selectDestFileClick(self):
        startDir = self.cfg.getDataDir(op.join(op.expanduser('~/'),
            'jpadata'))
        fileFilter = self.__tr('Data files (*.dat);;All files (*.*)')
        fileName = QFileDialog.getSaveFileName(startDir, fileFilter, self,
            None, self.__tr('Save file'), None, True)
        self.edDestLoc.setText(fileName)

    def startImportClick(self):
        if self.__checkCanImport():
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                self.__importData()
            finally:
                qApp.restoreOverrideCursor()

    def __checkCanImport(self):
        srcLoc = unicode(self.edFileLoc.text())
        dstLoc = self.edDestLoc.text()
        return \
            (dstLoc != QString.null) and \
            ((srcLoc[:7] == 'http://') or (op.isfile(srcLoc)))

    def __importData(self):
        self.pbImportProgress.reset()
        cdt = time.localtime()
        fileName = unicode(self.edFileLoc.text())
        dst = unicode(self.edDestLoc.text())
        if self.importMode == 0:
            # leave it for now...
            pass
        elif self.importMode == 1:
            # this also still doesn't work...
            pass
        else:
            import jt_storage
            data = jt_storage.Storage(fileName)
            dest = jt_storage2.Storage(dst)
            en = data.getEntries()
            self.pbImportProgress.setTotalSteps(len(en))
            i = 0
            for msgId in en:
                i = i + 1
                self.pbImportProgress.setProgress(i)
                entry = data[msgId]
                # we don't want to modify the template...
                newEntry = copy.deepcopy(jt_const.EMPTY_MSG)
                newEntry['msgid'] = entry.msgId
                # JPA 0.3.x saved dates as textual representation in format
                # yyyy-mm-dd hh:nn, so we need to strptime() them to get time_t
                newEntry['created'] = time.strptime(entry.created,
                    '%Y-%m-%d %H:%M')
                if entry.sent:
                    newEntry['sent'].append(time.strptime(entry.dateSent,
                        '%Y-%m-%d %H:%M'))
                # JPA 0.3.x saved messages not as unicode objects, but as byte
                # strings, so we need to convert them now...
                newEntry['title'] = entry.title.decode(jt_const.enc)
                newEntry['body'] = entry.body.decode(jt_const.enc)
                newEntry['edited'].append(cdt)
                # message body is textile markup, so we don't touch 
                # its content-type, leave as is
                dest.writeMessage(newEntry)
            dest.close()
        self.pbImportProgress.reset()

    def __tr(self, s, c=None):
        return qApp.translate("MsgImportDialogImpl", s, c)
