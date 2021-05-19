import face_recognition
import cv2
import mysql.connector
import numpy as np

class Detector():
    def __init__(self, username):
        self.username = username
        self.connDb = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database=self.username)
        self.cDb = self.connDb.cursor()

    def __del__(self):
      pass

    def fetch_encodings(self):
        self.encoding_query='select encodings from members'
        self.cDb.execute(self.encoding_query)
        self.result = self.cDb.fetchall()
        self.all_encodings = [eval(self.i[0]) for self.i in self.result]
        self.all_encodings_to_numpy = np.array(self.all_encodings[0])
        self.all_encodings_to_numpy = np.expand_dims(self.all_encodings_to_numpy, axis=0)
        for self.i in range(1, len(self.all_encodings)):
              self.all_encodings_to_numpy = np.append(
                    self.all_encodings_to_numpy, np.expand_dims(np.array(self.all_encodings[self.i]), axis=0),
                    axis=0)
        return self.all_encodings_to_numpy        

    def fetch_names(self):
        self.name_query = 'select name from members'
        self.cDb.execute(self.name_query)
        self.names = self.cDb.fetchall()
        self.all_names = [self.i[0] for self.i in self.names]
        return self.all_names

    def check(self, frame,  all_encodings_to_numpy, all_names):
        self.encodings = face_recognition.face_encodings(frame)
        
        if self.encodings==[]:
            print('No Face')
            self.name = ''
            return frame, self.name
        
        for self.i, self.name in zip(all_encodings_to_numpy, all_names):
            if face_recognition.compare_faces(self.encodings, self.i)[0]:
                print(self.name)
                self.new_frame = cv2.putText(frame, self.name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.FILLED)
                return self.new_frame, self.name
        
        print('No Match')
        self.name = ''
        return frame, self.name
