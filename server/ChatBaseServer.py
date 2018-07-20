from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import contextlib


class ChatHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.conn = sqlite3.connect("chat_server.sqlite")
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        '''
        use this for basic checkup
        curl -s -d '' -XPOST http://localhost:8080/check
        OR
        curl -v POST http://localhost:8080/createUser -d @test.json --header "Content-Type: application/json"

        '''
        if self.path == "/check":
            self.handle_check()
        elif self.path == "/createUser":
            self.create_user()
        elif self.path == "/login":
            self.login_user()
        elif self.path == "/sendMessage":
            self.send_message()

    def do_GET(self):
        if self.path == "/getMessages":
            self.get_message()

    #check implementation goes here
    def handle_check(self):
        if self.query_health() != 1:
            raise Exception('unexpected query result')
        self.wfile.write(json.dumps({"health": "ok"}).encode('UTF-8'))
        self.send_response(200)

    def query_health(self):
        with contextlib.closing(self.conn.cursor()) as cur:
            cur.execute('SELECT 1')
            (res, ) = cur.fetchone()
            return res

    #create_user implementation goes here
    def create_user(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print post_body

    #login_user implementation goes here
    def login_user(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print post_body

    #send_message implementation goes here
    def send_message(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print post_body

    #get_message implementation goes here
    def get_message(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print post_body

def run():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, ChatHandler)
    print "Chat server is running....."
    httpd.serve_forever()

if __name__== "__main__":
    run()
