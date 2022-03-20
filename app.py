from flask import Flask, request
from random import randint

from domain.Authenticator import *
from domain.Authenticator import logOut
from domain.User import *

import json

app = Flask(__name__)


@app.route("/")
def helloWorld():
    return "PES Econnect Root!"


@app.route("/account", methods=['POST'])
def registerUser():
    # TODO: Use POST request instead of test data

    if request.method == 'POST':
        # Create account
        username = request.form['username']
        username = request.form['email']
        password = request.form['password']

        username = "TestUser" + str(randint(1, 10000))
        password = "TestPass" + str(randint(1, 10000))

        try:
            User.register(username, password)

            # User created successfully
            return 0

        except UserAlreadyExistsException as ue:
            print(ue)

            # Failed to create user because username already exists
            return ERR_USERNAME_EXISTS;


@app.route("/account/login")
def accountLogin():
    email = request.args.get('email')
    passwordString = request.args.get('password')

    try:
        token = logIn(email, passwordString)
        return json.dumps({
            'token': str(token)
        })

    except UserNotFoundException:
        return json.dumps({'error': 'ERROR_USER_NOT_FOUND'})

    except IncorrectUserPasswordException:
        return json.dumps({'error': 'ERROR_USER_INCORRECT_PASSWORD'})

    except FailedStartingSessionForUserException:
        return json.dumps({'error': 'ERROR_STARTING_USER_SESSION'})


@app.route("/account/logout", methods=['GET'])
def logout():
    tok = request.args.get('token')
    try:
        logOut(tok)
        return {'status': 'success'}
    except InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/products/<id>/answer")
def adminUser(id):
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()

