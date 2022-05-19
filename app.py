import traceback

import psycopg2
from flask import Flask, request

# Domain Layer
import domain.Authenticator as auth

from domain.Reviewable import *
from domain.Question import *

from domain.User import *
from domain.Question import *
from domain.Forum import *

# Data Layer (TODO - Remove)
import data.DBSession as dbs
import data.DBReviewable as dbp
import data.DBUser as dbu

import json
import hashlib

from sodapy import Socrata
client_gene = Socrata("analisi.transparenciacatalunya.cat", "kP8jxf5SrHh4g8Sd42esZ5uba")

from flask import Blueprint

from endpoints.UserEndpoints import user_endpoint
from endpoints.ReviewableEndpoints import reviewable_endpoint
from endpoints.ForumEndpoints import forum_endpoint

app = Flask(__name__)

app.register_blueprint(user_endpoint)
app.register_blueprint(reviewable_endpoint)
app.register_blueprint(forum_endpoint)

def anyNoneIn(l: list) -> bool:
    return any(x is None for x in l)

@app.route("/")
def helloWorld():
    return "PES Econnect Root!"

if __name__ == "__main__":
    app.debug = True
    app.run()

'''
from endpoints import UserEndpoints
from endpoints import ReviewableEndpoints
from endpoints import ForumEndpoints'''
