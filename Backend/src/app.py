
from db import Notification
from db import db
from flask import Flask
from flask import request
import json
import os
from db import Availability
from db import Course
from db import User
from flask import Flask, redirect, request, url_for, Request
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin
)
from loguru import logger

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

@app.route("/api/courses/<int:code>/")
def get_course(code):
    """
    Endpoint for getting a course by code
    """
    course = Course.query.filter_by(code=code).first()
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())

@app.route("/api/notifications/")
def get_notifications():
    """
    Endpoint for getting all notifications.
    """
    return success_response({"notifications": [n.serialize for n in Notification.query.all()]})

@app.route("/api/notifications/<int:notification_id>/")
def get_notification(notification_id):
    """
    Endpoint for getting a notification.
    """
    noti = User.query.filter_by(id=notification_id).first()
    if noti is None:
        return failure_response("Notification not found")
    return success_response(noti.serialize())

@app.route("/api/notifications/", methods=["POST"])
def create_notifications():
    """
    Endpoint for creating a notification.
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    note = body.get("note")
    if note is None:
        return failure_response("Note field is empty.")
    new_noti = Notification(note=note,
    sender_id = sender_id,
    receiver_id = receiver_id)
    if sender_id is None and receiver_id is None:
        return failure_response("SENDER ID or RECEIVER ID is empty.")
    db.session.add(new_noti)
    db.session.commit()
    return success_response(new_noti.serialize(), 201)

@app.route("/api/users/notifications/<int:user_id>")
def get_notifications_for_user(user_id):
    """
    Endpoint for getting a specific users notifications
    """

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response({"notifications": [n.serialize for n in user.notifications]})


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def del_user(user_id):
    """
    Endpoint for deleting a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
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

@app.route("/users/current/")
def get_current_user():  
    if logged_in(current_user) == True:
        return success_response(current_user.serialize())
    else:
        return failure_response("User logged out")

@app.route("/api/users/<int:user_id>/availability/", methods = ["POST"])
def add_availablility(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    body = json.loads(request.data)
    time= body.get("time")
    if time == None:
        return failure_response("invalid request", 400)
    new_av = Availability(
        time = time,
        user_id = user_id
    )
    db.session.add(new_av)
    db.session.commit()

    return success_response(new_av.serialize_nc, 201)

def fill_courses():
    subjects = request.get("https://classes.cornell.edu/api/2.0/config/subjects.json?roster=SP22")
    course_codes = subjects.get("value")
    for code in course_codes:
        cs = request.get("https://classes.cornell.edu/api/2.0/search/classes.json?roster=FA14&subject=%s" % code)
        classnbr = cs.get("catalogNBR")
        new_course = Course(code = classnbr)
        db.session.add(new_course)




    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
