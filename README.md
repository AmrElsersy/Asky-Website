Auth0
https://sersy.auth0.com/authorize?audience=Asky&response_type=token&client_id=u0y0irpKDge5BHCadh7U7ni9qB2ih5dw&redirect_uri=http://127.0.0.1:5000/

Gmail,Ray2: 
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3NlcnN5LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzkwNDIxOTE1MjAzMzQ0MzQ1MyIsImF1ZCI6WyJBc2t5Il0sImlhdCI6MTU5NDU3NTk3NCwiZXhwIjoxNTk0NjQ3OTcyLCJhenAiOiJ1MHkwaXJwS0RnZTVCSENhZGg3VTduaTlxQjJpaDVkdyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6W119.YgJSEFkQIng54wwS46gNqEQWm1Inw1mgFitfewlyItM

Github
http://127.0.0.1:5000/#access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3NlcnN5LmF1dGgwLmNvbS8iLCJzdWIiOiJnaXRodWJ8MzU2MTM2NDUiLCJhdWQiOlsiQXNreSJdLCJpYXQiOjE1OTQ1Nzc3MTEsImV4cCI6MTU5NDY0OTcwOSwiYXpwIjoidTB5MGlycEtEZ2U1QkhDYWRoN1U3bmk5cUIyaWg1ZHciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOltdfQ.jRZ_hf5EBUMojPo49AqRk-1DrU4-WG2SZupmjnsGN3U&scope=openid%20profile%20email&expires_in=71998&token_type=Bearer&state=g6Fo2SA2UDBNYkNvYmtNMFN1Q0RpblA4dlBRcVhod0g4SDBQT6N0aWTZIHM5ZTdsN3ZUdmE3U1htTUo0Q0c0ZlU4T1plTGdNQkkzo2NpZNkgdTB5MGlycEtEZ2U1QkhDYWRoN1U3bmk5cUIyaWg1ZHc


GET /questions/id
get the data of a specific question
example: /questions/34
return :
{
    "question": {
        "answer": null,
        "content": "test_questions",
        "id": 34,
        "is_answered": false,
        "reacts": 0,
        "user_id": 25
    }
}


GET /users/<int:id>/questions
get the questions that asked to the user
example : users/100/questions
return {
	"questions": [
		{
			"content": "what is your name?",
			"answer": "karim",
			"user_id": 25
			"id" : 100
			"reacts" : 2
		}
	]
}

POST /users/<int:id>/questions
get the questions that asked to the user
example : users/100/questions
{
	"content" : "question .... ?",
	"asker_id": 12
}
return {
	
}

GET /users/<int:id>/followers
get the followers that the user with <id> follows
example GET users/100/followers
return {
	"followers" : [
		{
			"id": 10,
			"name": "user1"
		},
		{
			"id": 123,
			"name": "user2"
		}
	]
}

GET /users/<int:id>/followers
user with <id> follows user with id specefied in the json body
example POST users/100/followers {"id" : 200}
return {
	"followed": 200,
	"success": True
}

GET users/<int:id>/asked_questions
get the questions that the user asked
example : users/100/asked_questions
return:
{
	"questions": [
		{
			"content": "what is your name?",
			"answer": "karim",
			"user_id": 25
			"id" : 100
			"reacts" : 2
		}
	]
}


POST users/id/questions
brief: ask question to the user which has <id> and send the asker id & the question in the body json
example:
/users/25/questions
{
	"id": 28,
	"question": "test_question"
}

return:
{
    "question": {
        "answer": null,
        "content": "test_questions",
        "id": 34,
        "is_answered": false,
        "reacts": 0,
        "user_id": 25
    },
    "success": true
}


GET /reports
return all the reports that get reported by users
example /reports
return 
{
    "reports": [
        {
            "id": 6,
            "question_id": 28,
            "user_id": 26
        },
        {
            "id": 7,
            "question_id": 33,
            "user_id": 25
        }
    ],
    "success": true
}



