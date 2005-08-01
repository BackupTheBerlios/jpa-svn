# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003, 2004 Jarek Zgoda <jzgoda@gazeta.pl>
#
# JPA is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JPA; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import os.path as op

class PixmapProviderFactory:

    def getProvider(self):
        if os.getenv('KDEDIR') is not None:
            return KDEPixmapProvider()
        else:
            return NullPixmapProvider()


class PixmapProvider:
    """Base provider class, that defines common functionality for all derived
    UI pixmap providers."""
    
    def __init__(self):
        self.pixmaps = []
        self.imageType = 'xpm' # this needs to be adjusted in derived classes
        self.imageDir = ''
        
    def __getitem__(self, item):
        imgName = '%s.%s' % (item, self.imageType)
        if imgName in self.pixmaps:
            return op.join(self.imageDir, imgName)


class NullPixmapProvider(PixmapProvider):
    """This class effectively delivers nothing. No images, no icons."""

    def __init__(self):
        PixmapProvider.__init__(self)
        
    def __getitem__(self, item):
        return None


class KDEPixmapProvider(PixmapProvider):
    """On systems, where KDE3 is installed, we will use default KDE icon theme.
    Fortunately for us, directory $KDEDIR/share/icons/default.kde is a symlink 
    to directory with current icon theme."""

    def __init__(self):
        PixmapProvider.__init__(self)
        self.imageType = 'png'
        self.imageDir = op.join(os.getenv('KDEDIR'), # KDE is installed
            'share', 'icons', 'default.kde', # default KDE3 icon theme
            '22x22', # small, but not smallest icons
            'actions') # application defined actions
        self.pixmaps = os.listdir(self.imageDir)