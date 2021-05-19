from flask import Flask, Response, render_template, request, make_response, url_for, session, flash
import os

from register import Register
from camera import VideoCamera, Generate
from login import Authenticate
from newmember import AddMember
from addsession import AddSession
from trial import T

app = Flask(__name__)

app.config["SECRET_KEY"] = "xd3i2437rxqkbdq323"

@app.route('/', methods = ['GET', 'POST'])
def indexfunc():
    return render_template('index.html') 


@app.route('/signup', methods = ['GET', 'POST'])
def signupfunc():
    return render_template('signup.html')


@app.route('/addmember', methods = ['GET', 'POST'])
def addememberfunc():
    if 'useName' not in session:
        return indexfunc()
    if request.method=='POST':
        name = request.form.get('membername')
        rollno = request.form.get('rollno')
        email = request.form.get('email')
        contact = request.form.get('contact')
        photo = request.files.get('photo')
        obj = AddMember(session['useName'])
        obj.Add(name, rollno, email, contact, photo)
    return render_template('addmember.html')


@app.route('/home', methods = ['GET', 'POST'])
def homepagefunc():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        if request.form.get('email') is not None: 
            email = request.form.get('email')
            contact = request.form.get('contact')
            obj = Register()
            obj.CreateAccount(name, password, email, contact)
            obj.CreateFolder(name)
            session["useName"] = name
        else:
            result = Authenticate.Verify(name, password)
            if result == True:
                session["useName"] = name
    return render_template('home.html', username=session["useName"])


@app.route('/webcam', methods = ['GET', 'POST'])
def camfunc():
    session = request.form.get('sessionName')
    VideoCamera.sessionName = session
    return render_template('webcam.html')


@app.route('/video', methods = ['GET', 'POST'])
def video_feed():
    vid = VideoCamera(session["useName"])
    return Response(Generate.Gen(vid), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/newsession', methods = ['GET', 'POST'])
def sessfunc():
    obj=T()
    obj.t()
    # if request.method == 'POST':
    #     print('POST')
    #     sessionName = request.form.get('sessionName')
    #     obj = AddSession(session['useName'])
    #     obj.add(sessionName)
    return render_template('addsession.html')
    

@app.route('/selectsession', methods = ['GET', 'POST'])
def selectsessfunc():
    obj = AddSession(session['useName'])
    all_sessions = obj.fetch()
    return render_template('selectsession.html', sessions = all_sessions)


app.run()
