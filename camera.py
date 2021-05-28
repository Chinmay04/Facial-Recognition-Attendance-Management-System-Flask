#!/usr/bin/env python3.7
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

model_load = load_model('model_i1.h5')

def predict(frame):
    results = {0:'A', 1:'B', 2:'C'}
    new_array = cv2.resize(frame,(50,50))
    new_array = np.array(new_array).reshape(-1,50,50) 
    new_array = new_array/255.0
    new_array = new_array.reshape(-1,50,50,3)
    prediction = np.argmax(model_load.predict(new_array), axis=-1)[0]
    return results[prediction]


import cv2
from imutils.video import WebcamVideoStream

class VideoCamera(object):
    def __init__(self):
        self.stream = WebcamVideoStream(src=0).start()
    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        image = self.stream.read()
        letter = predict(image)
        image = cv2.putText(image, letter, (50, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 0, 0) , 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        return data

class Generate():
    def Gen(cam):
        while True:
            data = cam.get_frame()
            frame = data[0]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')



    
    
