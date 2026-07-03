from http.server import BaseHTTPRequestHandler,HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path
        resp=b'<h1>PAGE NOT FOUND<h1>'
        with open('text.txt', 'r') as file:
            content=file.read()
        if path.endswith('/'):
            with open('mainpage.html','rb') as file:
                resp=file.read()
        elif path.endswith('/about'):
            resp=b'<h1>About<h1>'
        elif path.endswith('/contact'):
            resp=b'<h1>Contact<h1>'
        self.send_response(200)
        self.send_header('Content-type', 'text/html;charset=utf-8')
        self.end_headers()
        self.wfile.write(resp)

name='localhost'
port=8000
web=HTTPServer((name,port),Handler)
web.server_activate()
try:
    web.serve_forever()
except:
    web.server_close()