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

import os
import os.path as op
import time

from qt import *
import textile

import jt_cfg, jt_storage2, qjt_msgeditdialog, qjt_optionsdialog, \
    qjt_msgimport, qjt_aboutdialog, jt_const, qjt_msghistorydialog, \
    qjt_msgsend, qjt_archviewdialog, qjt_pixmapprovider, qjt_cfg
from mainform2_impl import MainFormImpl
from jt_version import VERSION
from jt_const import MSGTEMPLATE


class MainForm(MainFormImpl):

    def __init__(self, parent=None, name=None, fl=0):
        MainFormImpl.__init__(self, parent, name, fl)
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.cfg = qjt_cfg.AppConfig()
            self.vb = QVBox(self)
            self.vb.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            self.ws = QWorkspace(self.vb)
            self.ws.setScrollBarsEnabled(True)
            self.setCentralWidget(self.vb)
            self.pp = qjt_pixmapprovider.PixmapProviderFactory().getProvider()
            if self.pp.pixmaps == []:
                self.toolBar.hide()
            else:
                self.__loadPixmaps()
        finally:
            qApp.restoreOverrideCursor()
            
    ### actions ###
    
    def helpAbout(self):
        qjt_aboutdialog.showAboutDialog(self)
    
    def helpAboutQt(self):
        QMessageBox.aboutQt(self, 'Jogger Publishing Assistant')
    
    ### events ###

    def closeEvent(self, e):
        e.accept()
        
    ### private methods ###
        
    def __loadPixmaps(self):
        i = QIconSet()
        if self.pp['filenew'] is not None:
            i.setPixmap(self.pp['filenew'], QIconSet.Automatic)
            self.acFileNew.setIconSet(i)
        if self.pp['fileopen'] is not None:
            i.setPixmap(self.pp['fileopen'], QIconSet.Automatic)
            self.acFileOpen.setIconSet(i)
        if self.pp['exit'] is not None:
            i.setPixmap(self.pp['exit'], QIconSet.Automatic)
            self.acFileExit.setIconSet(i)
        if self.pp['editcut'] is not None:
            i.setPixmap(self.pp['editcut'], QIconSet.Automatic)
            self.acEditCut.setIconSet(i)
        if self.pp['editcopy'] is not None:
            i.setPixmap(self.pp['editcopy'], QIconSet.Automatic)
            self.acEditCopy.setIconSet(i)
        if self.pp['editpaste'] is not None:
            i.setPixmap(self.pp['editpaste'], QIconSet.Automatic)
            self.acEditPaste.setIconSet(i)
        if self.pp['mail_new'] is not None:
            i.setPixmap(self.pp['mail_new'], QIconSet.Automatic)
            self.acMsgNew.setIconSet(i)
        if self.pp['edit'] is not None:
            i.setPixmap(self.pp['edit'], QIconSet.Automatic)
            self.acMsgEdit.setIconSet(i)
        if self.pp['mail_delete'] is not None:
            i.setPixmap(self.pp['mail_delete'], QIconSet.Automatic)
            self.acMsgDelete.setIconSet(i)
        if self.pp['filesave'] is not None:
            i.setPixmap(self.pp['filesave'], QIconSet.Automatic)
            self.acMsgSave.setIconSet(i)
        if self.pp['mail_send'] is not None:
            i.setPixmap(self.pp['mail_send'], QIconSet.Automatic)
            self.acMsgSend.setIconSet(i)
        if self.pp['configure'] is not None:
            i.setPixmap(self.pp['configure'], QIconSet.Automatic)
            self.acToolsOptions.setIconSet(i)

    def __tr(self, s, c=None):
        return qApp.translate("MainFormImpl", s, c)


if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MainForm()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
