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

class Credentials:

    keys = ('jid', 'hostname', 'port', 'use ssl', 'passwd')
    
    def __init__(self):
        self.data = dict()
    
    def __setitem__(self, key, value):
        if key in self.keys:
            self.data[key] = value
            
    def __getitem__(self, key):
        if key in self.keys:
            # no fskin' exception, please
            return self.data[key]