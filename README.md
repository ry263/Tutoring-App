# Tutoring-App



## Backend API Specification
### Authentication Functions
#### Register new user
```POST /register/```
```
Request
{
    "email": <USER INPUT>,
    "password": <USER INPUT>,
    "name": <USER INPUT>,
    "profile pic": <USER INPUT>
}
```
```
Response
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "name": <NAME FROM USER INPUT>,
    "email": <EMAIL FROM USER INPUT>,
    "profile_pic": <PROFILE PIC FROM USER INPUT>,
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
    "session_token": User Session Token,
    "session_expiration": User Session Expiration,
    "update_token": User Update Token
}
```
#### Login
```POST /login/```
```
Request
{
    "email": <USER INPUT>,
    "password": <USER INPUT>
}
```
```
Response
<HTTP STATUS CODE 200>
{
    "session_token": User Session Token,
    "session_expiration": User Session Expiration,
    "update_token": User Update Token
}
```
#### Update session
```POST /session/```
```
Request
{
    <UPDATE TOKEN IN HEADER> 
}
```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "email": "ry263@cornell.edu",
    "profile_pic": "url for profile pic",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
    "session_token": New User Session Token,
    "session_expiration": New User Session Expiration,
    "update_token": New User Update Token
}
```
#### Verify session
```POST /secret/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "email": "ry263@cornell.edu",
    "profile_pic": "url for profile pic",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
    "session_token": New User Session Token,
    "session_expiration": New User Session Expiration,
    "update_token": New User Update Token
}
```

###  User Functions
#### Get all users
```GET /api/users/```
```
Response
<HTTP STATUS CODE 200>
{
    "users" : [
        {
            "id": 1,
            "name": "Rachel Yue",
            "email": "ry263@cornell.edu",
            "profile_pic": "url for profile pic",
            "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
            "availability": [ <SERIALIZED TIMES>, ... ],
            "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
            "rate": "20 per hour"
        },
        {
            "id": 2,
            "name": "Luk Man",
            "email": "ry263@cornell.edu",
            "profile_pic": "url for profile pic",
            "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
            "availability": [ <SERIALIZED TIMES>, ... ],
            "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
            "rate": "20 per hour"
        }
    ]
}
```

#### Get current user
```GET /api/users/current/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "email": "ry263@cornell.edu",
    "profile_pic": "url for profile pic",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

#### Get specific user
```GET /api/users/{user_id}/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "email": "ry263@cornell.edu",
    "profile_pic": "url for profile pic",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

#### Delete user
```DELETE /api/users/{user_id}/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "email": "ry263@cornell.edu",
    "profile_pic": "url for profile pic",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```
### Availability Functions
#### Add availability
```POST /api/users/{user_id}/availability/```
```
Request
<HTTP STATUS CODE 201>
{
    "time": <USER INPUT>
}
```
```
Response
<HTTP STATUS CODE 201>
{
    "time": <USER INPUT>
}
```

###  Course Functions
#### Get all Courses
```GET /api/courses/```
```
Response
<HTTP STATUS CODE 200>
{
    "courses" : [
        {
            "id": 1,
            "code": "CS 1110",
            "tutors": [<SERIALIZED USERS WITHOUT COURSES>, ...]
        },
        {
            "id": 2,
            "code": "CS 2110",
            "tutors": [<SERIALIZED USERS WITHOUT COURSES>, ...]
        }
    ]
}
```
#### Get course by code
```GET /api/courses/{string(code)}```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "code": "CS 1110",
    "tutors": [<SERIALIZED USERS WITHOUT COURSES>, ...]
}
```

###  Notification Functions
#### Get all notifications
```GET /api/notifications/```
```
Response
<HTTP STATUS CODE 200>
{
    "courses" : [
        {
            "id": 1,
            "sender_id": 3,
            "receiver_id": 1
        },
        {
            "id": 2,
            "sender_id": 3,
            "receiver_id": 2
        }
    ]
}
```

#### Get notification by id
```GET /api/notifications/{notification_id}/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "sender_id": 3,
    "receiver_id": 1,
    "time": "<TIME OF NOTIFICATION>"
}
```

#### Create notification
```POST /api/notifications/```
```
Request
{
    "sender_id": <USER INPUT>,
    "receiver_id": <USER INPUT>,
    "time": "<TIME OF NOTIFICATION>"
}
```
```
Response
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "sender_id": <USER INPUT FOR SENDER ID>,
    "receiver_id": <USER INPUT FOR RECEIVER ID>,
    "time": "<TIME OF NOTIFICATION>"
}
```

### Get Notifications for a specific user 
```GET /api/users/notifications/{user_id}/```
```
Response
<HTTP STATUS CODE 200>
{
    "notifications" : [
        {        
            "id": id,              
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "time": "<TIME OF NOTIFICATION>"
        }
    ]

}
```

#### Add Tutor to course
```POST /api/courses/{course_id}/add/```
```
Request
{
     "user_id": <USER INPUT>
}
```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "code": "CS 1110",
    "tutors": [<SERIALIZED USERS WITHOUT COURSES>, ...]
}
```

#### Drop Tutor from course
```POST /api/courses/{course_id}/drop/```
```
Request
{
     "user_id": <USER INPUT>
}
```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "email": "ry263@cornell.edu",
    "profile_pic": "url for profile pic",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

### Prepopulate the courses table(Must call at start of app)
```POST /api/allcourses/```
```
Response
<HTTP STATUS CODE 200>
{
    "courses" : [
        {
            "id": 1,
            "code": "CS 1110",
            "tutors": [<SERIALIZED USERS WITHOUT COURSES>, ...]
        },
        {
            "id": 2,
            "code": "CS 2110",
            "tutors": [<SERIALIZED USERS WITHOUT COURSES>, ...]
        }
    ]
}
```

### Add rate to user
```POST /api/rate/{user_id}```
```
Request
{
     "rate": <USER INPUT>
}
```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "email": "ry263@cornell.edu",
    "profile_pic": "url for profile pic",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

### Delete a user's availibility
```DELETE /api/users/{user_id}/availability/{availibility_id}/```
```
Response
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "sender_id": <USER INPUT FOR SENDER ID>,
    "receiver_id": <USER INPUT FOR RECEIVER ID>
}
```



