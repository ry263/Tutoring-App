# Tutoring-App



## Backend API Specification
###  User Functions

#### Login
```GET /```
```
Response
<HTTP STATUS CODE 201>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

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
            "netid": "ry263",
            "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
            "availability": [ <SERIALIZED TIMES>, ... ],
            "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
            "rate": "20 per hour"
        },
        {
            "id": 2,
            "name": "Luk Man",
            "netid": "lm1",
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
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

#### Create user
```GET /api/users/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

#### Get specific user
```GET /api/users/{id}/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```

#### Delete user
```DELETE /api/users/{id}/```

```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES WITHOUT USERS>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ],
    "notifications": [ <SERIALIZED NOTIFICATIONS>, ... ],
    "rate": "20 per hour"
}
```
###  Course Functions
#### Get all Courses
```GET /api/courses/```
```
Response
<HTTP STATUS CODE 200>
{
    "notifications" : [
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
```GET /api/courses/{code}```
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
            "receiver_id": 1,
            "note": "Heyo wassup you wanna tutor me my number is ##########"
        },
        {
            "id": 2,
            "sender_id": 3,
            "receiver_id": 2,
            "note": "Hello, if you're free to tutor me this Thursday, please email me back at fake@email.com"
        }
    ]
}
```

#### Get notification by id
```GET /api/notifications/{id}/```
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "sender_id": 3,
    "receiver_id": 1,
    "note": "Heyo wassup you wanna tutor me my number is ##########"
}
```

#### Create notification
```POST /api/notifications/```
```
Request
{
    "sender_id": <USER INPUT>,
    "receiver_id": <USER INPUT>,
    "note": <USER INPUT>
}
```
```
Response
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "sender_id": <USER INPUT FOR SENDER ID>,
    "receiver_id": <USER INPUT FOR RECEIVER ID>,
    "note": <USER INPUT FOR NOTE>
}
```

#### Delete notification
```DELETE /api/notifications/{id}```
```
Response
<HTTP STATUS CODE 200>
{
    <DELETED NOTIFICATION>
}
```

