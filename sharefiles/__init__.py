import os
import io
import sys
import urllib
import html
from http.server import *
from http import HTTPStatus
import http.server, cgi, pathlib
from http.server import SimpleHTTPRequestHandler
import socketserver

class RequestHandlerWithUpload(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        
        self.upload_el = '''
            <form action="" method="POST" enctype="multipart/form-data">
            <input name="file" type="file" multiple='multiple'>+Add File(s)<br>
            <input type="submit">
            </form>
            '''
        
        super(SimpleHTTPRequestHandler, self).__init__(*args, **kwargs)


    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).
        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().
        """
        try:
            list = os.listdir(path)
            # list.append(0, self.upload_el)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')
        
        r.append(self.upload_el)####################
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>'
                    % (urllib.parse.quote(linkname,
                                          errors='surrogatepass'),
                       html.escape(displayname, quote=False)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, 
                                environ={'REQUEST_METHOD': 'POST'})
        if 'file' in form:
            if not isinstance(form['file'], list):
                files = [form['file']]
            else:
                files = form['file']
            for file in files:
                if file.file and file.filename:
                    with open(os.path.join(os.getcwd(),self.path[1:],file.filename), "wb") as f:
                        f.write(file.file.read())
        self.do_GET()

def main():
    from functools import partial
    from http import HTTPStatus
    def test(HandlerClass=BaseHTTPRequestHandler,
             ServerClass=ThreadingHTTPServer,
             protocol="HTTP/1.0", port=8000, bind=""):
        """Test the HTTP request handler class.
        This runs an HTTP server on port 8000 (or the port argument).
        """
        server_address = (bind, port)

        HandlerClass.protocol_version = protocol
        with ServerClass(server_address, HandlerClass) as httpd:
            sa = httpd.socket.getsockname()
            serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
            print(serve_message.format(host=sa[0], port=sa[1]))
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting.")
                sys.exit(0)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--cgi', action='store_true',
                       help='Run as CGI Server')
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    args = parser.parse_args()
    if args.cgi:
        handler_class = CGIHTTPRequestHandler
    else:
        handler_class = partial(RequestHandlerWithUpload,
                                directory=args.directory)
    test(HandlerClass=handler_class, port=args.port, bind=args.bind)

