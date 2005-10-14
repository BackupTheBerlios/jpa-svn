# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003 - 2005 Jarek Zgoda <jzgoda@o2.pl>
#
# JPA is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with 
# JPA; if not, write to the Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Definition of generic weblog transport interface."""

__revision__ = '$Id$'

class WeblogTransport:

    def getBlogList(self): raise NotImplementedError

    def postNew(self, entry): raise NotImplementedError

    def postModified(self, entryId, entry): raise NotImplementedError

    def getEntry(self, entryId): raise NotImplementedError

    def deleteEntry(self, entryId): raise NotImplementedError