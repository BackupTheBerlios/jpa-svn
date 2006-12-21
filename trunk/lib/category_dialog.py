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

"""Category item editor"""

__revision__ = '$Id$'

import louie
import gtk

import datamodel
from appwindow import EditDialog

class CategoryDialog(EditDialog):
    
    def __init__(self, parent, category=None):
        EditDialog.__init__(self, 'dlgCategory', parent)
        self.category = category
        self.edName = self.wTree.get_widget('edName')
        self.tvDescription = self.wTree.get_widget('tvDescription')
        self.ckbIsActive = self.wTree.get_widget('ckbIsActive')
        self._initGui()
    
    def _initGui(self):
        if self.category:
            name = self.category.name
            description = self.category.description
            active = self.category.isActive
            self.edName.set_text(name)
            bf = gtk.TextBuffer()
            bf.set_text(description)
            self.tvDescription.set_buffer(bf)
            self.ckbIsActive.set_active(active)
            windowTitle = _('Editing category "%s"') % self.category.name
        else:
            windowTitle = _('Editing new category')
        self.window.set_title(windowTitle)
    
    def run(self):
        ret = self.window.run()
        if ret == gtk.RESPONSE_OK:
            name = self.edName.get_text().decode('utf-8')
            bf = self.tvDescription.get_buffer()
            description = bf.get_text(bf.get_start_iter(), 
                bf.get_end_iter()).decode('utf-8')
            active = self.ckbIsActive.get_active()
            if self.category:
                self.category.name = name
                self.category.description = description
                self.category.isActive = active
            else:
                datamodel.Category(
                    name=name,
                    description=description,
                    isActive=active
                )
            louie.send('category-changed')
        self.window.destroy()            

