from app import db
from datetime import datetime
from flask_login import UserMixin

class Chatusers(UserMixin,db.Model):
    __tablename__="chatusers"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30) , unique=True,nullable=False)
    email =db.Column(db.String(30) , unique=True,nullable=False)
    image_file=db.Column(db.String(30),nullable=False,default='default.jpg')
    password = db.Column(db.String(50),unique=True,nullable=False)
    posts = db.relationship('Post',backref='chatusers',lazy=True)

    # def __init__(self,username,email,image_file,password):
    #     self.username=username
    #     self.email=email
    #     self.image=image_file
    #     self.password=password

    # def __repr__(self):
    #     return f'username {self.username},{self.image_file}'
    def serialize(self):
        return {"id":self.id,
                "username":self.username,
                "password":self.password,
                "email":self.email}

class Post(UserMixin,db.Model):
    __tablename__ = "post"
    id=db.Column(db.Integer,primary_key=True)
    date_posted= db.Column(db.DateTime ,nullable=False,default=datetime.utcnow)
    content = db.Column(db.String(100), nullable=True)
    user_id =db.Column(db.Integer,db.ForeignKey('chatusers.id'),nullable=False)

    # def __init__(self,content):
    #     self.content=content

    def __repr__(self):
        return f'time {self.date_posted}'
    def serialize(self):
        return {"id":self.id,
                "date":self.date_posted,
                "content":self.content}

