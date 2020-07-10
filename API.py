from app import *

# ======== Questions ==============
@app.route('/questions')
def get_all_questions():
    pass

@app.route('/questions/<int:id>', methods=["GET"])
def get_question(id):
    pass

# Admin Role
@app.route('/questions/<int:id>', methods=["DELETE"])
def get_question(id):
    pass

# answer & react
@app.route('/questions/<int:id>', methods=["PATCH"])
def answer_question(id):
    data = request.get_json()

@app.route('/questions/<int:id>/reply',  methods=["POST"])
def add_reply(id):
    data = request.get_json()

@app.route('/questions/<int:id>/reply',  methods=["GET"])
def get_replys(question_id):
    pass

# ============= User ================
@app.route('/users/<int:id>',  methods=["GET"])
def get_user(id):
    pass

@app.route('/users/<int:id>',  methods=["PATCH"])
def edit_user(id):
    data = request.get_json()

# Admin Role
@app.route('/users/<int:id>',  methods=["DELETE"])
def delete_user(id):
    pass

@app.route('/users/<int:id>/questions',  methods=["GET"])
def get_user_questions(id):
    pass


# ============== Report ===============
# Admin Role
@app.route('/reports', methods= ["GET"])
def get_all_reports():
    pass

# User only Role
@app.route('/reports', methods= ["POST"])
def add_report_question(id):
    pass

# Admin Role
@app.route('/reports/<int:id>', methods= ["GET"])
def get_report(id):
    pass

# Admin Role
@app.route('/reports/<int:id>', methods= ["DELETE"])
def delete_report(id):
    pass


# ============= Follow ================
@app.route('/follow/<int:id_follower>/<int:id_followed>',  methods=["POST"])
def follow_user(id_follower, id_followed):
    pass



