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

"""Display HTML source of entry"""

__revision__ = '$Id$'

import gtk, pango
import gtk.glade

import renderer
from appwindow import JPAWindow

class HtmlViewDialog(JPAWindow):
    
    def __init__(self, parent, entry):
        JPAWindow.__init__(self, 'frmHtmlView')
        self.entry = entry
        if parent:
            self.window.set_transient_for(parent.window)
        self.edTitle = self.wTree.get_widget('edTitle')
        self.txBody = self.wTree.get_widget('txBody')
    
    def show(self):
        editorFontName = self.cfg.getOption('fonts', 'editor', 'Monospace 10')
        self.txBody.modify_font(pango.FontDescription(editorFontName))
        title = self.entry.title.encode('utf-8')
        self.window.set_title(_('Viewing entry: "%s"') % title)
        self.edTitle.set_text(title)
        body = self.entry.body.encode('utf-8')
        bodyType = self.entry.bodyType.encode('utf-8')
        body = renderer.renderBody(body, bodyType)
        bf = self.txBody.get_buffer()
        bf.set_text(body)
    
    ### signal handlers ###
    def on_btnClose_clicked(self, *args):
        self.window.destroy()
