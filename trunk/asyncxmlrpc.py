# This code has been published 2006-05-18 by A.M. Kuchling on PyGTK
# mailing list. Cann't find its

import pygtk
pygtk.require('2.0')
import gtk, gobject

import xmlrpclib

class XMLRPCDeferred:
    """
    Object representing the delayed result of an XML-RPC
    request.

    .is_ready: bool
      True when the result is received; False before then.
    .value : any
      Once is_ready=True, this attribute contains the result of the
      request.  If this value is an instance of the xmlrpclib.Fault
      class, then some exception occurred during the request's
      processing.  
    """
    
    def __init__ (self, transport, http):
        self.transport = transport
        self.http = http
        self.value = None
        self.is_ready = False
        sock = self.http._conn.sock
        self.src_id = gobject.io_add_watch(sock,
            gobject.IO_IN | gobject.IO_HUP, self.handle_io)

    def handle_io (self, source, condition):
        # Triggered when there's input available on the socket.
        # The assumption is that all the input will be available
        # relatively quickly.
        self.read()
        # Returning false prevents this callback from being triggered
        # again.  We also remove the monitoring of this file
        # descriptor.
        gobject.source_remove(self.src_id)
        return False
    
    def read (self):
        errcode, errmsg, headers = self.http.getreply()
        if errcode != 200:
            raise xmlrpclib.ProtocolError(
                self.http.host,
                errcode, errmsg,
                headers,
            )
        try:
            result = xmlrpclib.Transport._parse_response(self.transport,
                self.http.getfile(), None)
        except xmlrpclib.Fault, exc:
            result = exc
        self.value = result
        self.is_ready = True

    def __len__ (self):
        # XXX egregious hack!!!
        # The code in xmlrpclib.ServerProxy calls len() on the object
        # returned by the transport, and if it's of length 1 returns
        # the contained object.  Therefore, this __len__ method
        # returns a completely fake length of 2.
        return 2 

        
class GtkTransport (xmlrpclib.Transport):

    def request(self, host, handler, request_body, verbose=0):
        # issue XML-RPC request
        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)
        self.verbose = verbose
        return XMLRPCDeferred(self, h)


class HelloWorld2:

    # Our new improved callback.  The data passed to this method
    # is printed to stdout.
    def callback(self, widget, data):
        print "Hello again - %s was pressed" % data

        # Fire off an XML-RPC request for a model load; this
        # is pretty time-consuming.
        t = GtkTransport()

        s = xmlrpclib.ServerProxy('http://xmlrpc.example.com', t)
        result = s.long_slow_method()

        # You get back an XMLRPCDeferred object; is_ready will be True
        # once the results are back.
        import time
        while not result.is_ready:
            print 'waiting', time.time()
            gtk.main_iteration(block=False)
            time.sleep(1)

        # result.value now holds the result.
        print 'result:', result.value
        
    # another callback
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # This is a new call, which just sets the title of our
        # new window to "Hello Buttons!"
        self.window.set_title("Hello Buttons!")

        # Here we just set a handler for delete_event that immediately
        # exits GTK.
        self.window.connect("delete_event", self.delete_event)

        # Sets the border width of the window.
        self.window.set_border_width(10)

        # We create a box to pack widgets into.  This is described in detail
        # in the "packing" section. The box is not really visible, it
        # is just used as a tool to arrange widgets.
        self.box1 = gtk.HBox(False, 0)

        # Put the box into the main window.
        self.window.add(self.box1)

        # Creates a new button with the label "Button 1".
        self.button1 = gtk.Button("Button 1")

        # Now when the button is clicked, we call the "callback" method
        # with a pointer to "button 1" as its argument
        self.button1.connect("clicked", self.callback, "button 1")

        # Instead of add(), we pack this button into the invisible
        # box, which has been packed into the window.
        self.box1.pack_start(self.button1, True, True, 0)

        # Always remember this step, this tells GTK that our preparation for
        # this button is complete, and it can now be displayed.
        self.button1.show()

        # Do these same steps again to create a second button
        self.button2 = gtk.Button("Button 2")

        # Call the same callback method with a different argument,
        # passing a pointer to "button 2" instead.
        self.button2.connect("clicked", self.callback, "button 2")

        self.box1.pack_start(self.button2, True, True, 0)

        # The order in which we show the buttons is not really important, but I
        # recommend showing the window last, so it all pops up at once.
        self.button2.show()
        self.box1.show()
        self.window.show()


if __name__ == "__main__":
    hello = HelloWorld2()
    gtk.main()



