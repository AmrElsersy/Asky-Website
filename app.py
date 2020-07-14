from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import random
import json
from models import *
from auth import *
from API import Resource_Questions, Resource_Users, Resource_Reports, Error_Handling


def create_app():
    
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    Error_Handling(app)
    Resource_Questions(app)
    Resource_Users(app)
    Resource_Reports(app)

    @app.route('/')
    def home():
        print(request.headers.get("Authorization",None))
        users = User.query.all()
        return jsonify({
            "users" : [user.format() for user in users]
        })

    return app


app = create_app()

if __name__ == '__main__':
  app.run(use_reloader=False, debug=False)

