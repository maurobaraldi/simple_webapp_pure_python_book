#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_DELETE(self):
        self.send_response(204)
        self.end_headers()
                            
        if __name__ == "__main__":
            server = HTTPServer(('', 8080), HTTPRequestHandler)
            server.serve_forever()
