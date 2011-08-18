#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from threading import Thread

try:
    from pyvows import Vows
    pyvows_present = True
except ImportError:
    pyvows_present = False

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

if pyvows_present:
    class RodContext(Vows.Context):
        def __init__(self, parent):
            super(RodContext, self).__init__(parent)
            self.rod_port = 10000
            self.ignore('say', 'configure')

        def configure(self):
            pass

        def say(self, url, method="GET", body=""):
            self._server.record(method, url, body)

        def setup(self):
            self.configure()
            self._server = RodServer(self.rod_port)
            self._server.start()

        def teardown(self):
            self._server.stop()


class RodServer(object):
    def __init__(self, port):
        self.recordings = []
        self.http_server = None
        self.port = port

    def record(self, method, url, body):
        self.recordings.append({
            'method': method,
            'url': url,
            'body': body
        })

    def start(self):
        class HandleRequest(BaseHTTPRequestHandler):
            def do_GET(self):
                found = False
                for recording in self.server.rod.recordings:
                    if self.path.endswith(recording['url']):
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/html')
                        self.end_headers()
                        self.wfile.write(recording['body'])
                        found = True

                if not found:
                    self.send_response(404)
                    self.wfile.write('')

            def log_request(self, *args, **kw):
                pass

            def log_error(self, *args, **kw):
                pass

            def log_message(self, *args, **kw):
                pass

        self.http_server = HTTPServer(('', self.port), HandleRequest)
        self.http_server.rod = self
        def process_request():
            while (True):
                time.sleep(0.2)
                self.http_server.handle_request()

        self.thr = Thread(target=process_request)
        self.thr.daemon = True
        self.thr.start()

    def stop(self):
        if self.http_server:
            self.http_server.socket.close()
            self.http_server = None


if __name__ == '__main__':
    server = RodServer(2000)
    server.record(method='GET', url='/hello.html', body='hello')
    server.start()
    try:
        while (True):
            time.sleep(0.1)
    except KeyboardInterrupt:
        server.stop()

