from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import os


class HTTPHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


class HTTPServer(BaseHTTPServer):
    def __init__(
            self,
            base_path,
            server_address,
            RequestHandlerClass=HTTPHandler
            ):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)


def run():

    web_dir = os.path.join(os.path.dirname(__file__), 'dist')
    httpd = HTTPServer(web_dir, ("", 8080))
    httpd.serve_forever()
