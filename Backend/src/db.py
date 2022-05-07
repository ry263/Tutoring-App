from tokenize import String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, DateTime
from flask_login import UserMixin
import datetime
from mimetypes import guess_extension, guess_type
import hashlib
import os
import bcrypt

db = SQLAlchemy()

ins_assoc_table = db.Table(
    "course_ins_assoc",
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("tutor_id", db.Integer, db.ForeignKey("user.id"))
)

"""time_assoc_table = db.Table(
    "user_time_assoc",
    db.Column("time_id" , db.Integer, db.ForeignKey("availability.id")),
     db.Column("user_id", db.Integer, db.ForeignKey("users.id"))

"""


# your classes here
class Course(db.Model):
    """
    Course model
    Has a many-to-many relationship with the User model
    """
    __tablename__ = "course"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    code = db.Column(db.String, nullable=False)
    #name = db.Column(db.String, nullable=False)
    #assignments = db.relationship("Assignment", cascade="delete")
    tutors = db.relationship("User", secondary=ins_assoc_table, back_populates="teaching")
    #students = db.relationship("User", secondary=stu_assoc_table, back_populates="scourses")

    def __init__(self, **kwargs):
        """
        initialize Course object
        """
        self.code = kwargs.get("code", "")
        #self.name = kwargs.get("name", "")

    def serialize(self):   
        """
        Serialize a course object
        """ 
        return {        
            "id": self.id,        
            "code": self.code,        
            "tutors": [t.serialize_nc() for t in self.tutors]
        }

    def serialize_nc(self):   
        """
        Serialize a course object without users field
        """ 
        return {        
            "id": self.id,        
            "code": self.code 
        }
    
class User(db.Model):  
    """
    User model
    """  
    __tablename__ = "user"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    teaching = db.relationship("Course", secondary=ins_assoc_table, back_populates="tutors")
    availability = db.relationship("Availability", cascade = "delete")
    notifications = db.relationship("Notification", cascade = "delete")
    rate = db.Column(db.String, nullable=True)
    profile_pic = db.Column(db.String,nullable = True)

    password_digest = db.Column(db.String, nullable=False)

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        """
        Initializes User object
        """
        self.name = kwargs.get("name", "")
        self.email = kwargs.get("email", "")
        self.profile_pic = kwargs.get("profile_pic")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        #self.renew_session()

"""
    def _urlsafe_base_64(self):
        """
       # Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
       # Renews the sessions, i.e.
        #1. Creates a new session token
        #2. Sets the expiration time of the session to be a day from now
        #3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
       # Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
       # Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
       # Verifies the update token of a user
        """
        return update_token == self.update_token


    def serialize(self):   
        """
       # Serialize a User object
        """ 
        return {        
            "id": self.id,               
            "name": self.name, 
            "image":self.profile_pic,   
            "email": self.email,
            "courses": [c.serialize_nc() for c in self.teaching],
            "availability": [a.serialize() for a in self.availability],
            "rate": self.rate
            

            #+ [c.serialize_nc() for c in self.scourses])
            #"courses": list(set([c.serialize_nc() for c in self.icourses] + [c.serialize_nc() for c in self.scourses]))
        }

    def serialize_nc(self):   
        """
        #Serialize a User object without courses field
        """ 
        return {        
            "id": self.id,               
            "name": self.name,    
            "email": self.email,
            "rate":self.rate
        }
"""
    def serialize_session(self):   
        """
        Serialize a User object
        """ 
        return {        
            "id": self.id,               
            "name": self.name, 
            "image":self.profile_pic,   
            "email": self.email,
            "courses": [c.serialize_nc() for c in self.teaching],
            "availability": [a.serialize() for a in self.availability],
            "rate": self.rate,
            "session_token":self.session_token,
            "session_expiration":str(self.session_expiration),
            "update_token":self.update_token
        }
    
    
class Availability(db.Model):
    """
    Availability model
    """
    __tablename__ = "availability" 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    time = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes Availability object
        """
        self.time = kwargs.get("time", "")
        self.user_id = kwargs.get("user_id", "")

    
    def serialize_nc(self):
        """
        Serialize an Availability object simply
        """ 
        return {                       
            "time": self.time
        }

    def serialize(self):   
        """
        Serialize an Availability object
        """ 
        return {        
            "id": self.id,               
            "time": self.time,
            "user_id":self.user_id 
        }

class Notification(db.Model):
    """
    Notification model
    """
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, nullable = False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    time = db.Column(db.DateTime, nullable=False)



    def __init__(self, **kwargs):
        """
        Initializes Notification object
        """
        self.sender_id = kwargs.get("sender_id", "")
        self.receiver_id = kwargs.get("receiver_id", "")
        self.time = datetime.datetime.utcnow
    
    def serialize(self):   
        """
        Serialize a Notification object
        """ 
        return {        
            "id": self.id,              
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "time": str(self.time)
        }
        
