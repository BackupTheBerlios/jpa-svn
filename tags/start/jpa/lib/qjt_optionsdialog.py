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
import qjt_repleditdialog
from jt_const import TRUE_VALUES
import textile

def editOptions(parent, config):
    dlg = OptionsDialog(config, parent=parent)
    if (dlg.exec_loop() == 1):
        dlg.saveConfig()


class OptionsDialog(OptionsDialogImpl):

    def __init__(self, config, parent=None, name=None, modal=0, fl=0):
        OptionsDialogImpl.__init__(self, parent, name, modal, fl)
        self.curProfile = None
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.cfg = config
            profiles = config.profiles.keys()
            if len(profiles) > 0:
                profiles.sort()
                for profile in profiles:
                    self.cbxProfile.insertItem(QString(profile))
                self.__loadProfile(self.cfg.getCurrentProfile())
            else:
                self.edJoggerJID.setText(config.getJoggerAddress())
                self.edJabberServer.setText(config.getJabberServer())
                self.edJID.setText(config.getJabberUser())
                self.edPasswd.setText(config.getJabberPasswd())
            pattern = config.getData('misc', 'xmms_pattern',
                'p. (NP: %s -- _%s_)')
            self.edXmmsInfoFormat.setText(pattern)
            trackInfo = jt_xmmsinfo.getTrackInfo(pattern)
            if trackInfo is not None:
                self.lbXmmsEx.setText(textile.textile(trackInfo))
            else:
                self.lbXmmsEx.setText(QString.null)
        finally:
            qApp.restoreOverrideCursor()

    def __loadProfile(self, name):
        if self.curProfile != name:
            self.curProfile = name
            profile = self.cfg.profiles[name]
            try:
                self.ckbDefault.setChecked(profile['default'] in TRUE_VALUES)
            except KeyError:
                # old configuration, just ignore
                self.ckbDefault.setChecked(False)
            for i in range(0,self.cbxProfile.count()):
                if unicode(self.cbxProfile.text(i))==name:
                    self.cbxProfile.setCurrentItem(i)
                    found = True
            self.edJoggerJID.setText(profile['jogger address'])
            self.edJabberServer.setText(profile['jabber server'])
            self.edJID.setText(profile['jabber username'])
            self.edPasswd.setText(profile['jabber password'])
            self.cbxPort.setCurrentText(unicode(profile['jabber port']))
            self.ckbUseSSL.setChecked(profile['use ssl'] in TRUE_VALUES)
            try:
                self.setReplacements(profile['replacements'])
            except KeyError:
                # ignore old configuration
                pass

    def saveConfig(self):
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            profileName = self.cbxProfile.currentText()
            if profileName != QString.null:
                profileName = unicode(profileName)
                profile = jt_cfg.EMPTY_PROFILE.copy()
                profile['name'] = profileName
                profile['default'] = self.ckbDefault.isChecked()
                profile['jogger address'] = unicode(self.edJoggerJID.text())
                profile['jabber server'] = unicode(self.edJabberServer.text())
                profile['jabber username'] = unicode(self.edJID.text())
                profile['jabber password'] = unicode(self.edPasswd.text())
                profile['replacements'] = self.getReplacements()
                try:
                    profile['jabber port'] = \
                        int(unicode(self.cbxPort.currentText()))
                except ValueError:
                    # stick to default if not numeric value
                    profile['jabber port'] = '<default>'
                profile['use ssl'] = self.ckbUseSSL.isChecked()
                self.cfg.writeProfile(profile)
                self.cfg.setCurrentProfile(profile['name'])
            else:
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

    def chgProfile(self, profileName):
        self.__loadProfile(unicode(profileName))

    def __tr(self, s, c=None):
        return qApp.translate('OptionsDialogImpl', s, c)

    def newReplacement(self):
        ret = qjt_repleditdialog.editReplacement(('', ''), self)
        if ret is None:
            return
        added = QListViewItem(self.lvReplacer, ret[0], ret[1])
        self.lvReplacer.insertItem(added)
        self.lvReplacer.setSelected(added, 1)

    def editReplacement(self):
        item = self.lvReplacer.currentItem()
        ret = qjt_repleditdialog.editReplacement((item.text(0), item.text(1)), self)
        if ret is None:
            return
        self.lvReplacer.currentItem().setText(0, ret[0])
        self.lvReplacer.currentItem().setText(1, ret[1])
        self.lvReplacer.sort()

    def delReplacement(self):
        toDel = self.lvReplacer.currentItem()
        self.lvReplacer.takeItem(toDel)
        del toDel

    def setReplacements(self, replacementsStr):
        self.clearReplacements()
        rDict = eval(replacementsStr)
        for regex, replacement in rDict.iteritems():
            added = QListViewItem(self.lvReplacer, regex, replacement)
            self.lvReplacer.insertItem(added)

    def getReplacements(self):
        repl = dict()
        current = self.lvReplacer.firstChild()
        while current:
            repl[unicode(current.text(0))] = unicode(current.text(1))
            current = current.nextSibling()
        return str(repl)

    def clearReplacements(self):
        while self.lvReplacer.childCount() > 0:
            self.lvReplacer.setSelected(self.lvReplacer.firstChild(), 1)
            toDel=self.lvReplacer.currentItem()
            self.lvReplacer.takeItem(toDel)
            del toDel

