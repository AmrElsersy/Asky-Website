from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import random
import json
from Models import *

app = Flask(__name__)
setup_db(app)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success" : False,
        "error" : 400,
        "message" : "Error Bad Request, you may forgot to send the json"
    }) , 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success" : False,
        "error" : 404,
        "message" : "Error Not Found"
    }) , 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success" : False,
        "error" : 422,
        "message" : "Error Un Proccessable"
    }) , 422

if __name__ == '__main__':
  app.run(use_reloader=False)

