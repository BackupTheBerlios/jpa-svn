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

from qt import *

import jt_const
import jt_version

from aboutdialog_impl import AboutDialogImpl

def showAboutDialog(parent):
    dlg = AboutDialog(parent=parent)
    dlg.exec_loop()

class AboutDialog(AboutDialogImpl):

    def __init__(self, parent=None, name=None, modal=0, fl=0):
        AboutDialogImpl.__init__(self, parent, name, modal, fl)
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            licFile = os.path.join(jt_const.PATHS['doc'], 'COPYING')
            f = open(licFile)
            try:
                self.tbLicense.setText(f.read())
            finally:
                f.close()
            self.lbProgVer.setText(unicode(self.__tr('Version: %s')) % \
                jt_version.VERSION)
        finally:
            qApp.restoreOverrideCursor()

    def __tr(self, s, c=None):
        return qApp.translate("AboutDialogImpl", s, c)
