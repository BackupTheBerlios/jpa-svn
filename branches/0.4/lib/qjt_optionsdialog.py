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

from qt import *

from optionsdialog_impl import OptionsDialogImpl

import jt_xmmsinfo, jt_const, jt_cfg
from jt_const import TRUE_VALUES
import textile

def editOptions(parent, config):
    dlg = OptionsDialog(config, parent=parent)
    if (dlg.exec_loop() == 1):
        dlg.saveConfig()


class OptionsDialog(OptionsDialogImpl):

    def __init__(self, config, parent=None, name=None, modal=0, fl=0):
        OptionsDialogImpl.__init__(self, parent, name, modal, fl)
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.cfg = config
            self.edJoggerJID.setText(config.getJoggerAddress())
            self.edJabberServer.setText(config.getJabberServer())
            self.edJID.setText(config.getJabberUser())
            self.edPasswd.setText(config.getJabberPasswd())
            pattern = config.getOption('misc', 'xmms_pattern',
                'p. (NP: %s &mdash; _%s_)')
            self.edXmmsInfoFormat.setText(pattern)
            trackInfo = jt_xmmsinfo.getTrackInfo(pattern)
            if trackInfo is not None:
                self.lbXmmsEx.setText(textile.textile(trackInfo))
            else:
                self.lbXmmsEx.setText(QString.null)
        finally:
            qApp.restoreOverrideCursor()

    def saveConfig(self):
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.cfg.setJoggerAddress(unicode(self.edJoggerJID.text()))
            self.cfg.setJabberServer(unicode(self.edJabberServer.text()))
            self.cfg.setJabberUser(unicode(self.edJID.text()))
            self.cfg.setJabberPasswd(unicode(self.edPasswd.text()))
            if self.gxXmms.isChecked():
                pattern = unicode(self.edXmmsInfoFormat.text())
            else:
                pattern = ''
            self.cfg.setOption('misc', 'xmms_pattern', pattern)
        finally:
            qApp.restoreOverrideCursor()

    def xiFormatChange(self, pattern):
        trackInfo = jt_xmmsinfo.getTrackInfo(unicode(pattern))
        if trackInfo is not None:
            self.lbXmmsEx.setText(textile.textile(trackInfo))
        else:
            self.lbXmmsEx.setText(QString.null)

    def __tr(self, s, c=None):
        return qApp.translate('OptionsDialogImpl', s, c)
