#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

PORT_NUMBER = 8080


# This class will handles any incoming request from
# the browser
class request_handler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    mime_type = ""
    send_image = False
    send_reply = False

    # Handler for the GET requests
    def do_GET(self):
        def set_response(end, mimetype, img_flag):
            if self.path.endswith(end):
                self.mime_type = mimetype
                self.send_image = img_flag

        if self.path == "/":
            self.path = "/index.html"

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

        try:
            # Check the file extension required and
            # set the right mime type
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


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), request_handler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
