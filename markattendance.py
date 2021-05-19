import mysql.connector

session = 'Whole Day'

class Mark():
	def __init__(self, username, sessionName, date, time, all_names):
		self.s = sessionName
		self.all_names = all_names
		self.username = username
		self.date = date
		self.time = time
		self.connDb = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database=self.username)
		self.cDb = self.connDb.cursor()

		self.initsessionquery = f"insert into attendance (session,date,time) values ('{sessionName}','{date}','{time}')"
		self.cDb.execute(self.initsessionquery)

	def __del__(self):
		print('Closing')
		for self.name in self.all_names:
			self.absent = f"update attendance set {self.name}=0 where time='{self.time}'"
			self.cDb.execute(self.absent)
		self.connDb.commit()
		self.connDb.close()

	def present(self, name):
		self.all_names.remove(name)
		self.query = f"update attendance set `{name}`=1 where time='{self.time}'"
		self.cDb.execute(self.query)
