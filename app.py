import sqlite3

from flask import Flask, request

# Domain Layer
import domain.Authenticator as auth

from domain.Reviewable import *

# Data Layer (TODO - Remove)
import data.DBSession as dbs
import data.DBReviewable as dbp

import json
import hashlib

app = Flask(__name__)


@app.route("/")
def helloWorld():
    return "PES Econnect Root!"

@app.route("/account", methods=['POST'])
def signUp():
    if request.method != 'POST':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    enPass = hashlib.sha256(password.encode('UTF-8')).hexdigest()

    if auth.getUserForEmail(email) is not None:
        return {'error': 'ERROR_USER_EMAIL_EXISTS'}

    if auth.getUserForUsername(username) is not None:
        return {'error': 'ERROR_USER_USERNAME_EXISTS'}

    try:
        auth.signUp(email, username, enPass)
        return {'status': 'success'}

    except sqlite3.Error:
        return {'error': 'ERROR_FAILED_SIGN_UP'}


@app.route("/account/login", methods=['GET'])
def accountLogin():
    if request.method != 'GET':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

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
    if request.method != 'GET':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        u = auth.getUserForToken(token)

        return {'result': 'true'} if u.isAdmin() else {'result': 'false'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/account/logout", methods=['GET'])
def logout():
    if request.method != 'GET':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        auth.logOut(token)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/products", methods=['POST', 'GET'])
def products():
    if request.method != 'POST' and request.method != 'GET':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    auth.checkValidToken(token)

    revType = request.args.get('type')
    name = request.args.get('name')

    if request.method == 'POST':
        # Create product

        manufacturer = request.args.get('manufacturer')
        # TODO: Obtain bytes from request body, upload to storage service, obtain URL, save it and return it.
        # imageURL = request.args.get('image')
        imageURL = 'https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-images-product-6_large.png'

        newProduct = Reviewable(id=None, name=name, type=revType, imageURL=imageURL, manufacturer=manufacturer, lat=None, lon=None)
        try:
            newProduct.insert()
            return {'status': 'success'}

        except dbp.FailedToInsertReviewableException:
            return {'error': 'ERROR_FAILED_TO_CREATE_PRODUCT'}

    elif request.method == 'GET':
        revRows = getReviewablesByType(revType)
        return {'result': revRows}

    return {'error': 'ERROR_NOT_YET_IMPLEMENTED'}


@app.route("/companies", methods=['POST', 'GET'])
def companies():
    if request.method != 'POST' and request.method != 'GET':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    auth.checkValidToken(token)

    if request.method == 'POST':
        # Create company
        revType = request.args.get('type')
        if revType != 'Company':
            return {'error': 'ERROR_NOT_COMPANY_TYPE'}

        name = request.args.get('name')

        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))

        # TODO: Obtain bytes from request body, upload to storage service, obtain URL, save it and return it.
        # imageURL = request.args.get('image')
        imageURL = 'https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-images-product-6_large.png'

        newCompany = Reviewable(id=None, name=name, type=revType, imageURL=imageURL, manufacturer=None, lat=lat, lon=lon)
        try:
            newCompany.insert()
            return {'status': 'success'}

        except dbp.FailedToInsertReviewableException:
            return {'error': 'ERROR_FAILED_TO_CREATE_COMPANY'}

    return {'error': 'ERROR_NOT_YET_IMPLEMENTED'}


@app.route("/products/<id>/answer")
def answerQuestion(id):
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        questionId = request.args.get('questionId')
        chosenOption = request.args.get('chosenOption')

        product = Reviewable(id, 'a', 1, 'testURL', 'das', 1, 1)
        product.answerQuestion(questionId, id, token, chosenOption)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


if __name__ == "__main__":
    app.debug = True
    app.run()
