# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Application signals"""

__revision__ = '$Id'

# entry-related signals
entry_posted = object()
entry_deleted = object()

# comment-related signals
comment_deleted = object()

# miscellaneous signals
post_list_retrieving_finished = object()
