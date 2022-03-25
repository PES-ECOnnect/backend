import sqlite3

from flask import Flask, request

# Domain Layer
import domain.Authenticator as auth

from domain.Reviewable import *
from domain.Question import *

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


'''
products
- invalid token
- if no type -> all except company
- if type -> all of type, empty if none
    - error: ERROR_TYPE_NOT_EXISTS


create
- product exists -> ERROR_PRODUCT_EXISTS / ERROR_COMPANY_EXISTS
- si type no existeix -> ERROR_TYPE_NOT_EXISTS
'''


@app.route("/companies", methods=['POST', 'GET'])
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

        if revType == "Company":
            newReviewable = Reviewable(id=None, name=name, type=revType, imageURL=imageURL, manufacturer=None,
                                       lat=lat,
                                       lon=lon)
        else:
            newReviewable = Reviewable(id=None, name=name, type=revType, imageURL=imageURL,
                                       manufacturer=manufacturer,
                                       lat=None, lon=None)
        try:
            newReviewable.insert()
            return {'status': 'success'}

        except dbp.FailedToInsertReviewableException:
            return {'error': 'ERROR_FAILED_TO_CREATE_REVIEWABLE'}

    elif request.method == 'GET':
        revRows = getReviewablesByType(revType)
        return {'result': revRows}

    return {'error': 'ERROR_SOMETHING_WENT_WRONG'}


@app.route("/companies/<id>/answer", methods=['POST'])
@app.route("/products/<id>/answer", methods=['POST'])
def answerQuestion(id):
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        questionIndex = request.args.get('questionIndex')
        chosenOption = request.args.get('chosenOption')

        reviewable = Reviewable(id, 'a', 1, 'testURL', 'das', 1, 1)
        reviewable.answerQuestion(id, token, chosenOption, questionIndex)

        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/companies/<id>/review", methods=['POST'])
@app.route("/products/<id>/review", methods=['POST'])
def reviewReviewable(id):
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        review = request.args.get('review')

        reviewable = Reviewable(id, 'a', 1, 'testURL', 'das', 1, 1)
        reviewable.review(id, token, review)

        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/types/new", methods=['POST'])
def newProductType():
    if request.method != 'POST':
        return {'error': 'INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    auth.checkValidToken(token)
    name = request.args.get('name')

    try:
        q = request.args.get('questions')


        createType(name)

        id = getTypeIdByName(name)
        typeId = id['TypeId']
            # hardcoded just for test
        newQuestion = Question(typeId, q, 1)
        newQuestion.insert()

        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/types", methods=['GET'])
def getProductTypes():
    if request.method != 'GET':
        return {'error': 'INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        result = getAllReviewableTypes()
        # {'name': 'NOM', 'preguntes': [{'idx': 'b', 'text': 'TEXT'}, {'idx': 'b', 'text': 'TEXT'}]}
        return {'result':result}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/companies/<id>")
@app.route("/products/<id>")
def getReviewable(id):
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        # return name, image, manufacturer, type, ratings[5], vector, questions{text,num_yes, num_no}
        return getProduct(id)
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    except dbr.IdWrongTypeException:
        return {'error': 'ID_WRONG_TYPE'}
    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_INCORRECT_ID_REVIEWABLE'}


if __name__ == "__main__":
    app.debug = True
    app.run()
