from Models import *
from auth import *
from flask import Flask, request, abort, jsonify

# ======== Questions ==============

def Resource_Questions(app):
    @app.route('/questions/<int:id>', methods=["GET"])
    @requires_auth("get:question")
    def get_question(jwt, id):
        question = Question.query.get(id)
        print(question)
        
        if question is None:
            print("not founed")
            abort(404)

        return jsonify({
            "question" : question.format()
        })

    # Admin Role
    @app.route('/questions/<int:id>', methods=["DELETE"])
    @requires_auth("delete:question")
    def delete_question(jwt, id):

        question = Question.query.get(id)

        if question is None:
            abort(404)
        try:

            # delete the assignation of user to that question
            users_asked_question = Asked.query.filter(Asked.question_id == question.id).all()
            if users_asked_question:
                users_asked_question[0].delete()

            # delete the assign of replys to that question
            replys = QuestionReplys.query.filter(
                QuestionReplys.question_id == question.id or
                QuestionReplys.reply_id == question.id
                ).all()
            for reply in replys:
                reply.delete()

            question.delete()        

            return jsonify ({
                "success" : True,
            }), 200

        except:
            abort(400)

    # answer & react
    @app.route('/questions/<int:id>', methods=["PATCH"])
    @requires_auth("answer:question")
    def answer_question(jwt, id):
        data = request.get_json()

        if data is None:
            abort(400)
            
        question = Question.query.get(id)

        if question is None:
            abort(404)

        try:
            if "answer" in data:
                question.answer = data["answer"]
                question.flag_answered = True
                question.update()
            if "reacts" in data:
                question.reacts = data["reacts"]
                question.update()

            return jsonify ({
                "success" : True,
                "question" : question.format()
            }), 200
        except:
            abort(400)

    ####  Replys
    @app.route('/questions/<int:id>/replys',  methods=["POST"])
    @requires_auth("answer:question")
    def add_reply(jwt, id):
        data = request.get_json()

        if data is None:
            abort(400)

        parent_question = Question.query.get(id)
        if not parent_question:
            abort(404)

        try:
            if "reply" in data and "asker_id" in data:

                # create new question
                new_reply = Question(
                    content = data["reply"],
                    user_id = parent_question.user_id
                )

                # add to the database
                new_reply.insert()

                # add reply to the parent question
                QuestionReplys(question_id = id, reply_id = new_reply.id).insert()
                # assign the user who asked the reply to the reply
                Asked(user_id = data["asker_id"], question_id = new_reply.id).insert()

                return jsonify({
                    "success" : True,
                    "id" : new_reply.id
                }),200

            else:
                # bad request
                abort(400)

        except:
            abort(400)


    # get all replys of a question
    @app.route('/questions/<int:id>/replys',  methods=["GET"])
    @requires_auth("get:question")
    def get_replys(jwt, id):
        
        q = Question.query.get(id)
        if q is None:
            abort(404)

        replys = QuestionReplys.query.filter(QuestionReplys.question_id == id).all()

        # get only the replys that get answered 
        question_replys = []
        for reply in replys:
            question = Question.query.get(reply.reply_id)
            question_replys.append(question)

        return jsonify({
            "success" : True,
            "reply" : [reply.format() for reply in question_replys]
        }), 200


