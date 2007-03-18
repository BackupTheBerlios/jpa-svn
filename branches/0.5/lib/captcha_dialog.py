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

"""Additional authentication measure, used by Google. An image with text."""

__revision__ = '$Id$'

import gtk

from appwindow import EditDialog

class CaptchaDialog(EditDialog):

    def __init__(self, parent, imagePath):
        EditDialog.__init__(self, 'dlgCaptcha', parent)
        self.imagePath = imagePath
        self.imgCaptcha = self.wTree.get_widget('imgCaptcha')
        self.edAuthCode = self.wTree.get_widget('edAuthCode')
        self._initGui()

    def _initGui(self):
        pass

    def run(self):
        ret = self.window.run()
        result = None
        if ret == gtk.RESPONSE_OK:
            result = self.edAuthCode.get_text().decode('utf-8')
        self.window.destroy()
        return result
