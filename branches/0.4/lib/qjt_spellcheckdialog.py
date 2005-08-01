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

import locale
import shlex, string, StringIO

from qt import *

from spellcheckdialog_impl import SpellCheckDialogImpl
import jt_spellcheck

def checkSpelling(text, parent):
    if jt_spellcheck.getSpellChecker() is None:
        # no spell checker available
        return text
    dlg = SpellCheckDialog(text, parent=parent)
    if dlg.exec_loop() == 1:
        return unicode(dlg.tbText.text())
    else:
        return text

class SpellCheckDialog(SpellCheckDialogImpl):

    def __init__(self, text, parent=None, name=None, modal=0, fl=0):
        SpellCheckDialogImpl.__init__(self, parent, name, modal, fl)
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.tbText.setText(text)
            self.speller = jt_spellcheck.getSpellChecker()
            langs = self.speller.getLangs()
            self.cbxLang.clear()
            for lang in langs:
                self.cbxLang.insertItem(lang)
            self.lang, self.enc = locale.getlocale()
            if self.lang in langs:
                self.cbxLang.setCurrentText(self.lang)
            else:
                # current locale-specified language is not available, 
                # use default (en_US)
                self.cbxLang.setCurrentText('en_US')
            self.ignoredWords = []
            self.fp = None
        finally:
            qApp.restoreOverrideCursor()

    def startClick(self):
        qApp.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.src = unicode(self.tbText.text()).encode(self.enc)
            self.speller.setLang(unicode(self.cbxLang.currentText()))
            self.fp = StringIO.StringIO(self.src)
            self.tokenizer = shlex.shlex(self.fp)
            self.tokenizer.whitespace += ',./()-;:"*_~<>{}[]+=|&?#@$%!' \
                + string.digits
            self.tokenizer.wordchars = string.letters
        finally:
            qApp.restoreOverrideCursor()
        self.tbText.setFocus()
        self.curPos = self.curPara = 0
        self.curWord = self.tokenizer.get_token()
        self.tbText.setCursorPosition(self.curPara, self.curPos)
        if self.curWord:
            (found, self.curPara, self.curPos) = \
                self.tbText.find(QString(self.curWord), True, True)
            if not self.speller.checkWord(self.curWord):
                suggestions = self.speller.suggest(self.curWord)
                self.lbxSuggest.clear()
                for s in suggestions:
                    self.lbxSuggest.insertItem(s)
                if len(suggestions) > 0:
                    self.lbxSuggest.setSelected(0, True)

    def replaceClick(self):
        self.replace()

    def skipClick(self):
        self.next()

    def ignoreClick(self):
        if not self.curWord in self.ignoredWords:
            self.ignoredWords.append(self.curWord)
        self.next()

    def closeEvent(self, e):
        # be polite to your file streams
        if self.fp:
            self.fp.close()
        e.accept()

    def __tr(self, s, c=None):
        return qApp.translate('SpellCheckDialogImpl', s, c)

    def next(self):
        self.lbxSuggest.clear()
        self.curWord = self.tokenizer.get_token()
        while self.curWord:
            (found, self.curPara, self.curPos) = \
                self.tbText.find(QString(self.curWord), True, True)
            if (self.speller.checkWord(self.curWord) or 
                (self.curWord in self.ignoredWords)):
                self.curWord = self.tokenizer.get_token()
            else:
                suggestions = self.speller.suggest(self.curWord)
                for s in suggestions:
                    self.lbxSuggest.insertItem(s)
                if len(suggestions) > 0:
                    self.lbxSuggest.setSelected(0, True)
                break
        else:
            QMessageBox.information(self, self.__tr('Information'),
                self.__tr('Spell checking complete.'), QMessageBox.Ok)

    def replace(self):
        self.tbText.removeSelectedText()
        self.tbText.insert(self.lbxSuggest.currentText())
        self.src = unicode(self.tbText.text())
        self.next()
