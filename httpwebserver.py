from BaseHTTPServer import HTTPServer

from requesthandler import request_handler

PORT_NUMBER = 8080

server = HTTPServer(('', PORT_NUMBER), request_handler)

try:
    print 'Webserver running on port ', PORT_NUMBER
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
