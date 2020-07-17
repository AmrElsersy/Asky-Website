# Asky Website
#### Asky Project is a Question Based Website that allow people to ask each other questions and follow other users and report bad questions, like ask-fm

it is only a backend

## User Story
### Asky Backend has 2 Roles User and Admin
* User can ask question to other user
* User can answer his questions
* User can report a bad question
* User can react to a question 
* User can get all questions that people ask him
* User can get the questions he asked
* User can edit his profile
* User can see who is he following to get their questions

- =========================================

* Admin can view all reports by all users
* Admin can delete question 
* Admin can delete the report after dealing with its question
* Admin can view question's data

## Database Design

![Screenshot from 2020-07-17 02-35-19](https://user-images.githubusercontent.com/35613645/87735655-7189b380-c7d6-11ea-9f37-51525bfdf77d.png)


## Topics
- The Final Project of the Full stack Nanodegree
- Database modeling using sqlalchemy (models.py)
- REST API for CRUD using Flask (app.py)
- Authentication & Authorization Role based using Auth0 (auth.py)
- Deployment on Heroku
- Unit testing using unittest (Test.py)
- Enviroment variables encapsulation (Setup.sh)


## Install
```
source setup.sh
pip install -r requirements.txt
```

## Run the Server
```
source setup.py
python3 app.py
```

## Run Testing
```
source setup.py
python3 Test.py

----------------------------------------------------------------------
Ran 35 tests in 60.227s

OK
```

### Enviroment variables
- AUTH0_DOMAIN='sersy.auth0.com'
- API_AUDIENCE='Asky'
- ALGORITHMS='RS256'
- ADMIN= ( Admin Token )
- USER ( User Token )
- DATABASE_URL='postgresql://postgres:1@localhost:5432/Asky'





## Getting Started
* Base URL : this app can be run localy with base URL https://askysers.herokuapp.com/
## Error Handling
* Sample 
```
      "success" : False,
      "error" : 404,
      "message" : "Error Not Found"
```
* Error types
- 404 Unfound 
- 400 Bad Request
- 422 Not Proceesable
- 401 Not Authenticated
- 403 Not Authorized


## Endpoits
### Note : All categories requires Access Token
### Tokens :
#### Admin : eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IloxaGFneUZaSkVySGVMbnpLcHdmQiJ9.eyJpc3MiOiJodHRwczovL3NlcnN5LmF1dGgwLmNvbS8iLCJzdWIiOiJnaXRodWJ8MzU2MTM2NDUiLCJhdWQiOlsiQXNreSIsImh0dHBzOi8vc2Vyc3kuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDY5Njg1NSwiZXhwIjoxNTk0NzgzMjU1LCJhenAiOiJ1MHkwaXJwS0RnZTVCSENhZGg3VTduaTlxQjJpaDVkdyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cXVlc3Rpb24iLCJkZWxldGU6cmVwb3J0IiwiZ2V0OnF1ZXN0aW9uIiwiZ2V0OnJlcG9ydCIsImdldDp1c2VyX2luZm8iLCJsb2dpbiJdfQ.nuXfzj4OSayT0AaLaldyMKa6myNzK4QtCYilHjmcfLuCu9wdKNWXXISdGDaYF5oWSSyhvJ1D4uMRuQN0UKuoR3OLN7J4c7l1HMmhaNU4Sw9XkgLAkr_KhVGolQoYrbrPnpPsykKNYBD4pcZbJW4xQ7VBwB-3s80HW2pgUc1PxOC1Ul7WIXPvL_axSMByXvqLLmDVj3gP9b6HBB_43m6AExVQkyEyUp8z5SqY5RIbVph3skkOEREwv_KQo0U7_R5Yf_NMUKRyUyqPLhO1ITZboqF74FhIjkvZEecrSYGVeZv9ESJHAObwfNT2FEcANW4RZWqDqr6pJBO-1QrgsvrNbA


#### User : 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IloxaGFneUZaSkVySGVMbnpLcHdmQiJ9.eyJpc3MiOiJodHRwczovL3NlcnN5LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzkwNDIxOTE1MjAzMzQ0MzQ1MyIsImF1ZCI6WyJBc2t5IiwiaHR0cHM6Ly9zZXJzeS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk0Njk2OTIxLCJleHAiOjE1OTQ3ODMzMjEsImF6cCI6InUweTBpcnBLRGdlNUJIQ2FkaDdVN25pOXFCMmloNWR3Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDpyZXBvcnQiLCJhbnN3ZXI6cXVlc3Rpb24iLCJhc2s6cXVlc3Rpb24iLCJmb2xsb3c6cHJvZmlsZSIsImdldDpxdWVzdGlvbiIsImdldDp1c2VyX2luZm8iLCJsb2dpbiJdfQ.jeYC8dl9vYjlqKmJcHiCXuYk6vYxYuts_oTCzjoFGgACqVk5rEjeU6QiHn8JKXMAgwGPk1uMnHNmpGKrkRwuCBzZgpW9OBEYsOd2ZuB5Af3u_JEVOP5gCc3IIo2Nb1qY166ogXPHar_0qCrEC2ipmBE3_WQ7dPeifROqsrwudF-uMTMauYg1KsbZrRRZVHH7qYZ_t28FHXpDV4B1P1I3GeBcoNtcQRXwogw6QNKzrJsl2jodB6JNoVIF91PMmrDLXLiefUJd2hmJiow20Awu-fzHSbT313-dr0Mz6sGrSjsmdHO6PgSBHRIzuAeGh_BYLKm7XHJsuPBQj_ckN7bvJg



### Each endpoint assigned with its roles

### All endpoints is tested on Postman


( User & Admin )
* GET /questions/<id>
- get the data of a specific question
- Request : GET askysers.herokuapp.com/questions/1
- Request Arguments : None
- Response :
``` 
{
    "question": {
        "answer": " a computer engineer student",
        "content": "how are you sersy? ",
        "id": 26,
        "is_answered": false,
        "reacts": 3,
        "user_id": 25
    }
}
```



=================================== 
( Admin )
* DELETE /questions/<id>
- get the data of a specific question
- Request : DELETE askysers.herokuapp.com:5000/questions/2
- Response :
``` 
{
	"success": True
}
```



=================================== 
( User )
* PATCH /questions/<id>
- get the data of a specific question
- Request : PATCH askysers.herokuapp.com:5000/questions/1
```
{
	"answer" : "answer to question",
	"reacts" : 4
}
```
- Response :
``` 
{
"success": True,
"question": {
        "answer": " answer to question",
        "content": "how are you sersy? ",
        "id": 26,
        "is_answered": false,
        "reacts": 4,
        "user_id": 25
    }
}
```


=================================== 
( User & Admin )
* GET /questions/<int:id>/replys
- get the replys of the question ( reply is another question but is a child of queistion with <id>)
- Request : GET askysers.herokuapp.com/questions/4/replys
- Request Arguments : 
- Response :
``` 
{
    "reply": [
        {
            "answer": null,
            "content": "test_reply",
            "id": 5,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        }
    ],
    "success": true
}
```


=================================== 
( User )
* POST /questions/<int:id>/replys
- add another question as a reply (continue asking) to that question (like in ask-fm)
- Request : POST askysers.herokuapp.com/questions/4/replys
- Request Arguments : reply:string contains the question reply, asker_id is the id of the user that is asking
```
{
	"reply" : "continue asking... reply ???",
	"asker_id" : 101
}
```
- Response : id : is the id of the added reply question
``` 
{
    "id": 153,
    "success": true
}
```



===================================
( User & Admin )
* GET /users/<int:id>
- get the user info like name, picture
- Request : GET askysers.herokuapp.com/users/28
- Request Arguments :  None
- Response :
``` 
{
    "questions": [],
    "success": true,
    "user": {
        "id": 28,
        "name": "sersy",
        "picture": null
    }
}
```


=================================== 
( User & Admin )
* PATCH /users/<int:id>
- get the user info like name, picture
- Request : PATCH askysers.herokuapp.com/users/28
- Request Arguments :  
```
{
	"name" : "mahmoud sersy",
	"picture": "link to his picture"
}
```
- Response :
``` 
{
    "success": true,
    "user": {
        "id": 28,
	"name" : "mahmoud sersy",
	"picture": "link to his picture"
    }
}
```


=================================== 
( User)
* GET users/<int:id>/asked_questions
- get the questions that the user asked
- Request : GET askysers.herokuapp.com/users/28/asked_questions
- Response :
``` 
{
	"questions": [
		{
			"content": "test question",
			"answer": "test answer",
			"user_id": 25
			"id" : 100
			"reacts" : 3
		}
	]
}
```



=================================== 
( User & Admin )
* GET /users/<int:id>/questions
- get the questions that asked to the user
- Request : GET askysers.herokuapp.com/users/25/questions
- Response 
```
{
    "questions": [
        {
            "answer": null,
            "content": "test_reply",
            "id": 42,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        },
        {
            "answer": " a computer engineer student",
            "content": "how are you sersy? ",
            "id": 26,
            "is_answered": false,
            "reacts": 3,
            "user_id": 25
        },
        {
            "answer": null,
            "content": "hey amr , iam user_not ray2, how are you ?",
            "id": 33,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        },
        {
            "answer": "test_answer",
            "content": "test_question",
            "id": 100,
            "is_answered": true,
            "reacts": 3,
         "user_id": 25
        },
        {
            "content": "is that project excellent or very goog ?",
            "id": 28,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        }
    ],
    "success": true
}
```


=================================== 
( User )
* POST /users/<int:id>/questions
- ask question to the user
- Request : POST askysers.herokuapp.com/users/28/questions
- Request body: id is the asker id
``` 
	"id": 28,
	"question": "question body ???"
}
```
- Response : id : the new question id
``` 
{
	"success" : True,
	"id" 300
}
```

=================================== 
( User & Admin )
* GET /users/<id>/followers
- get the followers that the user with <id> follows
- Request : GET askysers.herokuapp.com/users/28/followers
- Response :
```
{
	"followers" : [
		{
			"id": 25,
			"name": "amr"
		}	
	]
}
```

=================================== 
( User )
* POST users/id/followers 
- make user of id (specified in the url) to follow a user with id (specified in json body)
- Request : POST users/100/followers
``` 
{"id" : 100}
```
- Response :
``` 
{
	"followed": 100,
	"success": True
}
```


=========================================
( Admin )
* GET /reports
- return all the reports that get reported by users (only for admin)
- Request : GET askysers.herokuapp.com/reports
``` 
```
- Response :
``` 
{
    "reports": [
        {
            "id": 7,
            "question_id": 33,
            "user_id": 25
        },
        {
            "id": 100,
            "question_id": 100,
            "user_id": 100
        }
    ],
    "success": true
}
```

=================================== 
( User )
* POST /reports 
- report a bad question to the admin (only for user)
- Request : POST askysers.herokuapp.com/reports
``` 
{
	"user_id": 25,
	"question_id": 42
}
```
- Response :
``` 
{
    "report": {
        "id": 41,
        "question_id": 42,
        "user_id": 25
    },
    "success": true
}
```


=================================== 
( Admin )
* GET /reports/<int:id>
- return a specific report that get reported by users (only for admin)
- Request : GET askysers.herokuapp.com/reports/7
- Response :
``` 
{
    "report":
        {
            "id": 7,
            "question_id": 33,
            "user_id": 25
        },
    "success": true
}
```

=================================== 
( Admin )
* DELETE /reports/<int:id>
- Delete a report (only for admin)
- Request : DELETE askysers.herokuapp.com/reports/200
- Response :
``` 
{
	"deleted_report": 200,
	"success": true
}
```




