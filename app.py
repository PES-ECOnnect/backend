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

@app.route("/account/home", methods=['PUT'])
def setHome():
    token = request.args.get('token')
    newHome = request.args.get('newHome')

    if anyNoneIn([token, newHome]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setHome(newHome)
        return {'status': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/test")
def test():
    import data.DBUtils as db

    testRes = {}

    # Select tests
    ######

    # 1. Select single value
    q = "SELECT * FROM users WHERE iduser = %s"
    res = db.select(q, (1,), True)
    testRes['1.- Select 1'] = str(res["iduser"])
    testRes['1.- Select 1'] += " (TEST PASSES)" if res["iduser"] == 1 else ""

    # 2. Select many values

    q = "SELECT * FROM users"
    res = db.select(q, (1,), False)
    testRes['2.- Select 2'] = ''

    for row in res:
        testRes['2.- Select 2'] += str(row['iduser']) + ', '

    # Insert tests
    ######

    # 3. Successful insert
    import time
    testPass = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"  # password 'test'
    q = "INSERT INTO users (name, email, password, address) VALUES (%s, %s, %s, %s)"
    lastRowId = db.insert(q, (
    'test' + str(time.time())[0:15], 'test@gmail.com' + str(time.time())[0:15], testPass, 'testAddress'))
    testRes['3.- Insert 1: Success'] = str(lastRowId) + " (TEST PASSES)"

    # 4. Insert with Integrity error (Duplicate key)
    testPass = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"  # password 'test'
    q = "INSERT INTO users (name, email, password, address) VALUES (%s, %s, %s, %s)"
    try:
        lastRowId = db.insert(q, ('test', 'test@gmail.com' + str(time.time())[0:15], testPass, 'testAddress'))
        testRes['4.- Insert 2: Error'] = lastRowId
    except psycopg2.IntegrityError:
        testRes['4.- Insert 2: Error'] = "User already exists (TEST PASSES)"

    # Delete tests
    ######

    db.insert("INSERT INTO users (name, email, password, address) VALUES (%s, %s, %s, %s)",
              ('testDelete', 'testDelete@gmail.com', 'testDelete', 'testDelete'))

    # 5. Delete success

    q = "DELETE FROM users WHERE name = %s"
    deleted = db.delete(q, ('testDelete',))
    testRes['5.- Delete 1: Success'] = "(TEST PASSES)" if deleted else "Error, something went wrong deleting."

    # If no row is deleted, no error is returned.

    # Update tests
    ######

    db.insert("INSERT INTO users (name, email, password, address) VALUES (%s, %s, %s, %s)",
              ('testUpdate', 'testUpdate@gmail.com', 'testUpdate', 'testUpdate'))

    # 6. Update success

    q = "UPDATE users SET name = %s WHERE name = 'testUpdate'"
    success = db.update(q, ('test' + str(time.time())[0:15],))
    testRes['6.- Update 1: Success'] = "Update worked. (TEST PASSES)" if success else "Update did not work."

    db.insert("INSERT INTO users (name, email, password, address) VALUES (%s, %s, %s, %s)",
              ('testUpdate1', 'testUpdate@gmail.com', 'testUpdate', 'testUpdate'))

    db.insert("INSERT INTO users (name, email, password, address) VALUES (%s, %s, %s, %s)",
              ('testUpdate2', 'testUpdate@gmail.com', 'testUpdate', 'testUpdate'))

    # 7. Update error

    q = "UPDATE users SET name = %s WHERE name = 'testUpdate1' "
    success = db.update(q, ("testUpdate2",))  # Will fail because of duplicate key
    testRes['7.- Update 2: Error'] = "Update worked." if success else "Update did not work. (TEST PASSES)"

    db.delete("DELETE FROM users WHERE name IN ('testUpdate1', 'testUpdate2')")

    return testRes

if __name__ == "__main__":
    app.debug = True
    app.run()

'''
from endpoints import UserEndpoints
from endpoints import ReviewableEndpoints
from endpoints import ForumEndpoints'''
