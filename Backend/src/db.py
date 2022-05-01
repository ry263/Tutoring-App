from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ins_assoc_table = db.Table(
    "course_ins_assoc",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("instructor_id", db.Integer, db.ForeignKey("users.id"))
)
stu_assoc_table = db.Table(
    "course_stu_assoc",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("student_id", db.Integer, db.ForeignKey("users.id"))
)

# your classes here
class Course(db.Model):
    """
    Course model
    Has a many-to-many relationship with the User model
    Has a one-to-many relationship with the Assignment model
    """
    __tablename__ = "courses"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship("User", secondary=ins_assoc_table, back_populates="icourses")
    students = db.relationship("User", secondary=stu_assoc_table, back_populates="scourses")

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
            "name": self.name,    
            "assignments": [a.serialize_nc() for a in self.assignments],
            "instructors": [i.serialize_nc() for i in self.instructors],
            "students": [s.serialize_nc() for s in self.students]
        }

    def serialize_nc(self):   
        """
        Serialize a course object without users and assignments fields
        """ 
        return {        
            "id": self.id,        
            "code": self.code,        
            "name": self.name  
        }
    
class User(db.Model):  
    """
    User model
    """  
    __tablename__ = "users"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    icourses = db.relationship("Course", secondary=ins_assoc_table, back_populates="instructors")
    scourses = db.relationship("Course", secondary=stu_assoc_table, back_populates="students")

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
            "courses": ([c.serialize_nc() for c in self.icourses] + [c.serialize_nc() for c in self.scourses])
            #"courses": list(set([c.serialize_nc() for c in self.icourses] + [c.serialize_nc() for c in self.scourses]))
        }

    def serialize_nc(self):   
        """
        Serialize a User object without courses field
        """ 
        return {        
            "id": self.id,               
            "name": self.name,    
            "netid": self.netid
        }
    

class Assignment(db.Model):    
    __tablename__ = "assignments"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    

    def __init__(self, **kwargs):
        """
        Initializes Assignment object
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", 0)
        self.course_id = kwargs.get("course_id")

    def serialize(self):   
        """
        Serialize an Assignment object
        """ 
        course = Course.query.filter_by(id=self.course_id).first()
        return {        
            "id": self.id,        
            "title": self.title,        
            "due_date": self.due_date,
            "course": course.serialize_nc()
        }
    def serialize_nc(self):
        """
        Serialize an Assignment object without course field
        """ 
        return {        
            "id": self.id,        
            "title": self.title,        
            "due_date": self.due_date
        }
    

