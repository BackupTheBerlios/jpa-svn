# -*- coding: utf-8 -*-

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

"""Application window's tooltips.

Some tooltips can not be set in glade, so they must be defined elsewhere."""

__revision__ = '$Id$'

import gtk

__FILE_MENU_TIPS = {
    'miFileNew': _('Write new entry'),
    'miFileEdit': _('Open and edit existing entry'), 
}

def setFileMenuTips(menu):
    group = gtk.Tooltips()
    for name, item in menu.items():
        try:
            group.set_tip(item, __FILE_MENU_TIPS[name])
        except KeyError:
            # just ignore non-existing keys
            pass
    return group