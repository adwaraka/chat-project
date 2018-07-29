from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import contextlib
import random
import ast


class ChatHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.conn = sqlite3.connect("chat_server.sqlite", isolation_level=None)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        '''
        use this for basic checkup
        curl -s -d '' -XPOST http://localhost:8080/check
        OR
        curl -v POST http://localhost:8080/createUser -d @test.json --header "Content-Type: application/json"

        '''
        res = False
        if self.path == "/check":
            res = self.handle_check()
            res = True
        elif self.path == "/createUser":
            res = self.create_user()
        elif self.path == "/login":
            res = self.login_user()
        elif self.path == "/sendMessage":
            res = self.send_message()
        if res:
            self.send_response(200)
        else:
            self.send_response(400)  

    def do_GET(self):
        if self.path == "/getMessages":
            self.get_message()

    #check implementation goes here
    def handle_check(self):
        if self.query_health() != 1:
            raise Exception('unexpected query result')
        self.wfile.write(json.dumps({"health": "ok"}).encode('UTF-8'))
        return True

    def query_health(self):
        with contextlib.closing(self.conn.cursor()) as cur:
            cur.execute('SELECT 1')
            (res, ) = cur.fetchone()
            return res

    #create_user implementation goes here
    def create_user(self):
        try:
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            print post_body
            data = ast.literal_eval(post_body)
            username, password = data["username"], data["password"] #obviously we need to use a hash function to encrypt the data
            user_id_list = [random.randint(0,9) for i in xrange(5)] #this needs to change to - better to have an alphanumeric key in db using UUId
            user_id = 0
            for i in user_id_list:
                user_id = user_id*10 + i
            username = "{username}_{user_id}".format(username=username, user_id=str(user_id))
            with contextlib.closing(self.conn.cursor()) as cur:
                create_user_stmt = "INSERT INTO user_credentials ({user_name}, {password}) VALUES (\"{username_val}\", \"{password_val}\")".format\
                                   (user_name="user_name", password="password", username_val=username, password_val=password)
                cur.execute(create_user_stmt)
                print "Added user...."
                return True
            raise ValueError('a very bad thing happened...')
        except:
            return False

    #login_user implementation goes here
    def login_user(self):
        try:
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            data = ast.literal_eval(post_body)
            username, password = data["username"], data["password"]
            with contextlib.closing(self.conn.cursor()) as cur:
                create_user_stmt = "SELECT COUNT(*) FROM user_credentials WHERE ({user_name_field} = \"{username}\" AND {password_field} = \"{password_value}\")".format\
                                   (user_name_field="user_name", username=username, password_field="password", password_value=password)
                cur.execute(create_user_stmt)
                (number_of_rows,) = cur.fetchone()
                return number_of_rows==1
            raise ValueError('a very bad thing happened...')
        except:
            return False

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
