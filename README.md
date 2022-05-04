# Tutoring-App



# API Specification
## Expected Functionality

### Login
```GET /```
```
Response
<HTTP STATUS CODE 201>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ]
}
```

### Get all users
##### GET /api/users/
```
Response
<HTTP STATUS CODE 200>
{
    "users" : [
        {
            "id": 1,
            "name": "Rachel Yue",
            "netid": "ry263",
            "courses": [ <SERIALIZED COURSES>, ... ],
            "availability": [ <SERIALIZED TIMES>, ... ]
        },
        {
            "id": 2,
            "name": "Luk Man",
            "netid": "lm1",
            "courses": [ <SERIALIZED COURSES>, ... ],
            "availability": [ <SERIALIZED TIMES>, ... ]
        }
    ]
}
```

### Get current user
##### GET /api/users/current/
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ]
}
```

### Create user
##### GET /api/users/
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ]
}
```

### Get specific user
##### GET /api/users/{id}/
```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ]
}
```

### Delete user
##### DELETE /api/users/{id}/

```
Response
<HTTP STATUS CODE 200>
{
    "id": 1,
    "name": "Rachel Yue",
    "netid": "ry263",
    "courses": [ <SERIALIZED COURSES>, ... ],
    "availability": [ <SERIALIZED TIMES>, ... ]
}
```
