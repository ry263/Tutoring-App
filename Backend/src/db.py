from tokenize import String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer

db = SQLAlchemy()

ins_assoc_table = db.Table(
    "course_ins_assoc",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("instructor_id", db.Integer, db.ForeignKey("users.id"))
)

time_assoc_table = db.Table(
    "user_time_assoc",
    db.Column("time_id" , db.Integer, db.ForeignKey("availability.id")),
     db.Column("user_id", db.Integer, db.ForeignKey("users.id"))

)


# your classes here
class Course(db.Model):
    """
    Course model
    Has a many-to-many relationship with the User model
    """
    __tablename__ = "courses"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    code = db.Column(db.String, nullable=False)
    #name = db.Column(db.String, nullable=False)
    #assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship("User", secondary=ins_assoc_table, back_populates="icourses")
    #students = db.relationship("User", secondary=stu_assoc_table, back_populates="scourses")

    def __init__(self, **kwargs):
        """
        initialize Course object
        """
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):   
        """
        Serialize a course object
        """ 
        return {        
            "id": self.id,        
            "code": self.code,        
            "tutors": [i.serialize_nc() for i in self.instructors]
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
    __tablename__ = "users"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.String, nullable=False)
    #year = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    icourses = db.relationship("Course", secondary=ins_assoc_table, back_populates="instructors")
    availability = db.relationship("Availability", cascade = "delete")
    rate = db.Column(db.String, nullable=False)
    
    #scourses = db.relationship("Course", secondary=stu_assoc_table, back_populates="students")

    def __init__(self, **kwargs):
        """
        Initializes User object
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")

    def serialize(self):   
        """
        Serialize a User object
        """ 
        return {        
            "id": self.id,               
            "name": self.name,    
            "netid": self.netid,
            "courses": ([c.serialize_nc() for c in self.icourses]),
            "availabiltiy": [a.serialize_nc() for a in self.availability],
            "rate": self.rate

            #+ [c.serialize_nc() for c in self.scourses])
            #"courses": list(set([c.serialize_nc() for c in self.icourses] + [c.serialize_nc() for c in self.scourses]))
        }

    def serialize_nc(self):   
        """
        Serialize a User object without courses field
        """ 
        return {        
            "id": self.id,               
            "name": self.name,    
            "netid": self.netid,
            "availabiltiy": [a.serialize_nc() for a in self.availability],
            "rate":self.rate
        }
    
class Availability(db.model):
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

class Notification(db.model):
    """
    Notification model
    """
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes Notification object
        """
        self.note = kwargs.get("note", "")
    
    def serialize(self):   
        """
        Serialize a Notification object
        """ 
        return {        
            "id": self.id,               
            "note": self.note
        }
        
