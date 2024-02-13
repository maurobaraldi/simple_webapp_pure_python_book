#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class HTTPRequestHandler(BaseHTTPRequestHandler):

        def do_PUT(self):
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)

            self.send_response(204)
            self.end_headers()

            self.wfile.write(b"")


if __name__ == "__main__":
    server = HTTPServer(('', 8080), HTTPRequestHandler)
    server.serve_forever()