# ============= User ================
def Resource_Users(app):
    @app.route('/users/<int:id>',  methods=["GET"])
    @requires_auth("get:user_info")
    def get_user(jwt, id):

        user = User.query.get(id)
        if not user:
            abort(404)

        # get the answered questions
        questions = Question.query.filter(
            Question.user_id == user.id and 
            Question.flag_answered == True).all()    
        
        return jsonify ({
            "success" : True,
            "user" : user.format(),
            "questions" : [question.format() for question in questions]
        }), 200

    @app.route('/users/<int:id>',  methods=["PATCH"])
    @requires_auth("get:user_info")
    def edit_user(jwt, id):
        data = request.get_json()

        if not data:
            abort(400) # bad request

        user = User.query.get(id)
        if not user:
            abort(404)

        try:
            if "name" in data:
                user.name = data["name"]
            if "picture" in data:
                user.picture = data["picture"]
            
            return jsonify({
                "success" : True,
                "user" : user.format()
            }),200
        except:
            abort(400) # bad request

    @app.route('/users/<int:id>/asked_questions',  methods=["GET"])
    @requires_auth("get:question")
    def get_user_asked_questions(jwt, id):

        user = User.query.get(id)
        if not user:
            abort(404)

        # get the IDs of questions that the user has asked
        questions_ids = Asked.query.filter(Asked.user_id == user.id).all()

        # get that questions by id 
        questions = []
        for q_id in questions_ids:
            questions.append( Question.query.get(q_id.question_id) )

        return jsonify({
            "success" : True,
            "questions" : [q.format() for q in questions]
        }), 200


    ### Get My Questions to answer it or to show it to other users
    @app.route('/users/<int:id>/questions',  methods=["GET"])
    @requires_auth("get:question")
    def get_user_questions(jwt, id):

        user = User.query.get(id)
        if not user:
            abort(404)

        # questions asked to the user 
        questions = Question.query.filter(
            Question.user_id == user.id).all()


        return jsonify({
            "success" : True,
            "questions" : [question.format() for question in questions]
        }), 200

    ### Add Question
    @app.route('/users/<int:id>/questions',  methods=["POST"])
    @requires_auth("ask:question")
    def ask_question(jwt, id):
        data = request.get_json()

        if not data:
            abort(400) # bad request

        user = User.query.get(id)
        if user is None:
            abort(404)

        if "id" in data and "question" in data:
            new_question = Question(
                content = data["question"],
                user_id = user.id
            )
            new_question.insert()

            Asked(
                user_id = data["id"],
                question_id = new_question.id
            ).insert()

            return jsonify({
                "success" : True,
                "question" : new_question.format()
            }), 200

        else : 
            abort(400) # bad request



    # get the users that the user follow 
    @app.route('/users/<int:id>/followers', methods =["GET"])
    @requires_auth("get:user_info")
    def get_followers(jwt, id):

        user = User.query.get(id)
        if not user:
            abort(404)

        followers = Follow.query.filter(Follow.follower == user.id).all()
        users = []

        for follower in followers:
            user_follower = User.query.get(follower.followed)
            users.append(user_follower)

        return jsonify({
            "success" : True,
            "followers": [follower.format() for follower in users]
        }), 200

    # follow someone 
    @app.route('/users/<int:id>/followers', methods =["POST"])
    @requires_auth("follow:profile")
    def add_follower(jwt, id):

        data = request.get_json()

        if not data:
            abort(400) # bad request

        user = User.query.get(id)
        if not user:
            abort(404)

        if "id" in data:
            if len( Follow.query.filter(Follow.followed == data['id']).all() ) == 0:
                Follow(follower = user.id, followed = data["id"]).insert()

            return jsonify({
                "success" : True,
                "followed" : data["id"]
            }), 200
        else:
            abort(400) # bad request


# ============== Report ===============
def Resource_Reports(app):
    # Admin Role
    @app.route('/reports', methods= ["GET"])
    @requires_auth("get:report")
    def get_all_reports(jwt):
        # get all reports for the admin
        reports = Report.query.all()
        return jsonify({
            "success" : True,
            "reports" : [report.format() for report in reports]
        }), 200

    # User only Role
    @app.route('/reports', methods= ["POST"])
    @requires_auth("add:report")
    def add_report_question(jwt):

        data = request.get_json()
        if not data:
            abort(400) # bad request

        if "user_id" in data and "question_id" in data:
            
            rr = Report.query.filter(Report.user_id == data["user_id"] and Report.question_id == data["question_id"]).all()
            if len(rr) == 1:
                print('xxxxxxxxxxxx')
                return jsonify({
                    "success" : True,
                    "report" : rr[0].format()
                }), 200

            print('yyyyyyyyyyyyyyyy')
            new_report = Report(
                user_id = data["user_id"],
                question_id = data["question_id"]
            )
            print(new_report)
                
            new_report.insert()
            
            return jsonify({
                "success" : True,
                "report" : new_report.format()
            }), 200
        else:
            abort(400)

    # Admin Role
    @app.route('/reports/<int:id>', methods= ["GET"])
    @requires_auth("get:report")
    def get_report(jwt,id):
        report = Report.query.get(id)
        if not report:
            abort (404)

        return jsonify({
            "success": True,
            "report" : report.format()
        }), 200

    # Admin Role
    @app.route('/reports/<int:id>', methods= ["DELETE"])
    @requires_auth("delete:report")
    def delete_report(jwt, id):
        report = Report.query.get(id)
        if not report:
            abort (404)

        report.delete()

        return jsonify({
            "success": True,
            "deleted_report" : id
        }), 200

def Error_Handling(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success" : False,
            "error" : 404,
            "message" : "Error Not Found"
        }) , 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success" : False,
            "error" : 400,
            "message" : "Error Bad Request, you may forgot to send the json"
        }) , 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success" : False,
            "error" : 422,
            "message" : "Error Un Proccessable"
        }) , 422

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            'message': error.error
        }), 401

