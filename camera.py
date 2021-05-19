import cv2
from imutils.video import WebcamVideoStream
from recognizer import Detector
from flask import session
from markattendance import Mark
import time
import datetime

class VideoCamera(object):
    sessionName = ''
    def __init__(self, username):
        self.stream = WebcamVideoStream(src=0).start()
        self.username = username
        self.obj1 = Detector(self.username)
        self.all_encodings_to_numpy = self.obj1.fetch_encodings()
        self.all_names = self.obj1.fetch_names()
        self.obj2 = Detector(self.username)#trying
        print(self.all_names)
        self.session_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.session_time = datetime.datetime.now().strftime('%H:%M:%S')

        self.temp = 0

        self.obj3 = Mark(self.username, self.sessionName, self.session_date, self.session_time, self.all_names)

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        self.temp = self.temp + 1
        image = self.stream.read()

        if self.temp%500==0:
            # self.obj2 = Detector(self.username)
            self.image, self.name = self.obj2.check(image, self.all_encodings_to_numpy, self.all_names)

            if self.name:
                image = cv2.putText(image, self.name, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
                self.obj3.present(self.name)

        ret, jpeg = cv2.imencode('.jpg', image)
        data = [] #needed?-yes
        data.append(jpeg.tobytes())
        return data

class Generate():
    def Gen(cam):
        while True:
            data = cam.get_frame()
            frame = data[0]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')






