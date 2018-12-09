from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import bcrypt
import random
from wonka_db import wonkaDB
from http import cookies

class serverHandler(BaseHTTPRequestHandler):

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session(self):
        # assign oompa value to cookie
        self.load_cookie()
        if "oompa" in self.cookie:
            return

    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)


    def do_GET(self):
        self.load_session()
        if self.path == "/tickets":
            self.handleTicketList()
        else:
            self.handleNotFound()
    
    def do_POST(self):
        self.load_session()
        if self.path == "/tickets":
            self.handleTicketCreate()
        else:
            self.handleNotFound()

    def handleTicketCreate(self):
        length = self.headers["Content-length"]
        # read the body data from the client
        body = self.rfile.read(int(length)).decode("utf-8")
        # parse the body to a dictionary
        data = parse_qs(body)

        name = data['name'][0]
        age = data['age'][0]
        guest = data['guest'][0]
        token = random.randint(0, 6)

        if "oompa" not in self.cookie:
            #send to db
            db = wonkaDB()
            db.createTicket(name, age, guest, token)
            
            self.send_response(201)
            self.cookie["oompa"] = "loompa"
            self.end_headers()
        else:
            self.handle403()

    def handleTicketList(self):
        self.send_response(200) 
        self.send_header("Content-type", "application/json")
        self.end_headers()
        db = wonkaDB()
        tickets = db.getTickets()
        self.wfile.write(bytes(json.dumps(tickets), "utf-8"))
    

    def handle403(self):
        # 403 response
        self.send_response(403)
        self.send_header("Content-type", "text-html")
        self.end_headers()
        self.wfile.write(bytes("The Ooompa Loopas have already recieved our ticket. Please try again tomorrow", "utf-8"))

    
    def handleNotFound(self):
        # 404 response 
        self.send_response(404)
        self.send_header("Content-type", "text-html")
        self.end_headers()
        self.wfile.write(bytes("It seems that this resource has been lost in the chocolate pipes. An Oompa Loompa will be dispatched promptly to recover the artifact", "utf-8"))

def run():
    db = wonkaDB()
    db.createTables()
    db = None

    listen = ("0.0.0.0", 8080)
    server = HTTPServer(listen, serverHandler)

    server.serve_forever()
run()
