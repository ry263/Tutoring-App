import json
import sys
from threading import Thread
from time import sleep
import unittest

from app import app
import requests

# NOTE: Make sure you run 'pip3 install requests' in your virtualenv

# Flag to run extra credit tests (if applicable)
EXTRA_CREDIT = False

# URL pointing to your local dev host
LOCAL_URL = "http://localhost:5000"

# Sample request bodies
SAMPLE_COURSE = {"code": "CS 1998", "name": "Intro to Backend Development"}
BAD_COURSE = {"name": "Intro to Backend Development"}
SAMPLE_USER = {"name": "Cornell AppDev", "netid": "cad2014"}
BAD_USER = {"name": "Cornell AppDev"}
SAMPLE_ASSIGNMENT = {"title": "PA4", "due_date": 1554076799}
BAD_ASSIGNMENT = {}


# Request endpoint generators
def gen_users_route(user_id=None):
    base_path = "/api/users"
    return (
        f"{base_path}/"
        if user_id is None
        else f"{base_path}/{str(user_id)}/"
    )

def gen_users_path(user_id=None):
    return f"{LOCAL_URL}{gen_users_route(user_id)}"

def gen_courses_route(course_id=None):
    base_path = "/api/courses"
    return (
        base_path + "/"
        if course_id is None
        else f"{base_path}/{str(course_id)}/"
    )

def gen_courses_path(course_id=None):
    return f"{LOCAL_URL}{gen_courses_route(course_id)}"

def gen_assignments_route(assignment_id=None):
    base_path = "/api/assignments"
    return (
        base_path + "/"
        if assignment_id is None
        else f"{base_path}/{str(assignment_id)}/"
    )

def gen_assignments_path(assignment_id=None):
    return f"{LOCAL_URL}{gen_assignments_route(assignment_id)}"


# Error Handlers
def error_str(str):
    return f"\033[91m{str}\033[0m"


def is_jsonable(res, req_type, route, body=None):
    postfix = "" if body is None else f"\n\nRequest Body:\n{body}"
    try:
        res.json().get("test")
        return True, ""
    except json.decoder.JSONDecodeError:
        err = f"\n{req_type} request to route '{route}' did not return a JSON response.\
            \nAre you sure you spelled the route correctly?\
            \nIs there an error in the route handling?\
            \nDid you remember to use json.dumps() on your response?\
            \nAre you accidentally returning a list/tuple instead of a dictionary?"
        err += postfix
        return False, error_str(err)
    except AttributeError:
        err = f"\n{req_type} request to route '{route}' did not return a dictionary response.\
            \nAre you accidentally returning a tuple or a list?\
            \nAre you accidentally returning nothing?"
        err += postfix
        return False, error_str(err)


def status_code_error(req_type, route, res_code, expected_code, body=None):
    err = f"\n{req_type} request to route '{route}' returned a status code of {res_code}, but {expected_code} was expected."
    return error_str(err)


def wrong_value_error(
    req_type, route, res_val, expected_val, value_name, body=None
):
    err = f"\n{req_type} request to route '{route}' returned an incorrect response of:\n{res_val}\nwhen we expected\n{expected_val}\nfor {value_name} value."
    return error_str(err)


