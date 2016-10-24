from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler
from languageparser import parse_lang
from acceptparser import parse_accept


class request_handler(BaseHTTPRequestHandler):
    mime_type = ""
    html_version = True
    send_image = False
    send_reply = False

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.path = '/'

    def _check_accept_header(self, accept_dict):
        if accept_dict[0]['accept'] == 'text/plain':
            self.html_version = False

    def _map_response(self, end, mime_type, img_flag):
        if self.path.endswith(end):
            self.mime_type = mime_type
            self.send_image = img_flag

    def _send_reply_or_image(self, img_flag):
        f = open(curdir + sep + self.path, "rb") if img_flag else open(curdir + sep + self.path)
        data = f.read()
        self.send_response(200)
        self.send_header('Content-length', len(data))
        self.send_header('Content-type', self.mime_type)
        self.end_headers()
        self.wfile.write(data)
        f.close()

    def _process_path_request(self, accept_lang):
        if (self.path == '/' or self.path == '/index.html') and self.html_version and not accept_lang:
            self.path = 'index_en.html'
        if (self.path == '/' or self.path == '/index.html') and self.html_version:
            self.path = 'index_pl.html' if parse_lang(accept_lang)[0]['lang'] == 'pl' else 'index_en.html'
        elif not self.html_version:
            self.path = 'index_plain_pl.txt' if parse_lang(accept_lang)[0]['lang'] == 'pl' else 'index_plain_en.txt'

    def do_GET(self):

        accept_lang = self.headers.get('Accept-language')
        accept = self.headers.get("Accept")

        try:
            if accept:
                self._check_accept_header(parse_accept(accept))
            self._check_accept_header(parse_accept(accept))
            self._process_path_request(accept_lang)
            self._map_response(".txt", "text/plain", False)
            self._map_response(".html", "text/html", False)
            self._map_response(".js", "application/javascript", False)
            self._map_response(".css", "text/css", False)
            self._map_response(".jpg", "image/jpg", True)
            self._map_response(".png", "image/png", True)
            self._map_response(".gif", "image/gif", True)
            self._map_response(".svg", "image/svg+xml", True)
            self._map_response(".ico", "image/x-icon", True)
            self._send_reply_or_image(self.send_image)
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
