# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Various system-related utilities"""

__revision__ = '$Id$'

import os
import webbrowser

def open_url(url, system='system', command=None):
    if system == 'system':
        browser = webbrowser.get()
        browser.open(url, 1)
        return
    elif system == 'kde':
        cmd = 'kfmclient exec'
    elif system == 'gnome':
        cmd = 'gnome-open'
    else:
        cmd = command
    if os.name != 'nt':
        url = url.replace('"', '\\"')
    cmd = '%s "%s"' % (cmd, url)
    # FIXME: this is a dirty hack
    try:
        os.system(cmd)
    except:
        pass