# -*- coding: ISO8859-2 -*-

# Asynchronous HTTP/1.0 Client
# Based on example from book "Guide To Python Standard Library"
# by Fredrik Lundh (http://www.effbot.org/)
# This file is part of JPA
# Copyright: (C) 2004 Jarek Zgoda <jzgoda@gazeta.pl>
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

import StringIO
import socket, asyncore
import mimetools, urlparse
import traceback

def doRequest(uri, consumer):
    scheme, host, path, params, query, fragment = urlparse.urlparse(uri)
    if scheme != 'http':
        raise IOError, 'Only HTTP protocol is supported'
    try:
        host, port = host.split(':', 1)
        port = int(port)
    except (TypeError, ValueError):
        port = 80
    if not path:
        path = '/'
    if params:
        path = '%s;%s' % (path, params)
    if query:
        path = '%s?%s' % (path, query)
    return AsyncHttpClient(host, port, path, consumer)


class CloseConnection(Exception):
    pass


class AsyncHttpClient(asyncore.dispatcher_with_send):
    
    def __init__(self, host, port, path, consumer):
        asyncore.dispatcher_with_send.__init__(self)
        self.host = host
        self.port = port
        self.path = path
        self.consumer = consumer
        self.status = None
        self.header = None
        self.bytesIn = 0
        self.bytesOut = 0
        self.data = ''
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def handle_connect(self):
        request = 'GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' % \
            (self.path, self.host)
        self.send(request)
        self.bytesOut = self.bytesOut + len(request)

    def handle_expt(self):
        self.close()
        self.consumer.httpFailed(self)

    def handle_error(self):
        traceback.print_exc()
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        self.bytesIn = self.bytesIn + len(data)
        if not self.header:
            self.data = self.data + data
            header = self.data.split('\r\n\r\n', 1)
            if len(header) <= 1:
                return
            header, data = header
            fp = StringIO.StringIO(header)
            self.status = fp.readline().split(' ', 2)
            self.header = mimetools.Message(fp)
            self.data = ''
            try:
                self.consumer.httpHeader(self)
            except CloseConnection:
                self.close()
                return
            if not self.connected:
                return
        if data:
            self.consumer.feed(data)

    def handle_close(self):
        self.consumer.close()
        self.close()


class FileConsumer:
    
    def __init__(self, fileName):
        self.fileName = fileName

    def httpHeader(self, client):
        if client.status[1] != '200':
            client.close()
            raise CloseConnection
        self.host = client.host
        self.fp = None

    def httpFailed(self, client):
        pass

    def feed(self, data):
        if self.fp is None:
            self.fp = open(self.fileName, 'wb')
        self.fp.write(data)

    def close(self):
        if self.fp is not None:
            self.fp.close()
        self.fp = None

