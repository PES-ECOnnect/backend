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
        token = auth.logIn(email, password)
        return {'status': 'success',
                'token': str(token)}

    except sqlite3.Error:
        return {'error': 'ERROR_FAILED_SIGN_UP'}

    except dbs.FailedToOpenSessionException:
        return json.dumps({'error': 'ERROR_STARTING_USER_SESSION'})


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
    try:
        auth.checkValidToken(token)
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    revType = request.args.get('type')
    if revType is None:
        revType = "Company"

    try:
        getReviewableTypeIdByName(revType)
    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_TYPE_NOT_EXISTS'}

    name = request.args.get('name')

    if request.method == 'POST':
        # Create product

        manufacturer = request.args.get('manufacturer')
        # TODO: Obtain bytes from request body, upload to storage service, obtain URL, save it and return it.
        # imageURL = request.args.get('image')
        imageURL = 'https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-images-product-6_large.png'

        if revType == "Company":
            lat = request.args.get('lat')
            lon = request.args.get('lon')
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
        revRows = []
        if revType != "":
            revRows = getReviewablesByType(revType)
        else:
            types = getAllReviewableTypes()
            for t in types:
                typeName = t["name"]
                if typeName == "Company":
                    continue  # don't include companies
                typeProducts = getReviewablesByType(typeName)
                revRows += typeProducts
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


@app.route("/products/types", methods=['POST', 'GET'])
def newProductType():
    if request.method != 'POST' and request.method != 'GET':
        return {'error': 'INVALID_REQUEST_METHOD'}

    if request.method == 'POST':

        token = request.args.get('token')
        try:
            auth.checkValidToken(token)
        except dbs.InvalidTokenException:
            return {'error': 'ERROR_INVALID_TOKEN'}

        name = request.args.get('name')

        try:
            createType(name)
            revTypeId = getReviewableTypeIdByName(name)

            reqData = request.get_json()
            questions = reqData['questions']

            index = 1
            for q in questions:
                newQuestion = Question(revTypeId, q, index)
                newQuestion.insert()
                index += 1

            return {'status': 'success'}

        except dbrt.TypeAlreadyExistsException:
            return {'error': 'TYPE_EXISTS'}

    elif request.method == 'GET':
        token = request.args.get('token')
        try:
            auth.checkValidToken(token)
            result = getAllReviewableTypes()
            # {'name': 'NOM', 'preguntes': [{'idx': 'b', 'text': 'TEXT'}, {'idx': 'b', 'text': 'TEXT'}]}
            return {'result': result}
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


@app.route("/companies/questions", methods=['GET'])
def getCompanyQuestions():
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        questions = getQuestionsCompany()
        return {'result': questions}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


if __name__ == "__main__":
    app.debug = True
    app.run()
