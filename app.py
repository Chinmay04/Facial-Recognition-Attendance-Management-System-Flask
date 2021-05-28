#!/usr/bin/env python3.7
from flask import Flask, render_template, Response
from camera import VideoCamera, Generate

app = Flask(__name__)

@app.route('/')
def camfunc():
    return render_template('webcam.html')

@app.route('/video')
def video_feed():
    return Response(Generate.Gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run()