class TestRoutes(unittest.TestCase):
    def jsonable_test(self, res, req_type, route, status_code, body=None):
        jsonable, error = is_jsonable(res, req_type, route, body)
        self.assertTrue(jsonable, error)
        self.assertEqual(
            res.status_code,
            status_code,
            status_code_error(req_type, route, res.status_code, status_code),
        )

    def test_get_initial_courses(self):
        req_type = "GET"
        route = gen_courses_route()
        res = requests.get(gen_courses_path())
        self.jsonable_test(res, req_type, route, 200)

        courses = res.json().get("courses")
        self.assertEqual(
            type(courses),
            list,
            wrong_value_error(
                req_type, route, type(courses), list, "type of courses field"
            ),
        )

    def test_create_course(self):
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        self.jsonable_test(res, req_type, route, 201, SAMPLE_COURSE)
        course = res.json()
        for key in SAMPLE_COURSE.keys():
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type,
                    route,
                    course.get(key),
                    SAMPLE_COURSE[key],
                    key,
                    SAMPLE_COURSE,
                ),
            )
        self.assertEqual(
            type(course.get("assignments")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("assignments")), list, "type of assignments field"
            ),
        )
        self.assertEqual(
            type(course.get("instructors")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("instructors")), list, "type of instructors field"
            ),
        )
        self.assertEqual(
            type(course.get("students")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("students")), list, "type of students field"
            ),
        )

    def test_create_bad_course(self):
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(BAD_COURSE))
        self.jsonable_test(res, req_type, route, 400, BAD_COURSE)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_get_course(self):
        req_type = "GET"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        self.jsonable_test(res, req_type, route, 201, SAMPLE_COURSE)

        course_id = res.json()["id"]

        res2 = requests.get(gen_courses_path(course_id))
        self.jsonable_test(res2, req_type, route, 200, SAMPLE_COURSE)
        course = res2.json()
        for key in SAMPLE_COURSE.keys():
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type,
                    route,
                    course.get(key),
                    SAMPLE_COURSE[key],
                    key,
                    SAMPLE_COURSE,
                ),
            )
        self.assertEqual(
            type(course.get("assignments")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("assignments")), list, "type of assignments field"
            ),
        )
        self.assertEqual(
            type(course.get("instructors")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("instructors")), list, "type of instructors field"
            ),
        )
        self.assertEqual(
            type(course.get("students")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("students")), list, "type of students field"
            ),
        )


    def test_delete_course(self):
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )

        course_id = course["id"]
        req_type = "DELETE"
        route = gen_courses_path(course_id)
        res2 = requests.delete(gen_courses_path(course_id))
        self.jsonable_test(res2, req_type, route, 200)
        course = res2.json()
        for key in SAMPLE_COURSE:
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type, route, course.get(key), SAMPLE_COURSE[key], key
                ),
            )
        self.assertEqual(
            type(course.get("assignments")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("assignments")), list, "type of assignments field"
            ),
        )
        self.assertEqual(
            type(course.get("instructors")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("instructors")), list, "type of instructors field"
            ),
        )
        self.assertEqual(
            type(course.get("students")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("students")), list, "type of students field"
            ),
        )

        req_type = "GET"
        route = gen_courses_path(course_id)
        res = requests.get(gen_users_path(course_id))
        jsonable, error = is_jsonable(res, req_type, route)
        self.assertTrue(
            jsonable,
            error_str(
                "Getting a course by ID did not return a json response. See test_get_course for details."
            ),
        )
        self.assertEqual(
            res.status_code,
            404,
            error_str(
                "Trying to get a deleted course did not return a 404 status code."
            ),
        )

    def test_create_user(self):
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        self.jsonable_test(res, req_type, route, 201, SAMPLE_USER)
        user = res.json()
        for key in SAMPLE_USER.keys():
            self.assertEqual(
                user.get(key),
                SAMPLE_USER[key],
                wrong_value_error(
                    req_type,
                    route,
                    user.get(key),
                    SAMPLE_USER[key],
                    key,
                    SAMPLE_USER,
                ),
            )
        self.assertEqual(
            type(user.get("courses")),
            list,
            wrong_value_error(
                req_type, route, type(user.get("courses")), list, "type of courses field"
            ),
        )

    def test_create_bad_user(self):
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(BAD_USER))
        self.jsonable_test(res, req_type, route, 400, BAD_USER)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_get_user(self):
        req_type = "GET"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        self.jsonable_test(res, req_type, route, 201, SAMPLE_USER)

        user_id = res.json()["id"]
        res2 = requests.get(gen_users_path(user_id))
        self.jsonable_test(res2, req_type, route, 200, SAMPLE_USER)
        user = res2.json()
        for key in SAMPLE_USER.keys():
            self.assertEqual(
                user.get(key),
                SAMPLE_USER[key],
                wrong_value_error(
                    req_type,
                    route,
                    user.get(key),
                    SAMPLE_USER[key],
                    key,
                    SAMPLE_USER,
                ),
            )
        self.assertEqual(
            type(user.get("courses")),
            list,
            wrong_value_error(
                req_type, route, type(user.get("courses")), list, "type of courses field"
            ),
        )

    def test_add_student_to_course(self):
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]

        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]

        add_user_body = {"type": "student", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        self.jsonable_test(res, req_type, route, 200)
        course = res.json()
        for key in SAMPLE_COURSE:
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type, route, course.get(key), SAMPLE_COURSE[key], key
                ),
            )
        self.assertEqual(
            type(course.get("assignments")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("assignments")), list, "type of assignments field"
            ),
        )
        self.assertEqual(
            type(course.get("instructors")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("instructors")), list, "type of instructors field"
            ),
        )
        self.assertEqual(
            len(course.get("students")),
            1,
            wrong_value_error(
                req_type, route, len(course.get("students")), 1, "length of students field"
            ),
        )
        for student in course.get("students"):
            for key in SAMPLE_USER:
                self.assertEqual(
                    student.get(key),
                    SAMPLE_USER[key],
                    wrong_value_error(
                        req_type, route, course.get(key), SAMPLE_USER[key], key
                    ),
                )
            self.assertEqual(
                student.get("id"),
                user_id,
                wrong_value_error(
                    req_type, route, student.get("id"), user_id, "student id"
                ),
            )
            self.assertEqual(
                student.get("courses"),
                None,
                wrong_value_error(
                    req_type, route, student.get("courses"), None, "type of courses field"
                ),
            )

        req_type = "GET"
        route = gen_courses_route()
        res = requests.get(gen_courses_path(course_id))
        self.jsonable_test(res, req_type, route, 200)
        course = res.json()
        for key in SAMPLE_COURSE:
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type, route, course.get(key), SAMPLE_COURSE[key], key
                ),
            )
        self.assertEqual(
            type(course.get("assignments")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("assignments")), list, "type of assignments field"
            ),
        )
        self.assertEqual(
            type(course.get("instructors")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("instructors")), list, "type of instructors field"
            ),
        )
        self.assertEqual(
            len(course.get("students")),
            1,
            wrong_value_error(
                req_type, route, len(course.get("students")), 1, "length of students list"
            ),
        )
        for student in course.get("students"):
            for key in SAMPLE_USER:
                self.assertEqual(
                    student.get(key),
                    SAMPLE_USER[key],
                    wrong_value_error(
                        req_type, route, course.get(key), SAMPLE_USER[key], key
                    ),
                )
            self.assertEqual(
                student.get("id"),
                user_id,
                wrong_value_error(
                    req_type, route, student.get("id"), user_id, "student id"
                ),
            )
            self.assertEqual(
                student.get("courses"),
                None,
                wrong_value_error(
                    req_type, route, student.get("courses"), None, "type of courses field"
                ),
            )

        req_type = "GET"
        res = requests.get(gen_users_path(user_id))
        self.jsonable_test(res, req_type, route, 200, SAMPLE_USER)
        user = res.json()
        self.assertEqual(
            len(user.get("courses")),
            1,
            wrong_value_error(
                req_type, route, len(user.get("courses")), 1, "length of courses list"
            ),
        )
        for course in user.get("courses"):
            for key in SAMPLE_COURSE:
                self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type,
                    route,
                    user.get(key),
                    SAMPLE_COURSE[key],
                    key,
                    SAMPLE_COURSE,
                ),
            )
            self.assertEqual(
                course.get("assignments"),
                None,
                wrong_value_error(
                    req_type, route, course.get("assignments"), None, "type of assignments field"
                ),
            )
            self.assertEqual(
                course.get("students"),
                None,
                wrong_value_error(
                    req_type, route, course.get("students"), None, "type of students field"
                ),
            )
            self.assertEqual(
                course.get("instructors"),
                None,
                wrong_value_error(
                    req_type, route, course.get("instructors"), None, "type of instructors field"
                ),
            )



    def test_add_instructor_to_course(self):
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]

        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]

        add_user_body = {"type": "instructor", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        self.jsonable_test(res, req_type, route, 200)
        course = res.json()
        for key in SAMPLE_COURSE:
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type, route, course.get(key), SAMPLE_COURSE[key], key
                ),
            )
        self.assertEqual(
            type(course.get("assignments")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("assignments")), list, "type of assignments field"
            ),
        )
        self.assertEqual(
            type(course.get("students")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("students")), list, "type of instructors field"
            ),
        )
        self.assertEqual(
            len(course.get("instructors")),
            1,
            wrong_value_error(
                req_type, route, len(course.get("instructors")), 1, "length of students list"
            ),
        )
        for instructor in course.get("instructors"):
            for key in SAMPLE_USER:
                self.assertEqual(
                    instructor.get(key),
                    SAMPLE_USER[key],
                    wrong_value_error(
                        req_type, route, course.get(key), SAMPLE_USER[key], key
                    ),
                )
            self.assertEqual(
                instructor.get("id"),
                user_id,
                wrong_value_error(
                    req_type, route, instructor.get("id"), user_id, "instructor id"
                ),
            )
            self.assertEqual(
                instructor.get("courses"),
                None,
                wrong_value_error(
                    req_type, route, instructor.get("courses"), None, "type of courses field"
                ),
            )

        req_type = "GET"
        route = gen_courses_route()
        res = requests.get(gen_courses_path(course_id))
        self.jsonable_test(res, req_type, route, 200)
        course = res.json()
        for key in SAMPLE_COURSE:
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type, route, course.get(key), SAMPLE_COURSE[key], key
                ),
            )
        self.assertEqual(
            type(course.get("assignments")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("assignments")), list, "type of assignments field"
            ),
        )
        self.assertEqual(
            type(course.get("students")),
            list,
            wrong_value_error(
                req_type, route, type(course.get("students")), list, "type of students field"
            ),
        )
        self.assertEqual(
            len(course.get("instructors")),
            1,
            wrong_value_error(
                req_type, route, len(course.get("instructors")), 1, "length of instructors field"
            ),
        )
        for instructor in course.get("instructors"):
            for key in SAMPLE_USER:
                self.assertEqual(
                    instructor.get(key),
                    SAMPLE_USER[key],
                    wrong_value_error(
                        req_type, route, course.get(key), SAMPLE_USER[key], key
                    ),
                )
            self.assertEqual(
                instructor.get("id"),
                user_id,
                wrong_value_error(
                    req_type, route, instructor.get("id"), user_id, "instructor id"
                ),
            )
            self.assertEqual(
                instructor.get("courses"),
                None,
                wrong_value_error(
                    req_type, route, instructor.get("courses"), None, "type of courses field"
                ),
            )

        req_type = "GET"
        res = requests.get(gen_users_path(user_id))
        self.jsonable_test(res, req_type, route, 200, SAMPLE_USER)
        user = res.json()
        self.assertEqual(
            len(user.get("courses")),
            1,
            wrong_value_error(
                req_type, route, len(user.get("courses")), 1, "length of courses list"
            ),
        )
        for course in user.get("courses"):
            for key in SAMPLE_COURSE:
                self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type,
                    route,
                    user.get(key),
                    SAMPLE_COURSE[key],
                    key,
                    SAMPLE_COURSE,
                ),
            )
            self.assertEqual(
                course.get("assignments"),
                None,
                wrong_value_error(
                    req_type, route, course.get("assignments"), None, "type of assignments field"
                ),
            )
            self.assertEqual(
                course.get("students"),
                None,
                wrong_value_error(
                    req_type, route, course.get("students"), None, "type of students field"
                ),
            )
            self.assertEqual(
                course.get("instructors"),
                None,
                wrong_value_error(
                    req_type, route, course.get("instructors"), None, "type of instructors field"
                ),
            )


    def test_create_assignment_for_course(self):
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]

        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        assignment_id = assignment["id"]
        for key in SAMPLE_ASSIGNMENT:
            self.assertEqual(
                assignment.get(key),
                SAMPLE_ASSIGNMENT[key],
                wrong_value_error(
                    req_type, route, assignment.get(key), SAMPLE_ASSIGNMENT[key], key, SAMPLE_ASSIGNMENT
                )
            )
        course = assignment["course"]
        for key in SAMPLE_COURSE:
            self.assertEqual(
                course.get(key),
                SAMPLE_COURSE[key],
                wrong_value_error(
                    req_type, route, course.get(key), SAMPLE_COURSE[key], key
                )
            )
        self.assertEqual(
            course.get("id"),
            course_id,
            wrong_value_error(
                req_type, route, course.get("id"), course_id, "id"
            )
        )
        
        req_type = "GET"
        route = gen_courses_route(course_id)
        res = requests.get(gen_courses_path(course_id))
        course = res.json()
        self.assertEqual(
            len(course.get("assignments")),
            1,
            wrong_value_error(
                req_type, route, len(course.get("assignments")), 1, "length of assignments list"
            ),
        )
        assignment = course.get("assignments")[0]
        for key in SAMPLE_ASSIGNMENT:
            self.assertEqual(
                assignment.get(key),
                SAMPLE_ASSIGNMENT[key],
                wrong_value_error(
                    req_type, route, assignment.get(key), SAMPLE_ASSIGNMENT[key], key
                )
            )
        self.assertEqual(
            assignment.get("course"),
            None,
            wrong_value_error(
                req_type, route, assignment.get("course"), None, "assignment course field"
            )
        )
        self.assertEqual(
            assignment.get("id"),
            assignment_id,
            wrong_value_error(
                req_type, route, assignment.get("id"), assignment_id, "id"
            )
        )

    def test_create_bad_assignment_for_course(self):
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]

        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(BAD_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 400, BAD_ASSIGNMENT)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_get_invalid_course(self):
        req_type = "GET"
        route = gen_courses_route(1000)
        res = requests.get(gen_courses_path(1000))
        self.jsonable_test(res, req_type, route, 404)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_get_invalid_user(self):
       req_type = "GET"
       route = gen_users_route(1000)
       res = requests.get(gen_users_path(1000))
       self.jsonable_test(res, req_type, route, 404)
       self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_add_user_invalid_course(self):
        req_type = "POST"
        route = gen_courses_route(1000) + "add/"
        add_user_body = {"type": "instructor", "user_id": 0}
        res = requests.post(
            gen_courses_path(1000) + "add/", data=json.dumps(add_user_body)
        )
        self.jsonable_test(res, req_type, route, 404)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_create_assignment_invalid_course(self):
        req_type = "GET"
        route = gen_courses_route(1000) + "assignment/"
        res = requests.post(
            gen_courses_path(1000) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 404)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_extra_drop_course(self):
        if not EXTRA_CREDIT:
            return
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]


        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]


        add_user_body = {"type": "student", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        

        route = gen_courses_route(course_id) + "drop/"
        drop_user_body = {"user_id": user_id}
        res = requests.post(
            gen_courses_path(course_id) + "drop/", data=json.dumps(drop_user_body)
        )
        self.jsonable_test(res, req_type, route, 200, drop_user_body)
        student = res.json()
        for key in SAMPLE_USER:
            self.assertEqual(
                student.get(key),
                SAMPLE_USER[key],
                wrong_value_error(
                    req_type, route, student.get(key), SAMPLE_USER[key], key
                )
            )
        self.assertEqual(
            len(student.get("courses")),
            0,
            wrong_value_error(
                req_type, route, len(student.get("courses")), 0, "length of courses filed"
            )
        )

        req_type = "GET"
        res = requests.get(gen_users_path(user_id))
        self.jsonable_test(res, req_type, route, 200, SAMPLE_USER)
        user = res.json()
        for key in SAMPLE_USER.keys():
            self.assertEqual(
                user.get(key),
                SAMPLE_USER[key],
                wrong_value_error(
                    req_type,
                    route,
                    user.get(key),
                    SAMPLE_USER[key],
                    key,
                    SAMPLE_USER,
                ),
            )
        self.assertEqual(
            len(user.get("courses")),
            0,
            wrong_value_error(
                req_type, route, len(user.get("courses")), 0, "length of courses field"
            ),
        )

    def test_extra_drop_invalid_course(self):
        if not EXTRA_CREDIT:
            return
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]

        route = gen_courses_route(1000) + "drop/"
        drop_user_body = {"user_id": user_id}
        res = requests.post(
            gen_courses_path(user_id) + "drop/", data=json.dumps(drop_user_body)
        )
        self.jsonable_test(res, req_type, route, 404, drop_user_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_extra_drop_invalid_user(self):
        if not EXTRA_CREDIT:
            return
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]

        route = gen_courses_route(course_id) + "drop/"
        drop_user_body = {"user_id": 1000}
        res = requests.post(
            gen_courses_path(course_id) + "drop/", data=json.dumps(drop_user_body)
        )
        self.jsonable_test(res, req_type, route, 404, drop_user_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def test_extra_drop_user_not_in_course(self):
        if not EXTRA_CREDIT:
            return
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]


        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]

        route = gen_courses_route(course_id) + "drop/"
        drop_user_body = {"user_id": user_id}
        res = requests.post(
            gen_courses_path(course_id) + "drop/", data=json.dumps(drop_user_body)
        )
        self.jsonable_test(res, req_type, route, 404, drop_user_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))

    def text_extra_update_assignment(self):
        if not EXTRA_CREDIT:
            return
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]


        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        assignment_id = assignment["id"]

        route = gen_assignments_route(assignment_id)
        update_assignment_body = {"title": "PA4 - CMS", "due_date": 1648093695}
        res = requests.post(gen_assignments_path(assignment_id), data=json.dumps(update_assignment_body))
        self.jsonable_test(res, req_type, route, 200, update_assignment_body)
        assignment = res.json()
        for key in update_assignment_body:
            self.assertEqual(
                assignment.get(key),
                update_assignment_body["key"],
                wrong_value_error(
                    req_type, route, assignment.get(key), update_assignment_body["key"], key
                )
            )

        req_type = "GET"
        route = gen_courses_route(course_id)
        res = requests.get(gen_courses_path(course_id))
        course = res.json()
        self.assertEqual(
            len(course.get("assignments")),
            1,
            wrong_value_error(
                req_type, route, len(course.get("assignments")), 1, "length of assignments list"
            ),
        )
        assignment = course.get("assignments")[0]
        for key in update_assignment_body:
            self.assertEqual(
                assignment.get(key),
                update_assignment_body[key],
                wrong_value_error(
                    req_type, route, assignment.get(key), update_assignment_body[key], key
                )
            )

    def test_extra_update_invalid_assignment(self):
        if not EXTRA_CREDIT:
            return
        req_type = "POST"
        route = gen_assignments_route(1000)
        update_assignment_body = {"title": "PA4 - CMS", "due_date": 1648093695}
        res = requests.post(gen_assignments_path(1000), data=json.dumps(update_assignment_body))
        self.jsonable_test(res, req_type, route, 404, update_assignment_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))
    
    def test_extra_submit(self):
        if not EXTRA_CREDIT:
            return
        # create user
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]
        # create course
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]
        # create assignment for course
        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        assignment_id = assignment["id"]
        # add student to course
        add_user_body = {"type": "student", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        # submit + check response
        route = gen_assignments_route(assignment_id) + "submit/"
        submission_body = {"user_id": user_id, "content": "my assignment"}
        res = requests.post(gen_assignments_path(assignment_id) + "submit/", data = json.dumps(submission_body))
        self.jsonable_test(res, req_type, route, 201, submission_body)
        submission = res.json()
        self.assertEqual(
            submission.get("content"),
            submission_body["content"],
            wrong_value_error(
                req_type, route, submission.get("content"), submission_body["content"], "content"
            )
        )

    def test_extra_submit_invalid_assignment(self):
        if not EXTRA_CREDIT:
            return
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]

        route = gen_assignments_route(1000) + "submit/"
        submission_body = {"user_id": user_id, "content": "my assignment"}
        res = requests.post(gen_assignments_path(1000) + "submit/", data = json.dumps(submission_body))
        self.jsonable_test(res, req_type, route, 404, submission_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))
    
    def test_extra_submit_invalid_user(self):
        if not EXTRA_CREDIT:
            return
         # create course
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]
        # create assignment for course
        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        assignment_id = assignment["id"]
        # submit + check response
        route = gen_assignments_route(assignment_id) + "submit/"
        submission_body = {"user_id": 1000, "content": "my assignment"}
        res = requests.post(gen_assignments_path(assignment_id) + "submit/", data = json.dumps(submission_body))
        self.jsonable_test(res, req_type, route, 404, submission_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))


    def test_extra_submit_invalid_assignment_for_user(self):
        if not EXTRA_CREDIT:
            return
        # create user
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]
        # create course
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]
        # create assignment for course
        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        assignment_id = assignment["id"]
        # submit + check response
        route = gen_assignments_route(assignment_id) + "submit/"
        submission_body = {"user_id": user_id, "content": "my assignment"}
        res = requests.post(gen_assignments_path(assignment_id) + "submit/", data = json.dumps(submission_body))
        self.jsonable_test(res, req_type, route, 404, submission_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))
    
    def test_extra_grade(self):
        if not EXTRA_CREDIT:
            return
        # create user
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]
        # create course
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]
        # create assignment for course
        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        assignment_id = assignment["id"]
        # add student to course
        add_user_body = {"type": "student", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        # submit
        route = gen_assignments_route(assignment_id) + "submit/"
        submission_body = {"user_id": user_id, "content": "my assignment"}
        res = requests.post(gen_assignments_path(assignment_id) + "submit/", data = json.dumps(submission_body))
        submission_id = res.json()["id"]
        # grade + check response
        route = gen_assignments_route(assignment_id) + "grade/"
        grade_body = {"submission_id": submission_id, "score": 100}
        res = requests.post(gen_assignments_path(assignment_id) + "grade/", data = json.dumps(grade_body))
        self.jsonable_test(res, req_type, route, 200, grade_body)
        submission = res.json()
        self.assertEqual(
            submission.get("score"),
            grade_body["score"],
            wrong_value_error(
                req_type, route, submission.get("score"), grade_body["score"], "score"
            )
        )

    def test_grade_invalid_assignment(self):
        if not EXTRA_CREDIT:
            return
        # create user
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]
        # create course
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]
        # add student to course
        add_user_body = {"type": "student", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        # grade + check response
        route = gen_assignments_route(1000) + "grade/"
        grade_body = {"submission_id": 1, "score": 100}
        res = requests.post(gen_assignments_path(1000) + "grade/", data = json.dumps(grade_body))
        self.jsonable_test(res, req_type, route, 404, grade_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))
        

    def test_grade_invalid_submission(self):
        if not EXTRA_CREDIT:
            return
        # create user
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]
        # create course
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]
        # create assignment 
        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        assignment_id = assignment["id"]
        # add student to course
        add_user_body = {"type": "student", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        # grade + check response
        route = gen_assignments_route(assignment_id) + "grade/"
        grade_body = {"submission_id": 1000, "score": 100}
        res = requests.post(gen_assignments_path(assignment_id) + "grade/", data = json.dumps(grade_body))
        self.jsonable_test(res, req_type, route, 404, grade_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))
        

    def test_grade_wrong_submission_assignment(self):
        if not EXTRA_CREDIT:
            return
        # create user
        req_type = "POST"
        route = gen_users_route()
        res = requests.post(gen_users_path(), data=json.dumps(SAMPLE_USER))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_USER)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a user did not return a json response. See test_create_user for details."
            ),
        )
        user = res.json()
        self.assertTrue(
            user.get("id") is not None,
            error_str(
                "Returned user from POST to /api/users/ has no 'id' field!"
            ),
        )
        user_id = user["id"]
        # create course
        req_type = "POST"
        route = gen_courses_route()
        res = requests.post(gen_courses_path(), data=json.dumps(SAMPLE_COURSE))
        jsonable, error = is_jsonable(res, req_type, route, SAMPLE_COURSE)
        self.assertTrue(
            jsonable,
            error_str(
                "Creating a course did not return a json response. See test_create_course for details."
            ),
        )
        course = res.json()
        self.assertTrue(
            course.get("id") is not None,
            error_str(
                "Returned course from POST to /api/courses/ has no 'id' field!"
            ),
        )
        course_id = course["id"]
        # create wrong assignment 
        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        wrong_assignment_id = assignment["id"]
        # create right assignment
        req_type = "POST"
        route = gen_courses_route(course_id)
        res = requests.post(
            gen_courses_path(course_id) + "assignment/",
            data=json.dumps(SAMPLE_ASSIGNMENT),
        )
        self.jsonable_test(res, req_type, route, 201, SAMPLE_ASSIGNMENT)
        assignment = res.json()
        right_assignment_id = assignment["id"]
        # add student to course
        add_user_body = {"type": "student", "user_id": user_id}
        route = gen_courses_route(course_id) + "add/"
        res = requests.post(
            gen_courses_path(course_id) + "add/", data=json.dumps(add_user_body)
        )
        # submit
        route = gen_assignments_route(right_assignment_id) + "submit/"
        submission_body = {"user_id": user_id, "content": "my assignment"}
        res = requests.post(gen_assignments_path(right_assignment_id) + "submit/", data = json.dumps(submission_body))
        submission_id = res.json()["id"]
        # grade + check response
        route = gen_assignments_route(wrong_assignment_id) + "grade/"
        grade_body = {"submission_id": submission_id, "score": 100}
        res = requests.post(gen_assignments_path(wrong_assignment_id) + "grade/", data = json.dumps(grade_body))
        self.jsonable_test(res, req_type, route, 404, grade_body)
        self.assertIsNotNone(res.json()["error"], wrong_value_error(req_type, route, res.json()["error"], str, "error", "type of error field"))


def run_tests():
    sleep(1.5)
    sys.argv = sys.argv[:1]
    unittest.main()


if __name__ == "__main__":
    argv = sys.argv[1:]
    EXTRA_CREDIT = len(argv) > 0 and argv[0] == "--extra"
    thread = Thread(target=run_tests)
    thread.start()
    app.run(host="0.0.0.0", port=5000, debug=False)