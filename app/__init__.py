from flask import Flask, render_template, request
from flask_sqlalchemy import  SQLAlchemy
from flask_socketio import SocketIO
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost/chat'
app.config["SECRET_KEY"] = "random"
app.config['UPLOAD_FOLDER']='app/static'

socketio = SocketIO(app)
db =SQLAlchemy(app)

from app import route