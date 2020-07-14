from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate

Base = declarative_base()
import json, os

database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
#    db.create_all() 
    migrate = Migrate(app, db)



class AbstractTable():
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        pass


class QuestionReplys(db.Model, AbstractTable):
    __tablename__ = "reply"

    question_id = Column(Integer, primary_key = True)
    reply_id  = Column(Integer, primary_key = True)


class Follow(db.Model, AbstractTable):
    __tablename__ = "follow"

    follower = Column(Integer, primary_key = True)
    followed = Column(Integer, primary_key = True)



class User(db.Model, AbstractTable):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    picture = Column(String)

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "picture" : self.picture
        }




class Question(db.Model, AbstractTable):
    __tablename__ = "question"

    id = Column(Integer, primary_key = True)
    content = Column(String, nullable=False)
    answer = Column(String)
    flag_answered = Column(Boolean, default = False)
    reacts = Column(Integer, default = 0)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = db.relationship("User", backref = "questions")



    def format(self):
        return {
            "id" : self.id,
            "content" : self.content,
            "answer" : self.answer,
            "reacts" : self.reacts,
            "user_id" : self.user_id,
            "is_answered" : self.flag_answered
        }

    def setID(self,id):
        self.id = id

class Asked(db.Model, AbstractTable):
    user_id = Column(Integer, primary_key = True)
    question_id = Column(Integer, primary_key = True)


class Report(db.Model, AbstractTable):
    __tablename__ = "report"

    id = Column(Integer, primary_key = True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = db.relationship("User", backref = "notifications")
    question_id = Column(Integer, ForeignKey("question.id"))
    # backref is not important
    question = db.relationship("Question", backref = "report")

    def format(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "question_id" : self.question_id
        }

    def setID(self,id):
        self.id = id

# map table that maps the IDs from Auth0 to another IDs that is used to attatch questions to users
class UserAuthID_ID(db.Model, AbstractTable):
    __tablename__ = "map"
    id = Column(Integer, primary_key= True)
    auth_id = Column(String)
