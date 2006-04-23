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

import os
import webbrowser

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
    return resp == gtk.RESPONSE_YES

def error(text, parent=None):
    """
    Error message dialog.
    """
    msg = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
        gtk.BUTTONS_OK, text)
    try:
        msg.run()
    finally:
        msg.destroy()

def warning(text, parent=None):
    """
    Warning message dialog.
    """
    msg = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,
        gtk.BUTTONS_OK, text)
    try:
        msg.run()
    finally:
        msg.destroy()

def ellipsize(text, maxLength=30):
    """
    Return text shortened to maxLength - 3 characters with added
    ellipsis ('...').
    """
    if len(text) <= maxLength:
        return text
    return text[:maxLength - 3] + '...'

def openURL(url, system, browserCmd=None):
    if system == 'system':
        browser = webbrowser.get()
        browser.open(url, 1)
        return
    elif system == 'kde':
        command = 'kfmclient exec'
    elif system == 'gnome':
        command = 'gnome-open'
    else:
        command = browserCmd
    if os.name != 'nt':
        url = url.replace('"', '\\"') # escape " for shell happiness
    command = command + ' "' + url + '"'
    try: #FIXME: dirty hack
        os.system(command)
    except:
        pass
