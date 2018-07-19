from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import contextlib


class ChatHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/check":
            self.handle_check()
    
    def handle_check(self):
        if self.query_health() != 1:
            raise Exception('unexpected query result')
        self.wfile.write(json.dumps({"health": "ok"}).encode('UTF-8'))
        self.send_response(200)

    def query_health(self):
        conn = sqlite3.connect('chat_server.sqlite')
        with contextlib.closing(conn.cursor()) as cur:
            cur.execute('SELECT 1')
            (res, ) = cur.fetchone()
            return res

def run():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, ChatHandler)
    print "Chat server is running....."
    httpd.serve_forever()

if __name__== "__main__":
    run()
