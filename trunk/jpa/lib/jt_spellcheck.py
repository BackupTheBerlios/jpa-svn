# -*- coding: utf-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003, 2004 Jarek Zgoda <jzgoda@gazeta.pl>
#
# JPA is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JPA; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import sys, locale, glob, os, string
import os.path as op

try:
    import aspell
    hasAspell = True
except ImportError:
    hasAspell = False
try:
    import myspell
    hasMyspell = True
except ImportError:
    hasMyspell = False

def getSpellChecker(lang=None):
    """Factory function that returns instance of spell checker. Aspell takes
    precedence over myspell (due to maturity and useful features). If none of
    these spell checkers can be created, None is returned."""
    if hasAspell:
        return AspellChecker(lang)
    elif hasMyspell:
        return MyspellChecker(lang)
    else:
        return None


# as seen in Ned Batchelder's blog
# http://www.nedbatchelder.com/text/pythonic-interfaces.html
def _functionId(obj, nFramesUp):
    """Create a string naming the function n frames up on the stack."""
    fr = sys._getframe(nFramesUp + 1)
    co = fr.f_code
    return '%s.%s' % (obj.__class__, co.co_name)

def abstractMethod(obj=None):
    """Use this instead of 'pass' for the body of abstract methods."""
    raise Exception('Unimplemented abstract method: %s' % _functionId(obj, 1))


# meat starts here
class SpellChecker:
    """All-abstract base spellchecking class. Basic functionality to be
    implemented by descentant classes."""

    def __init__(self, lang):
        abstractMethod(self)

    def checkWord(self, word):
        abstractMethod(self)

    def suggest(self, word):
        abstractMethod(self)

    def addToUserDict(self, word):
        abstractMethod(self)

    def addToSessionDict(self, word):
        abstractMethod(self)

    def getLangs(self):
        abstractMethod(self)

    def setLang(self, lang):
        abstractMethod(self)


class AspellChecker(SpellChecker):
    """Aspell-based spell checker"""

    def __init__(self, lang=None):
        """Create and return instance of AspellChecker. If parameter lang is
        not specified, default dictionary for current locale will be used."""
        self.__s = aspell.new()
        if lang is not None:
            self.__s.setoption('lang', lang)

    def checkWord(self, word):
        return self.__s.check(word)

    def suggest(self, word):
        return self.__s.suggest(word)

    def addToUserDict(self, word):
        self.__s.addtoPersonal(word)
        self.__s.saveAllwords()

    def addToSessionDict(self, word):
        self.__s.addtoSession(word)

    def getLangs(self):
        directory = self.__s.getoption('dict-dir')
        allDicts = glob.glob(op.join(directory, '*.multi'))
        dicts = []
        for d in allDicts:
            if d.find('-') == -1:
                dictName = op.splitext(op.basename(d))[0]
                normName = locale.normalize(dictName).split('.')[0]
                if not normName in dicts:
                    dicts.append(normName)
        dicts.sort()
        print dicts
        return dicts

    def setLang(self, lang):
        self.__s.setoption('lang', lang)


class MyspellChecker(SpellChecker):
    """Myspell-based spell checker"""

    def __init__(self, lang=None):
        """Create and return instance of MyspellChecker. If parameter lang is
        not specified, default dictionary for current locale will be used. In
        case the dictionary is not available, en_US will be used."""
        self.__s = myspell.MySpell()
        if lang is None:
            (lang, enc) = locale.getlocale()
            if lang is None:
                (lang, enc) = locale.getdefaultlocale()
        l = self.__s.list_languages()
        if not lang in l:
            lang = 'en_US'
        self.__s.load_language(lang)
        self.sessionDict = []

    def checkWord(self, word):
        return self.__s.spell(word)

    def suggest(self, word):
        return self.__s.suggest(word)

    def addToUserDict(self, word):
        """Myspell has no such feature, so we just ignore this call..."""
        pass

    def addToSessionDict(self, word):
        if not (word in self.sessionDict):
            self.sessionDict.append(word)

    def getLangs(self):
        return self.__s.list_languages()

    def setLang(self, lang):
        self.__s.load_language(lang)
