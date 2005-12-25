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

"""Miscellaneous utility functions"""

__revision__ = '$Id$'

import gtk, gtk.gdk

def startWait(window):
    """
    Show nice wait notification cursor.
    window must be a gtk.window descendant or must have gdk.window attribute
    """
    cursor = gtk.gdk.Cursor(gtk.gdk.WATCH)
    window.window.set_cursor(cursor)

def endWait(window):
    """
    Restore default application cursor after wait period.
    window must be a gtk.window descendant or must have gdk.window attribute
    """
    window.window.set_cursor(None)

def question(text, parent=None):
    """
    Dialog with question. Returns true if response was "Yes".
    """
    msg = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_YES_NO, text)
    try:
        resp = msg.run()
    finally:
        msg.destroy()
    return resp == gtk.RESPONSE_OK
