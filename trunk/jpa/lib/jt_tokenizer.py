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

import re

class Tokenizer:
    
    def __init__(self, input=None):
        self.flags = None
        #self.pattern = r"[\s(?:\bp.\b)_*\"]"
        self.pattern = r"\Ap\.|\*|_|\"|:http://\S*|\s|[,.;:]"
        self.re = None
        if input is not None:
            self.data = input
            self.setFlags(input)
            self.makeRe()
    
    def setInput(self, input):
        self.data = input
        self.setFlags(input)
        self.makeRe()
    
    def setFlags(self, forData):
        if type(forData) == type(u''):
            self.flags = re.UNICODE
    
    def makeRe(self):
        if self.flags is not None:
            self.re = re.compile(self.pattern, self.flags)
        else:
            self.re = re.compile(self.pattern)
    
    def getTokens(self):
        return [i.strip() for i in self.re.split(self.data) if i.strip()]

