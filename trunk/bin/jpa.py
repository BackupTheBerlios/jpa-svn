#! /usr/bin/env python
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

"""Main program file, used to initialize stuff, import global modules and set
standard paths."""

__revision__ = '$Id$'

class JPAApplication:
    """Main application class (bit dummy docstring)."""

    def __init__(self):
        self.gladeFile = 'jpa2.glade'


if __name__ == '__main__':
    import sys
    import pygtk
    pygtk.require('2.0')
    import gtk
    import gettext
    _ = gettext.gettext
    gtk.threads_init()
    gtk.threads_enter()
    app = JPAApplication()
    gtk.main()
    gtk.threads_leave()