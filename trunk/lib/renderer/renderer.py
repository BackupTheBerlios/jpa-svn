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

"""Convenience functions for rendering HTML from simplified markup"""

__revision__ = '$Id$'

PAGE_TEMPLATE = """ \
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>%s</title>
</head>
<body>
%s
</body>
</html>"""

def renderPage(title, text, renderer):
    return PAGE_TEMPLATE % (title, renderBody(text, renderer))

def renderBody(text, renderer):
    if renderer.lower() in ('plain', 'html'):
        body = text
    elif renderer == 'textile':
        import textile
        body = textile.textile(text, input_encoding='utf-8',
            output_encoding='utf-8')
    elif renderer.lower() == 'rest':
        from docutils.core import publish_parts
        body = publish_parts(text, writer_name='html')['fragment']
    elif renderer == 'markdown':
        import markdown
        body = markdown.markdown(text)
    return body.strip()
