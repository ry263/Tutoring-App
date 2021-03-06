
import profile

from sqlalchemy import desc, null
from db import Notification
from db import db

from sqlalchemy import desc
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import json
import os
from db import Availability
from db import Course
from db import User
from flask import Flask, redirect, request, url_for, Request
from oauthlib.oauth2 import WebApplicationClient
import requests
import users_dao
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin
)

"""#from https://realpython.com/flask-google-login/#creating-your-own-web-application
class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["wsgi.url_scheme"] = "https"
        return self.app(environ, start_response)
#---------------------------------------------------------------------------------------------------------------------
"""
# define db filename
db_filename = "tutoring_app.db"
app = Flask(__name__)
#app.wsgi_app = ReverseProxied(app.wsgi_app)

app.secret_key = os.urandom(24)

# setup config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

"""#Google login
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
"""
"""#login manager to get current user
login_manager = LoginManager()
login_manager.init_app(app)
"""
# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()
"""
# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@login_manager.user_loader
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found')
    else:
        return user
"""


# your routes here
#DB = db.DatabaseDriver()

def success_response(data, code=200):
    return json.dumps(data), code
    #return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code
    #return json.dumps({"success": False, "error": message}), code

"""def logged_in(user):
    try:
        user.serialize()
        return True
    except AttributeError:
        return False
"""

"""#change after google server number
@app.route(("/"), methods=["POST"])
def login():
    #google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://34.130.13.109/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"] + " " + userinfo_response.json()["family_name"]
    else:
        return failure_response('Email not authenticated by Google')
    user = User.query.filter_by(id=unique_id).first()
    if user is None:
        user = User(id=unique_id, name=users_name, email=users_email, profile_pic=picture)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return success_response(user.serialize(), 201)
#-------------------------------------------------------------------------------------------------

@app.route("/logout/", methods=["GET"])
def logout():
    logout_user()
    return success_response("User logged out")
"""

def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return False,json.dumps({"Missing Authorization header"})

    bearer_token = auth_header.replace("Bearer", "").strip()

    return True, bearer_token

@app.route("/")
def hello():
    "lom4 was here"
    return ("lom4  was here") , 200


@app.route("/register/", methods=["POST"])
def register_account():
    """
    Endpoint for registering a new user
    """

    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")
    name = body.get("name")
    profile_pic = body.get("profile_pic")
    #if email is None or password is None or name is None:
       # return failure_response("missing email, name, or password")

    #was_successful, user = users_dao.create_user(name, email, password, profile_pic)
    user = User(name = name, email =email, password =password, profile_pic =profile_pic )
    #if not was_successful:
    db.session.add(user)
    db.session.commit()

        #return failure_response("user already exists")

    return success_response(user.serialize(),201)


