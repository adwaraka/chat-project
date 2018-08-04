from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import contextlib
import random
import ast

class ChatHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.conn = sqlite3.connect("chat_server.sqlite", isolation_level=None)
        self.conn.text_factory = str
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
        if "/messages" in self.path:
            self.get_message()

    '''check implementation goes here'''
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

    '''create_user implementation goes here'''
    def create_user(self):
        try:
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            print post_body
            data = ast.literal_eval(post_body)
            username, password = data["username"], data["password"]
            user_id_list = [random.randint(0,9) for i in xrange(5)]
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

    '''login_user implementation goes here'''
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
                print number_of_rows
            return number_of_rows==1
        except:
            return False

    '''
    send_message implementation goes here
    query format: UPDATE chat_session SET chat_field = chat_field || <new_stmt> WHERE user_id_1="UName_6869" AND user_id_2="adwaraka257_82086_48726";
    '''
    def update_message_history(self, swapFlag, sender_id, recepient_id, msg_type, data):
        chat_line=None
        try:
            with contextlib.closing(self.conn.cursor()) as cur:
                if swapFlag:
                    chat_line="".join(["<som>", "[", sender_id, "]: ", data, "<eom>"])
                    update_chat_with_new = "UPDATE chat_session SET chat_field = chat_field || \"{new_chat_line}\" WHERE user_id_1=\"{sender_id_val}\" AND user_id_2=\"{recepient_id_val}\"".format\
                                           (new_chat_line=chat_line, sender_id_val=sender_id, recepient_id_val=recepient_id)
                else:
                    chat_line="".join(["<som>", "[", recepient_id, "]: ", data, "<eom>"])
                    update_chat_with_new = "UPDATE chat_session SET chat_field = chat_field || \"{new_chat_line}\" WHERE user_id_2=\"{sender_id_val}\" AND user_id_1=\"{recepient_id_val}\"".format\
                                           (new_chat_line=chat_line, sender_id_val=sender_id, recepient_id_val=recepient_id)
                cur.execute(update_chat_with_new)
                return True
            raise ValueError('Chat did not go. Dunno what happened...')
        except:
            return False

    def send_message(self):
        swap_sender_recipient = False
        cleaned_chat_history = None
        try:
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            data = ast.literal_eval(post_body)
            with contextlib.closing(self.conn.cursor()) as cur:
                initial_stmt = "SELECT COUNT(*) FROM chat_session WHERE ({sender_field} = \"{user_id_sender}\" AND {recipient_field} = \"{user_id_recipient}\")".format\
                               (sender_field="user_id_1", user_id_sender=data["sender"], recipient_field="user_id_2", user_id_recipient=data["recipient"])
                cur.execute(create_user_stmt)
                (number_of_rows,) = cur.fetchone()
                if number_of_rows == 0:
                    swap_sender_recipient = True
            return self.update_message_history(swap_sender_recipient, data["sender"], data["recipient"], data["content"]["type"], data["content"]["text"])
        except:
            return False

    '''
    get_message implementation goes here
    Test path: http://localhost:8080/messages/UName_6869/?recipient=adwaraka257_82086_48726
    '''
    def get_message(self):
        try:
            bits = self.path
            sender_user_id, recipient_user_id = bits.split("/")[2], bits.split("/")[3].split("=")[1]
            with contextlib.closing(self.conn.cursor()) as get_chat_history_cur:
                retrieve_chat_history = "SELECT chat_field FROM chat_session WHERE ({sender_field} = \"{user_id_sender}\" AND {recipient_field} = \"{user_id_recipient}\") \
                                         UNION SELECT chat_field FROM chat_session WHERE ({sender_field} = \"{user_id_recipient}\" AND {recipient_field} = \"{user_id_sender}\")".format\
                                   (sender_field="user_id_1", user_id_sender=sender_user_id, recipient_field="user_id_2", user_id_recipient=recipient_user_id)
                get_chat_history_cur.execute(retrieve_chat_history)
                result = get_chat_history_cur.fetchall()
                chat_history = result
            if chat_history != []:
                (cleaned_chat_history,) = chat_history[0]
                return cleaned_chat_history
            else:
                return None
        except:
            return None

def run():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, ChatHandler)
    print "Chat server is running....."
    httpd.serve_forever()

if __name__== "__main__":
    run()
