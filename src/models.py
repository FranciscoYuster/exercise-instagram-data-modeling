import os
import sys
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er
import datetime

Base = declarative_base()

followers = Table(
    'followers', 
    Base.metadata, 
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    bio = Column(String(300))
    create_at = Column(DateTime, default=datetime.datetime.now)
    

    posts = relationship("Post", backref='user')
    comments = relationship('Comment', backref='user')
    likes = relationship('Like', backref='user')
    followers = relationship('User', 
                             secondary=followers,
                             primaryjoin=(followers.c.follower_id == id),
                             secondaryjoin=(followers.c.following_id == id),
                             backref='following') 
    
    messages_sent = relationship('Message', foreign_keys="[Message.sender_id]", 
                                 primaryjoin="User.id==Message.sender_id")
    messages_received = relationship('Message', foreign_keys="[Message.receiver_id]", 
                                     primaryjoin="User.id==Message.receiver_id")
    stories = relationship('Story', backref='user')   




class Post(Base):
    __tablename__ = 'posts'
    id= Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    caption = Column(String(100), nullable=False)
    crate_at = Column(DateTime, default=datetime.datetime.now)
    
    

class Comments(Base):
    __tablename__ = 'comments'
    id= Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(String(100), nullable=False)
    crate_at = Column(DateTime, default=datetime.datetime.now)

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)



class Message(Base):
    __tablename__ = 'messages'    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    create_at = Column(DateTime, default=datetime.datetime.now)

    
class Story(Base):
    __tablename__ = 'stories'    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    create_at = Column(DateTime, default=datetime.datetime.now)
    expires_at = Column(DateTime, default=datetime.datetime.now) # sumar 24horas


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
