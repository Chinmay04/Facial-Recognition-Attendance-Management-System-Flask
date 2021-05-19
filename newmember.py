import mysql.connector
import os
import face_recognition

base_folder = 'static/User Accounts/'
images_folder = '/images/'

class AddMember():
	def __init__(self, user):
		self.user = user
		self.connDb = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database=user)
		self.cDb = self.connDb.cursor()

	def __del__(self):
		print('Here')
		self.connDb.close()

	def Add(self, name, rollno, email, contact, photo):
		self.image_path = base_folder+self.user+images_folder+name+'.jpg'
		photo.save(self.image_path)
		# name = name.replace(' ','-')
		self.image = face_recognition.load_image_file(self.image_path)
		print(self.image)
		self.face_encodings = face_recognition.face_encodings(self.image)
		if self.face_encodings == []:
			return False
		print('ENC',self.face_encodings)
		self.encodings_to_string = str(list(self.face_encodings[0]))
		print('strto')
		self.query = 'insert into members (name, rollno, email, contact, path, encodings) values (%s, %s, %s, %s, %s, %s)'
		self.values = (name, rollno, email, contact, self.image_path, self.encodings_to_string)

		self.cDb.execute(self.query, self.values)
		print('insert')
		self.alter = f"alter table attendance add column `{name}` tinyint"
		print('q')
		self.cDb.execute(self.alter)
		print('alter')
		self.connDb.commit()
		print('commited')

		return True

		