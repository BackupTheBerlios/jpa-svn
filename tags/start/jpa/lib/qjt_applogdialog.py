# -*- coding: ISO8859-2 -*-

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

from qt import *

from applogdialog_impl import AppLogDialogImpl

class AppLogDialog(AppLogDialogImpl):

    def __init__(self, parent=None, name=None, modal=0, fl=0):
        AppLogDialogImpl.__init__(self, parent, name, modal, fl)
