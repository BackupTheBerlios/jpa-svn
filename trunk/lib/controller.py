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

"""GUI controller/signal dispatcher"""

__revision__ = '$Id$'

import gtk
import gtk.glade

import license_dialog, entry_dialog, categories_dialog, prefs_dialog, \
    category_dialog

class Controller:
    
    def showLicense(self):
        dialog = license_dialog.LicenseDialog()
        dialog.show()
    
    def newEntry(self):
        dialog = entry_dialog.EntryDialog()
        dialog.show()
    
    def editEntry(self, entry):
        dialog = entry_dialog.EntryDialog(entry)
        dialog.show()

    def showCategories(self):
        dialog = categories_dialog.CategoriesDialog(self)
        dialog.show()
    
    def showPreferences(self):
        dialog = prefs_dialog.PreferencesDialog()
        dialog.show()
    
    def editCategory(self, category):
        dialog = category_dialog.CategoryDialog(category)
        dialog.show()