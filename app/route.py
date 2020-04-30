from flask import render_template,flash, redirect, request, session, url_for
from app import app
from  app.models import Chatusers,Post,db
from app import socketio
from flask_socketio import  emit ,join_room,leave_room,send
from flask_login import LoginManager ,login_user,logout_user,current_user

login =LoginManager(app)
login.init_app(app)

rooms=['game','news','rest','best']

@login.user_loader
def load_user(id):
    return Chatusers.query.get(int(id))

@app.route("/",methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form.get("name")
        password = request.form.get("password")
        print(username, '$$$$$$$$$$')
        uobj=Chatusers.query.filter_by(username=username).first()
        if uobj:
            u=uobj.serialize()
            print(u['password'])
            if u['password'] != password:
                flash('Invlaid Password','danger')
                return render_template('login.html')
            else:
                login_user(uobj)
                print(current_user.username)
                if current_user.is_authenticated:
                    flash('Successfully Loged in','success')
                return render_template('chat.html',res={"mes":'','user':current_user.username},rooms=rooms)
                # else:
                #     return render_template('login.html')
        else:
            flash('Invalid USER','danger')

    return render_template('login.html')

@app.route("/signin",methods=['POST','GET'])
def signin():
    if request.method=='POST':
        username=request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        if RegForm.validator(username=username):
            flash('Already Exist','danger')
            return render_template("signin.html")
        else:
            if password==cpassword:
                if RegForm.add_user(username,email,password):
                    flash('Successfully Signed in','success')
                    return render_template(url_for('/login'))
                else:
                    flash('Unsuccessful Try again','danger')
                    return render_template(url_for('signin'))
                flash('Password Donot Matched','danger')
                return render_template("signin.html")
    return render_template("signin.html")

@app.route("/logout")
def logout():
    print(Game,'\n',Rest)
    logout_user()
    flash('You have logged out successfully', 'success')
    # session.pop('user',None)

    return redirect(url_for('login'))


message={}
@app.route("/chats")
def chats():
    if not current_user.is_authenticated:
        return redirect('/')
    name=current_user.username
    print(current_user)
    # if name in message:
    return render_template('chat.html',res={"mes":'','user':name},rooms=rooms)
    # else:
    #     return render_template('chat.html',res={'mes':None,"user":name},rooms=rooms)

    # return redirect('/')

Game=[]
News=[]
Rest=[]
Best=[]
@socketio.on('submit')
def chat(data):
    print(data)
    user=data['name']
    mes=data['mes']
    room=data['room']
    val={'room':room,'user':user,"mes":mes}
    # val=[room,user,mes]
    eval(f'{room}').append(val)
    param={'user':user,'mes':mes,"room":room}
    print(param)
    emit('announce',param,room=room)

@socketio.on('join')
def join(data):
    print(data,'\n\n@@@@@@@@@join\n\n')
    join_room(data['room'])

    param={"mes":f'{data["username"]} joined {data["room"]} room'}
    send(param,room=data['room'])

@socketio.on('leave')
def leave(data):
    print(data,'\n\n@@@@@@@@@@@@@leave\n\n')
    leave_room(data['room'])
    param={"mes":f'{data["username"]} leaved {data["room"]} room'}
    send(param,room=data['room'])

@socketio.on('cache')
def cache(data):
    cache = eval(f'{data["room"]}')
    print(cache)
    param={"cache":cache}
    emit('memory',param)