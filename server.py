# most of this is set up for the server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import MySQLdb
import urlparse
import socket
import json
from chatbot import predict_from_bot

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        # self._set_headers()
        print(self.path)
        url = urlparse.urlsplit(self.path)
        if url.path == "/login":
            email = urlparse.parse_qs(url.query).get("email")[0]

            db = MySQLdb.connect(host="localhost",
                                 user="root",
                                 passwd="root",
                                 db="chatbot")
            cursor = db.cursor()
            try:
                if cursor.execute("SELECT pass_hash FROM users WHERE email = '" + email + "';") != 0:  # user exists
                    self.send_response(200)                                                           # in db
                    self.end_headers()
                    self.wfile.write(cursor.fetchone()[0])
                else:
                    self.send_response(401)
                    self.end_headers()
            finally:
                cursor.close()
                db.close()

        elif url.path == "/getDevices":
            email = urlparse.parse_qs(url.query).get("email")[0]

            db = MySQLdb.connect(host="localhost",
                                 user="root",
                                 passwd="root",
                                 db="chatbot")
            cursor = db.cursor()
            try:
                cursor.execute("SELECT * FROM devices WHERE owner = '" + email + "';")
                devices = json.dumps(cursor.fetchall())
                print devices
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({'devices': devices}))
            finally:
                cursor.close()
                db.close()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print(post_data)
        url = urlparse.urlsplit(self.path)
        if url.path == "/register":
            data = json.loads(post_data)
            email = data.get("email")
            passhash = data.get("pass_hash")

            db = MySQLdb.connect(host="localhost",
                                 user="root",
                                 passwd="root",
                                 db="chatbot")
            cursor = db.cursor()
            try:
                if cursor.execute("SELECT * FROM users WHERE email = '" + email + "';") != 0:  # user already exists
                    self.send_response(409)
                    self.end_headers()
                else:
                    cursor.execute("INSERT INTO users (email, pass_hash) VALUES ('" + email + "', '" + passhash + "');")
                    db.commit()
                    self.send_response(200)
                    self.end_headers()
            finally:
                cursor.close()
                db.close()

        elif url.path == "/message":
            message = json.loads(post_data)
            message = message.get("message")
            response = predict_from_bot(message)  # prediction from the bot
            print(response)
            self.send_response(200)  # in db
            self.end_headers()
            self.wfile.write(response)

        elif url.path == "/addDevice":
            data = json.loads(post_data)
            email = data.get("email")
            name = data.get("name")
            type = data.get("type")
            device_data = data.get("data")

            db = MySQLdb.connect(host="localhost",
                                 user="root",
                                 passwd="root",
                                 db="chatbot")
            cursor = db.cursor()
            try:
                if cursor.execute("SELECT * FROM devices WHERE owner = '" + email + "' AND name = '" + name + "';") != 0:
                    self.send_response(409)
                    self.end_headers()
                else:
                    cursor.execute("INSERT INTO devices (owner, name, type, data) VALUES ('"
                                   + email + "', '" + name + "', " + str(type) + ", '" + json.dumps(device_data) + "');")
                    db.commit()
                    self.send_response(200)
                    self.end_headers()
            finally:
                cursor.close()
                db.close()



def run(server_class=HTTPServer, handler_class=Server, port=8081):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd at " + socket.gethostbyname(""))
    httpd.serve_forever()
