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

import unittest

import re
from jt_tokenizer import Tokenizer

class TokenizerTest(unittest.TestCase):

    def setUp(self):
        self.unicodeInput = u'p. Zażółć _gęślą_ *jaźń* tak, ' + \
            u'jak to jest opisane "tutaj":http://o2.pl/.'
        self.unicodeTokens = (u'Zażółć', u'gęślą', u'jaźń', u'tak', u'jak', 
            u'to', u'jest', u'opisane', u'tutaj')
        self.stringInput = 'p. Zażółć _gęślą_ *jaźń* tak, ' + \
            'jak to jest opisane "tutaj":http://o2.pl/.'
        self.stringTokens = ('Zażółć', 'gęślą', 'jaźń', 'tak', 'jak', 
            'to', 'jest', 'opisane', 'tutaj')
        self.tokenizer = Tokenizer()
    
    def testSetFlagsSuccess(self):
        self.tokenizer.setInput(self.unicodeInput)
        self.failUnless(self.tokenizer.flags == re.UNICODE)

    def testGetTokensUnicodeSuccess(self):
        self.tokenizer.setInput(self.unicodeInput)
        tokens = self.tokenizer.getTokens()
        i = 0
        for t in self.unicodeTokens:
            self.failUnless(tokens[i] == t, u'%s <> %s' % (tokens[i], t))
            i = i + 1
    
    def testGetTokensUnicodeFailure(self):
        self.tokenizer.setInput(self.unicodeInput)
        tokens = self.tokenizer.getTokens()
        badTokens = self.unicodeInput.split()
        self.failIf(len(tokens) == len(badTokens))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
