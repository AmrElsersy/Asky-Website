from app import *

# ======== Questions ==============
@app.route('/questions/<int:id>', methods=["GET"])
def get_question(id):
    try:
        question = Question.query.filter(Question.id == id).all()[0]
        
        if not question:
            abort(404)

        return jsonify({
            "question" : question.format()
        })

    except:
        abort(400)

# Admin Role
@app.route('/questions/<int:id>', methods=["DELETE"])
def get_question(id):
    try:
        question = Question.query.filter(Question.id == id).all()[0]

        if not question:
            abort(404)

        question.delete()        

        return jsonify ({
            "success" : True,
        }), 200

    except:
        abort(400)

# answer & react
@app.route('/questions/<int:id>', methods=["PATCH"])
def answer_question(id):
    try:
        data = request.get_json()

        question = Question.query.filter(Question.id == id).all()[0]

        if not question:
            abort(404)

        if "answer" in data:
            question.answer = data["answer"]
            question.update()
        if "reacts" in data:
            question.reacts = data["reacts"]
            question.update()

        return jsonify ({
            "success" : True,
        }), 200
    except:
        abort(400)

####  Replys
@app.route('/questions/<int:id>/reply',  methods=["POST"])
def add_reply(id):
    try:
        data = request.get_json()

        parent_question = Question.query.get(id)
        if not parent_question:
            abort(404)

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

        else:
            # bad request
            abort(400)

    except:
        abort(400)


# get all replys of a question
@app.route('/questions/<int:id>/reply',  methods=["GET"])
def get_replys(question_id):
    replys = QuestionReplys.query.filter(QuestionReplys.question_id == id).all()

    # get only the replys that get answered 
    question_replys = []
    for reply in replys:
        if reply.flag_answered:
            question_replys.append(reply)

    return jsonify({
        "success" : True,
        "reply" : [reply.format() for reply in question_replys]
    }), 200

# ============= User ================
@app.route('/users/<int:id>',  methods=["GET"])
def get_user(id):
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
def edit_user(id):
  try:
    data = request.get_json()

    if not data:
        abort(400) # bad request

    user = User.query.get(id)
    if not user:
        abort(404)

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
def get_user_questions(id):

    user = User.query.get(id)
    if not user:
        abort(404)

    # get the IDs of questions that the user has asked
    questions_ids = Asked.query.filter(Asked.user_id == user.id).all()

    # get that questions by id 
    questions = Question.query.filter(Question.id == questions_ids.question_id)

    return jsonify({
        "success" : True,
        "questions" : [q.format() for q in questions]
    }), 200


### Get My Questions to answer it or to show it to other users
@app.route('/users/<int:id>/questions',  methods=["GET"])
def get_user_questions(id):

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
def ask_question(id):
    data = request.get_json()

    if not data:
        abort(400) # bad request

    user = User.query.get(id)
    if not user:
        abort(404)

    if "id" in data and "question" in data:
        new_question = Question(
            content = data["question"],
            user_id = user.id
        ).insert()

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
@app.round('/users/<int:id>/followers', methods =["GET"])
def get_followers(id):

    user = User.query.get(id)
    if not user:
        abort(404)

    followers = Follow.query.filter(Follow.followed == user.id)

    return jsonify({
        "success" : True,
        "followers": [follower.format() for follower in followers]
    }), 200

# follow someone 
@app.round('/users/<int:id>/followers', methods =["POST"])
def add_follower(id):

    data = request.get_json()

    if not data:
        abort(400) # bad request

    user = User.query.get(id)
    if not user:
        abort(404)

    if "id" in data:
        Follow(follower = user.id, followed = data["id"]).insert()

        return jsonify({
            "success" : True,
            "followed" : data["id"]
        }), 200
    else:
        abort(400) # bad request


# ============== Report ===============
# Admin Role
@app.route('/reports', methods= ["GET"])
def get_all_reports():
    # get all reports for the admin
    reports = Report.query.all()

    return jsonify({
        "success" : True,
        "reports" : [report.format() for report in reports]
    }), 200

# User only Role
@app.route('/reports', methods= ["POST"])
def add_report_question(id):

    data = request.get_json()
    if not data:
        abort(400) # bad request

    if "user_id" in data and "question_id" in data:
        
        new_report = Report(
            user_id = data["user_id"],
            question_id = data["question_id"]
        ).insert()
        
        return jsonify({
            "success" : True,
            "report" : new_report.format()
        }), 200
    else:
        abort(400)

# Admin Role
@app.route('/reports/<int:id>', methods= ["GET"])
def get_report(id):
    report = Report.query.get(id)
    if not report:
        abort (404)

    return jsonify({
        "success": True,
        "report" : report.format()
    }), 200

# Admin Role
@app.route('/reports/<int:id>', methods= ["DELETE"])
def delete_report(id):
    report = Report.query.get(id)
    if not report:
        abort (404)

    report.delete()

    return jsonify({
        "success": True,
        "deleted_report" : id
    }), 200

