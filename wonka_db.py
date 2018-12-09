import sqlite3

def dict_factory(cursor, row):
    d = {}  
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class wonkaDB:
    def __init__(self):
        print("Connecting to DB..")
        self.connection = sqlite3.connect("wonka.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def __del__(self):
        print("Disconnecting from DB..")
        self.connection.close()

    def createTables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ticket(id INTEGER PRIMARY KEY, entrant_name TEXT NOT NULL, entrant_age INTEGER NOT NULL, guest_name TEXT NOT NULL, random_token INTEGER NOT NULL)")
        self.connection.commit()

    def createTicket(self, name, age, guest, token):
        self.cursor.execute("INSERT into ticket (entrant_name, entrant_age, guest_name, random_token) VALUES (?, ?, ?, ?)", [name, age, guest, token])
        self.connection.commit()
    
    def getTickets(self):
        self.cursor.execute("SELECT * FROM ticket")
        return self.cursor.fetchall()