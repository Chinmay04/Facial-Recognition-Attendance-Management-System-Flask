import mysql.connector
import os

base_folder = 'static/User Accounts/'
images_folder = '/images'
files_folder = '/sheets'

class Register():
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password='dptstillworking')
        self.c = self.conn.cursor()

    def __del__(self):
        print('Closing')
        self.conn.close()
        self.connDb.close()
        self.connrootDb.close()

    def CreateAccount(self, name, password, email, contact):
        self.c.execute('create database '+name)
        self.conn.commit()
        
        self.connDb = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database=name)
        self.cDb = self.connDb.cursor()
        self.cDb.execute('create table Members (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(100), rollno int, email varchar(255), contact bigint, path varchar(255), encodings varchar(5000))')
        self.cDb.execute('create table Sessions (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(50))')
        self.cDb.execute('create table Attendance (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, session varchar(50), date varchar(20), time varchar(20))')
        
        self.default_Session = 'Whole Day'
        self.sessquery = f"insert into Sessions (name) value ('{self.default_Session}')"
        print(self.sessquery)
        self.cDb.execute(self.sessquery)

        self.connDb.commit()
        

        self.query = 'insert into roottable (accname, accpassword, accmail, acccontact) values (%s, %s, %s, %s)'
        self.values = (name, password, email, contact)

        self.connrootDb = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database='rootdb')
        self.crD = self.connrootDb.cursor()
        self.crD.execute(self.query, self.values)

        self.connrootDb.commit()


    def CreateFolder(self, name):
        os.mkdir(base_folder+name)
        os.mkdir(base_folder+name+images_folder)
        os.mkdir(base_folder+name+files_folder)        
