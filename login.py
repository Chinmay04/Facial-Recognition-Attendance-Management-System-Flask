import mysql.connector

class Authenticate():
	def Verify(name, password):
		connDb = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database='rootdb')
		query = "select accpassword from roottable where accname = '{}'".format(name)
		cDb = connDb.cursor()
		cDb.execute(query)
		p = cDb.fetchall()
		connDb.close()
		if p == []:
			return False
		if p[0][0] == password:
			return True
		return False
