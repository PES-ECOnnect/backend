from flask import Flask, request
from random import randint

import domain.Authenticator as auth

from domain.User import *
from domain.Product import *

import data.DBUser as dbu
import data.DBSession as dbs

import traceback

import json

app = Flask(__name__)


@app.route("/")
def helloWorld():
    return "PES Econnect Root!"


@app.route("/account", methods=['POST'])
def registerUser():
    # TODO: Use POST request instead of test data
    pass

@app.route("/account/login")
def accountLogin():
    email = request.args.get('email')
    passwordString = request.args.get('password')

    try:
        token = auth.logIn(email, passwordString)
        return json.dumps({
            'token': str(token)
        })

    except auth.UserNotFoundException:
        return json.dumps({'error': 'ERROR_USER_NOT_FOUND'})

    except auth.IncorrectUserPasswordException:
        return json.dumps({'error': 'ERROR_USER_INCORRECT_PASSWORD'})

    except dbs.FailedToOpenSessionException:
        return json.dumps({'error': 'ERROR_STARTING_USER_SESSION'})


@app.route("/account/isadmin", methods=['GET'])
def isAdmin():
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        u = auth.getUserForToken(token)

        return {'result': 'true'} if u.isAdmin() else {'result': 'false'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}



@app.route("/account/logout", methods=['GET'])
def logout():
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        auth.logOut(token)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/products/<id>/answer")
def answerQuestion(id):
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        questionId = request.args.get('questionId')
        chosenOption = request.args.get('chosenOption')

        product = Product(id, 'a', 1)
        product.answerQuestion(questionId, id, token, chosenOption)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

if __name__ == "__main__":
    app.debug = True
    app.run()

