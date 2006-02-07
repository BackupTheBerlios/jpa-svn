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

from htmlentitydefs import entitydefs
import re

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

def html2xml(html):
    """Convert html latin-1 entities to its numeric equivalents.
    May be usable to sanitize (X)HTML to be passed as part of XML
    document."""
    chunks = re.split('&(\w+);', html)
    for i in range(1, len(chunks), 2):
        if chunks[i] in ['amp', 'lt', 'gt', 'apos', 'quot']:
            chunks[i] = '&' + chunks[i] + ';'
        elif chunks[i] in entitydefs:
            chunks[i] = entitydefs[chunks[i]]
            if len(chunks[i]) == 1:
                chunks[i] = '&#' + str(ord(chunks[i])) + ';'
        else:
            chunks[i] = '?'
    return str(''.join(chunks))

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

def renderBodyAsXML(text, renderer):
    return html2xml(renderBody(text, renderer))
