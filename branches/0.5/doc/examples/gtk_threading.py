import sys, threading, os, urllib, traceback
import gtk

opener = urllib.FancyURLopener()

# used to work out whether to do gtk.main_quit()
remaining = 0
remaining_lock = threading.Lock()

class DownloadThread(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.cancel = threading.Event()
        self.create_ui()
        threading.Thread.__init__(self, name=url)

    def create_ui(self):
        self.frame = gtk.Frame(None)
        vbox = gtk.VBox(spacing=3)
        vbox.set_border_width(3)
        self.frame.add(vbox)
        label = gtk.Label('downloading %s' % self.url)
        vbox.pack_start(label, expand=False)

        hbox = gtk.HBox(spacing=3)
        vbox.pack_start(hbox)
        self.progress = gtk.ProgressBar()
        hbox.pack_start(self.progress)

        button = gtk.Button('Cancel')
        button.connect('clicked', self.cancel_cb)
        hbox.pack_start(button, expand=False)

        self.frame.show_all()

    def run(self):
        global remaining
        
        try:
            local = os.path.basename(self.url)
            if not local: local = 'index.html'
            opener.retrieve(self.url, local, reporthook=self.download_status)
        except SystemExit:
            pass
        except:
            traceback.print_exc()

        # if we completed the download, now clean things up.
        gtk.threads_enter()

        self.frame.destroy()
        del self.progress, self.frame

        remaining_lock.acquire()
        remaining -= 1
        value = remaining
        remaining_lock.release()

        if value == 0:
            gtk.main_quit()

        gtk.threads_leave()


    def download_status(self, block_count, block_size, file_size):
        # handler that gets called at regular intervals by
        # opener.retrieve().  This is called in the download thread,
        # so if we want to manipulate any gtk objects, then we
        # must acquire the gdk lock.
        
        # was the download canceled?
        if self.cancel.isSet():
            sys.exit()

        # calculate how far through the download we are
        gtk.threads_enter()

        fraction = float(block_count * block_size) / file_size
        fraction = max(min(fraction, 1.0), 0.0)
        self.progress.set_fraction(fraction)

        gtk.threads_leave()

    def cancel_cb(self, button):
        # as this is a signal handler, it will get called in the
        # thread running gtk.main().  We use an event object to
        # signal the download thread that it should exit.
        self.cancel.set()


if len(sys.argv) < 2:
    sys.stderr.write('usage: download.py url ...')
    sys.exit(1)

gtk.threads_init()
gtk.threads_enter()

w = gtk.Window(gtk.WINDOW_TOPLEVEL)
w.set_title('Downloading')

vbox = gtk.VBox(spacing=5)
vbox.set_border_width(5)
w.add(vbox)

remaining_lock.acquire()
for url in sys.argv[1:]:
    thread = DownloadThread(url)
    vbox.pack_start(thread.frame)
    thread.start()
    remaining += 1
remaining_lock.release()

w.show_all()

gtk.main()

gtk.threads_leave()
