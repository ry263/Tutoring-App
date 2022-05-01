from db import db
from flask import Flask
from flask import request
import json
import os

from db import Course
from db import User
from db import Assignment

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# your routes here
#DB = db.DatabaseDriver()

def success_response(data, code=200):
    return json.dumps(data), code
    #return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code
    #return json.dumps({"success": False, "error": message}), code

@app.route("/")
def get_default():
    """
    Endpoint for printing "<netid> was here!"
    """
    #return json.dumps(os.environ.get("NETID") + " was here!"), 200
    return os.environ.get("NETID") + " was here!"

@app.route("/api/courses/")
def get_courses():
    """
    Endpoint for getting all courses
    """
    return success_response({"courses": [c.serialize() for c in Course.query.all()]})

@app.route("/api/courses/", methods=["POST"])
def make_course():
    """
    Endpoint for creating a course
    """
    body = json.loads(request.data)
    code=body.get("code")
    name=body.get("name")
    if code is None:
        return failure_response("Code field empty", 400)
    if name is None:
        return failure_response("Name field empty", 400)
    new_course = Course(code=code, name=name)
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)

@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    """
    Endpoint for getting a course by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Endpoint for deleting a course
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())

@app.route("/api/users/", methods=["POST"])
def make_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    name=body.get("name")
    netid=body.get("netid")
    if name is None:
        return failure_response("Name field empty", 400)
    if netid is None:
        return failure_response("Netid field empty", 400)
    new_user = User(name = name,netid=netid)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding a user to a course
    """
    #check to make sure all fields present and valid
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    body = json.loads(request.data)
    user_id=body.get("user_id")
    t=body.get("type")
    if user_id is None:
        return failure_response("User ID field empty", 400)
    if t is None:
        return failure_response("Type field empty", 400)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    #add user
    if t=="student":
        course.students.append(user)
    elif t=="instructor":
        course.instructors.append(user)
    else:
        return failure_response("Invalid Type field", 400)
    db.session.commit()
    return success_response(course.serialize())
    

@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def make_assignment(course_id):
    """
    Endpoint for creating an assignment for a course by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    body = json.loads(request.data)
    title=body.get("title")
    due_date=body.get("due_date")
    if title is None:
        return failure_response("Title field empty", 400)
    if due_date is None:
        return failure_response("Due Date field empty", 400)
    new_assignment = Assignment(
        title=title, 
        due_date=due_date, 
        course_id=course_id)
    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize(), 201)

@app.route("/api/courses/<int:course_id>/drop/", methods=["POST"])
def drop_user(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    body = json.loads(request.data)
    user_id = body.get("user_id")
    user = Course.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    #check user in lists
    if user in course.students:
        course.students.remove(user)
    elif user in course.instructors:
        course.instructors.remove(user)
    else:
        return failure_response("User has not been added to this course")
    db.session.commit()
    return success_response(user.serialize())
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