@app.route("/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in a user
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    #if email is None or password is None:
        #return failure_response("missing email, or password")

    #was_successful, user = users_dao.verify_credentials(email, password)
    user = User.query.filter_by(email =email).first()
    

    if user == null or user.password_digest != password:
        return failure_response("Incorrect information")

    return success_response(user.serialize())


@app.route("/session/", methods=["POST"])
def update_session():
    """
    Endpoint for updating a user's session
    """
    was_successful, update_token = extract_token(request)

    if not was_successful:
        return update_token

    try:
        user = users_dao.renew_session(update_token)
    except Exception as e:
        return failure_response("Invalid Update token: {str(e)}" )

    return success_response(user.serialize_session())


@app.route("/secret/", methods=["GET"])
def secret_message():
    """
    Endpoint for verifying a session token and returning a secret message

    In your project, you will use the same logic for any endpoint that needs
    authentication
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid Session Token")

    return success_response(user.serialize_session())


@app.route("/users/current/")
def get_current_user():
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid Session Token")
    return success_response(user.serialize())


@app.route("/api/courses/")
def get_courses():
    """
    Endpoint for getting all courses
    """
    return success_response([c.serialize() for c in Course.query.all()])
    
@app.route("/api/courses/", methods=["POST"])
def make_course():
    """
    Endpoint for creating a course
    """
    body = json.loads(request.data)
    code=body.get("code")
    if code is None:
        return failure_response("Code field empty", 400)
    new_course = Course(code=code)
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)

@app.route("/api/courses/<string:code>/")
def get_course(code):
    """
    Endpoint for getting a course by code
    """

    parsed_code = code[:-4] + " " + code[-4:]
    course = Course.query.filter_by(code=parsed_code).first()
    
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())

@app.route("/api/courses/users/<string:code>/")
def get_tutors_for_course(code):
    """
    Endpoint for getting tutors by course code
    """

    parsed_code = code[:-4] + " " + code[-4:]
    course = Course.query.filter_by(code=parsed_code).first()
    
    if course is None:
        return failure_response("Course not found")
    
    return success_response([tutor.serialize() for tutor in course.tutors]) 



@app.route("/api/notifications/")
def get_notifications():
    """
    Endpoint for getting all notifications.
    """
    return success_response([n.serialize() for n in Notification.query.all()])

@app.route("/api/notifications/<int:notification_id>/")
def get_notification(notification_id):
    """
    Endpoint for getting a notification.
    """
    noti = Notification.query.filter_by(id=notification_id).first()
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
    new_noti = Notification(
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
    notifications = Notification.query.filter_by(receiver_id=user_id).order_by(desc(Notification.time)).all()
    return success_response([n.serialize() for n in notifications])

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
    if user_id is None:
        return failure_response("User ID field empty", 400)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    #add user   
    course.tutors.append(user)
    db.session.commit()
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/drop/", methods=["POST"])
def drop_user(course_id):
    """
    Endpoint for removing user from course
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    body = json.loads(request.data)
    user_id = body.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    #check user in lists

    if user in course.tutors:
        course.tutors.remove(user)
    else:
        return failure_response("User has not been added to this course")
    db.session.commit()
    return success_response(user.serialize())
"""
@app.route("/users/current/")
def get_current_user():  
    
    if logged_in(current_user) == True:
        return success_response(current_user.serialize())
    else:
        return failure_response("User logged out")
"""
@app.route("/api/users/<int:user_id>/availability/", methods = ["POST"])
def add_availablility(user_id):
    """
    Endpoint for adding availability
    """
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
    return success_response(new_av.serialize(), 201)

@app.route("/api/allcourses/", methods=["POST"])
def fill_courses():
    """
    Endpoint for filling courses
    """
    subjects = requests.get("https://classes.cornell.edu/api/2.0/config/subjects.json?roster=SP22")
    subjects = subjects.json()
    courses = subjects.get("data")
    course_code = courses.get("subjects")
    for x in course_code:
        r = x.get("value")
        cs = requests.get("https://classes.cornell.edu/api/2.0/search/classes.json?roster=SP22&subject="+ r)
        cs = cs.json()
        data = cs.get("data")
        classnbr = data.get("classes")
        for num in classnbr:
            numero = num.get("catalogNbr")
            new_course = Course(code = r + " " + numero)
            db.session.add(new_course)
    db.session.commit()   
    return success_response([c.serialize() for c in Course.query.all()])

@app.route("/api/rate/<int:user_id>/", methods =["POST"])
def add_rate(user_id):
    """
    Endpoint for changing rate
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    body = json.loads(request.data)
    rate  = body.get("rate")
    if rate == None:
        return failure_response("invalid rate", 400)
    user.rate = rate
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/availability/<int:av_id>/", methods = ["DELETE"])
def delete_availability(user_id,av_id):
    """
    Endpoint for deleting availability
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    for n in user.availability:
        old_av = n.query.filter_by(id = av_id).first()
    db.session.delete(old_av)
    db.session.commit()
    return success_response(old_av.serialize())
    

    

    



    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
