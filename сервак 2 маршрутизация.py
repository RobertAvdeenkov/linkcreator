from http.server import HTTPServer,BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path
        status=200
        content=0
        res=b'<h1> PAGE NOT FOUND <h1>'
        other=b'<font size=\'3\'> We are sorry :( <font size=\'3\'>'
        if path.endswith('/'):
            res=b'<h1> MAIN PAGE <h1>'
            other=b'<font size=\'3\'> Here you can see the most important information <font size=\'3\'>'
        elif path.endswith('/about'):
            res=b'<h1> ABOUT <h1>'
            other=b'<font size=\'3\'>  There is another information <font size=\'3\'>'
        elif path.endswith('/contact'):
            res=b'<h1> CONTACT <h1>'
            other=b'<font size=\'3\'>  Contact:\n+7-915-499-5909 <font size=\'3\'>'
        else: 
            status=404
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(res)
        self.wfile.write(other)

name='localhost'
port=8000
web=HTTPServer((name,port),Handler)
web.server_activate()
print('Server is running')
print(f'Link: http://{name}:{port}')
print('-'*65)
try:
    web.serve_forever()
except:
    web.server_close()
    
print('Server was closed')
