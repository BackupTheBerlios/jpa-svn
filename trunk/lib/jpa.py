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

"""Main application class module."""

__revision__ = '$Id$'

import os.path as op
import appconst, datamodel, controller, config
from main_window import MainWindow

class JPAApplication:
    
    def __init__(self):
        datamodel.initModel()
        appconst.CFG = config.AppConfig(op.join(appconst.PATHS['user'],
            'jpa.cfg'))
        self.gladeFile = op.join(appconst.PATHS['share'], appconst.GLADE_FILE)
        self.controller = controller.Controller(self.gladeFile)
        self.mainWindow = MainWindow(self.gladeFile, self.controller)