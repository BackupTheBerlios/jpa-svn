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
    qjt_msgsend, jt_msgsend, jt_evtqueue
from mainform_impl import MainFormImpl
from jt_version import VERSION
from jt_const import MSGTEMPLATE


class MainForm(MainFormImpl):

    def __init__(self, parent=None, name=None, fl=0):
        MainFormImpl.__init__(self, parent, name, fl)
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.events = jt_evtqueue.EventQueue(self)
            self.cfg = jt_cfg.AppConfig()
            self.fileName = op.join(op.expanduser('~'),
                'jpadata', '%s.dat' % time.strftime('%Y-%m'))
            geom = self.cfg.getWindowGeometry('mainform')
            self.setGeometry(geom[0], geom[1], geom[2], geom[3])
            self.data = jt_storage2.Storage(self.fileName)
            self.setCaption('JPA v. %s - %s' % (VERSION, self.fileName))
            #self.sender = jt_msgsend.Sender(self)
            self.sender = qjt_msgsend.Sender(self)
            self.__loadData()
        finally:
            qApp.restoreOverrideCursor()

    def __loadData(self):
        self.lbCreated.setText(QString.null)
        self.lbSent.setText(QString.null)
        self.lbTitle.setText(QString.null)
        self.tbMessage.setText(QString.null)
        self.lbxMessages.clear()
        lst = self.data.getEntries()
        if lst:
            self.lbxMessages.insertStrList(lst)
            self.lbxMessages.sort(False)
            self.lbxMessages.setCurrentItem(0)
            self.lbxMessages.setSelected(0, True)

    def fileNew(self):
        if self.data:
            startDir = op.dirname(self.fileName)
        else:
            startDir = self.cfg.getDataDir(op.join(op.expanduser('~/'),
                'jpadata'))
        fileFilter = self.__tr('Data files (*.dat);;All files (*.*)')
        fileName = QFileDialog.getSaveFileName(startDir, fileFilter, self,
            None, self.__tr('Save file'), None, True)
        if fileName != QString.null:
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                self.data.close()
                self.fileName = str(fileName)
                self.data = jt_storage2.Storage(self.fileName)
                self.setCaption('JPA v. %s - %s' % (VERSION, self.fileName))
                self.__loadData()
            finally:
                qApp.restoreOverrideCursor()

    def fileOpen(self):
        if self.data:
            startDir = op.dirname(self.fileName)
        else:
            startDir = self.cfg.getDataDir(op.join(op.expanduser('~/'),
                'jpadata'))
        fileFilter = self.__tr('Data files (*.dat);;All files (*.*)')
        fileName = QFileDialog.getOpenFileName(startDir, fileFilter, self,
            None, self.__tr('Open file'), None, True)
        if fileName != QString.null:
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                self.data.close()
                self.fileName = str(fileName)
                self.data = jt_storage2.Storage(self.fileName)
                self.setCaption('JPA v. %s - %s' % (VERSION, self.fileName))
                self.__loadData()
            finally:
                qApp.restoreOverrideCursor()

    def msgNew(self):
        msg = qjt_msgeditdialog.msgNew(self, self.cfg)
        if msg is not None:
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                msgId = msg['msgid']
                self.data.writeMessage(msg)
                self.data.flush()
                self.__loadData()
            finally:
                qApp.restoreOverrideCursor()

    def msgEdit(self):
        msg = self.data.getMessage(str(self.lbxMessages.currentText()))
        message = qjt_msgeditdialog.msgEdit(self, msg)
        if message is not None:
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                self.data.writeMessage(message)
                self.lbTitle.setText(message['title'])
                msgText = MSGTEMPLATE % \
                    (message['title'], textile.textile(message['body']))
                self.tbMessage.setText(msgText)
            finally:
                qApp.restoreOverrideCursor()

    def msgDelete(self):
        if QMessageBox.question(self, self.__tr('Confirm'),
            self.__tr('Are you sure you want to delete this message?'),
            QMessageBox.Yes,
            QMessageBox.No|QMessageBox.Default) == QMessageBox.Yes:
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                msgId = str(self.lbxMessages.currentText())
                self.data.deleteMessage(msgId)
                self.data.flush()
                self.__loadData()
            finally:
                qApp.restoreOverrideCursor()

    def msgHistory(self):
        msg = self.data.getMessage(str(self.lbxMessages.currentText()))
        if msg is not None:
            qjt_msghistorydialog.showMessageHistory(self, msg)

    def msgSave(self):
        msgId = str(self.lbxMessages.currentText())
        startDir = op.join(op.expanduser('~/'), '%s.html' % msgId)
        fileFilter = self.__tr('HTML documents (*.html);;All files (*.*)')
        fileName = QFileDialog.getSaveFileName(startDir, fileFilter, self,
            None, self.__tr('Save file'), None, True)
        if fileName != QString.null:
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                msg = self.data.getMessage(msgId)
                msgText = MSGTEMPLATE % \
                    (msg['title'], textile.textile(msg['body']))
                f = open(unicode(fileName), 'w')
                try:
                    f.write(msgText.encode(jt_const.enc))
                finally:
                    f.close()
            finally:
                qApp.restoreOverrideCursor()

    def msgSend(self):
        toSend = 1
        msg = self.data.getMessage(str(self.lbxMessages.currentText()))
        msg['body'] = self.cfg.useReplacements(msg['body'])
        if msg.has_key('sent') and (len(msg['sent']) > 0):
            toSend = (QMessageBox.question(self, self.__tr('Confirm'),
                self.__tr('This message already has been published.\n'
                    'Do you want to send it again?'),
                QMessageBox.Yes, QMessageBox.No|QMessageBox.Default,
                QMessageBox.NoButton) == QMessageBox.Yes)
        if toSend:
            resetPasswd = 0
            if self.cfg.getJabberPasswd() == '':
                resetPasswd = 1
                passwd = QInputDialog.getText(self.__tr('Password'),
                    self.__tr('Enter the password'), QLineEdit.Password)
                if not passwd:
                    raise IOError, self.__tr('No password provided')
                self.cfg.setJabberPasswd(unicode(passwd))
            try:
                try:
                    self.sender.send(msg)
                finally:
                    if resetPasswd:
                        self.cfg.setJabberPasswd('')
            except IOError, e:
                QMessageBox.critical(self, self.__tr('Error'),
                    unicode(e), QMessageBox.Ok, QMessageBox.NoButton,
                    QMessageBox.NoButton)

    def msgItemSelected(self):
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            msg = self.data.getMessage(str(self.lbxMessages.currentText()))
            self.lbCreated.setText(time.strftime('%Y-%m-%d %H:%M',
                msg['created']))
            if msg.has_key('sent') and (len(msg['sent']) > 0):
                self.lbSent.setText(time.strftime('%Y-%m-%d %H:%M',
                    msg['sent'][-1]))
            else:
                self.lbSent.setText(QString.null)
            self.lbTitle.setText(msg['title'])
            if msg['content-type'] == 'textile':
                body = textile.textile(msg['body'])
            else:
                body = msg['body']
            msgText = MSGTEMPLATE % (msg['title'], body)
            self.tbMessage.setText(msgText)
        finally:
            qApp.restoreOverrideCursor()

    def toolsImport(self):
        qjt_msgimport.importMessages(self, self.cfg)

    def toolsExport(self):
        startDir = op.expanduser('~/')
        fileFilter = self.__tr('Text files (*.txt);;All files (*.*)')
        fileName = QFileDialog.getSaveFileName(startDir, fileFilter, self,
            None, self.__tr('Save file'), None, True)
        if fileName != QString.null:
            qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                self.data.export(unicode(fileName), jt_const.enc)
            finally:
                qApp.restoreOverrideCursor()

    def toolsOptions(self):
        qjt_optionsdialog.editOptions(self, self.cfg)

    def helpAbout(self):
        qjt_aboutdialog.showAboutDialog(self)

    def helpAboutQt(self):
        QMessageBox.aboutQt(self, 'Jogger Publishing Assistant')

    ### events ###

    def closeEvent(self, e):
        if len(self.sender.threads) > 0:
            # I really don't know how to do things...
            e.ignore()
        g = self.geometry()
        self.cfg.setWindowGeometry('mainform',
            (g.left(), g.top(), g.width(), g.height()))
        self.cfg.saveConfig()
        self.data.close()
        e.accept()

    def customEvent(self, e):
        t = e.type()
        if t == 10000:
            # sender thread ended work
            self.statusBar().message(self.__tr('Finished sending message'))
            msg = e.data()
            if msg is None:
                msg = self.__tr('Message has been sent.')
            QMessageBox.information(self, self.__tr('Information'),
                unicode(msg), QMessageBox.Ok)
            self.msgItemSelected()
        elif t == 10001:
            # sender thread started work
            self.statusBar().message(self.__tr('Sending message...'))
            
    ### custom methods ###
    
    def notify(self, message):
        if message == 'item added':
            e = self.events.get_nowait()
            t = e.type()
            if t == 10000:
                # sender thread ended work
                self.statusBar().message(self.__tr('Finished sending message'))
                msg = e.data()
                if msg is None:
                    msg = self.__tr('Message has been sent.')
                QMessageBox.information(self, self.__tr('Information'),
                    unicode(msg, 'UTF-8', 'replace'), QMessageBox.Ok)
                self.msgItemSelected()
            elif t == 10001:
                # sender thread started work
                self.statusBar().message(self.__tr('Sending message...'))

    def __tr(self, s, c=None):
        return qApp.translate("MainFormImpl", s, c)
