from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
from datetime import datetime

db=SQLAlchemy()

#create_tracker
class tracker(db.Model):
    __tablename__='Tracker'
    id=db.Column(db.Integer, nullable=False, primary_key=True,  autoincrement = True)
    name=db.Column(db.String(255), nullable=False)
    description=db.Column(db.String(255), nullable=False)
    tracker_type=db.Column(db.String(25), nullable=False)
    setting = db.Column(db.String(150))     
    date_created=db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    logs=db.relationship('logs',secondary='tracker_logs', lazy=True, backref=db.backref('tracker',lazy=True))
    # user= db.Column(db.Integer, db.ForeignKey('User_Profile.user_id'), nullable = False, autoincrement = True)

#create_user
class User(db.Model,UserMixin):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(255),unique=True)
    username = db.Column(db.String(200),nullable=False)
    # name = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(300),nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255),unique=True,nullable=False)
    roles = db.relationship('Role',secondary='user_roles',backref=db.backref('User',lazy='dynamic'))
    trackers = db.relationship('tracker',secondary='user_trackers', lazy=True, backref=db.backref('User',lazy=True))
    
    # def __repr__(self):
    #     return '<User (username = %r)>' %(self.username) 

class Role(db.Model,RoleMixin):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(101),unique=True)
    description = db.Column(db.String(255))


#Log_table
class logs(db.Model):
    __tablename__="logs"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    timestamp=db.Column(db.DateTime, default=datetime.utcnow) 
    log=db.Column(db.String(255))
    value=db.Column(db.Integer, nullable=False)
    note=db.Column(db.String(255), nullable=True)       
    
#helper_0
user_roles = db.Table('user_roles',
    db.Column('user_id',db.Integer(),db.ForeignKey('user.user_id'),primary_key=True),
    db.Column('role_id',db.Integer(),db.ForeignKey('role.role_id'),primary_key=True)
    )

#helper_1
user_trackers = db.Table('user_trackers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('tracker_id', db.Integer, db.ForeignKey('Tracker.id'), primary_key=True)
)

#helper_2
tracker_logs = db.Table('tracker_logs',
    db.Column('tracker_id', db.Integer, db.ForeignKey('Tracker.id'), primary_key=True),
    db.Column('log_id', db.Integer, db.ForeignKey('logs.id'), primary_key=True)
)

