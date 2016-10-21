from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep


class request_handler(BaseHTTPRequestHandler):
    mime_type = ""
    send_image = False
    send_reply = False

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.path = '/'

    def do_GET(self):

        def set_response(end, mimetype, img_flag):
            if self.path.endswith(end):
                self.mime_type = mimetype
                self.send_image = img_flag

        def send_reply_or_image(img_flag):
            if img_flag:
                f = open(curdir + sep + self.path, "rb")
            else:
                f = open(curdir + sep + self.path)
            data = f.read()
            self.send_response(200)
            self.send_header('Content-length', len(data))
            self.send_header('Content-type', self.mime_type)
            self.end_headers()
            self.wfile.write(data)
            f.close()

        if self.path == "/":
            self.path = "/index.html"

        try:
            set_response(".html", "text/html", False)
            set_response(".js", "application/javascript", False)
            set_response(".css", "text/css", False)
            set_response(".jpg", "image/jpg", True)
            set_response(".png", "image/png", True)
            set_response(".gif", "image/gif", True)
            set_response(".svg", "image/svg", True)
            set_response(".ico", "image/x-icon", True)
            send_reply_or_image(self.send_image)
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
