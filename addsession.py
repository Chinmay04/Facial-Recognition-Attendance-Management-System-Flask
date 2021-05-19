import mysql.connector

class AddSession():
    def __init__(self, user):
        self.conn = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database=user)
        self.c = self.conn.cursor()

    def __del__(self):
    	pass

    def add(self, sessionName):
    	self.query = f"insert into sessions (name) values ('{sessionName}')"
    	self.c.execute(self.query)
    	self.conn.commit()

    def fetch(self):
    	self.query = 'select name from sessions'
    	self.c.execute(self.query)
    	self.all_sessions = self.c.fetchall()
    	return [self.i[0] for self.i in self.all_sessions]

