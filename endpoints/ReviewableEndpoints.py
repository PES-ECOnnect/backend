# Import Blueprint
from flask import Flask, request
from flask import Blueprint
reviewable_endpoint = Blueprint('reviewable_endpoint', __name__, template_folder='templates')

# Domain Layer
import domain.Authenticator as auth

from domain.Reviewable import *
from domain.Question import *

from domain.User import *
from domain.Question import *
from domain.Forum import *
from domain.Medal import *

# Data Layer (TODO - Remove)
import data.DBSession as dbs
import data.DBReviewable as dbp
import data.DBUser as dbu

import json
import hashlib

def anyNoneIn(l: list) -> bool:
    return any(x is None for x in l)


@reviewable_endpoint.route("/companies", methods=['POST', 'GET'])
@reviewable_endpoint.route("/products", methods=['POST', 'GET'])
def products():
    # check if token is valid
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    # check if we are working with a company or a product
    if str(request.url_rule) == "/products":
        revType = request.args.get('type')
        if revType == "Company":
            return {'error': 'ERROR_INVALID_ARGUMENTS'}
    else:
        revType = "Company"

    if revType is None:
        if str(request.url_rule) == "/products":
            return {'error': 'ERROR_INVALID_ARGUMENTS'}  # missing the type argument
        else:
            revType = "Company"

    # check if the reviewable type is valid (either "Company" or some valid product type)
    try:
        if revType != "":
            getReviewableTypeIdByName(revType)

    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_TYPE_NOT_EXISTS'}

    if request.method == 'POST':
        # Create product

        reviewableName = request.args.get('name')
        imageURL = request.args.get('imageURL')
        if anyNoneIn([reviewableName, imageURL]):
            return {'error': 'ERROR_INVALID_ARGUMENTS'}

        if revType == "Company":
            lat = request.args.get('lat')
            lon = request.args.get('lon')
            newReviewable = Reviewable(id=None, name=reviewableName, type=revType, imageURL=imageURL, manufacturer=None,
                                       lat=lat,
                                       lon=lon)
        else:
            manufacturer = request.args.get('manufacturer')
            if anyNoneIn([manufacturer]):
                return {'error': 'ERROR_INVALID_ARGUMENTS'}

            newReviewable = Reviewable(id=None, name=reviewableName, type=revType, imageURL=imageURL,
                                       manufacturer=manufacturer,
                                       lat=None, lon=None)
        try:
            newReviewable.insert()
            return {'status': 'success'}

        except dbp.FailedToInsertReviewableException:
            return {'error': 'ERROR_FAILED_TO_CREATE_REVIEWABLE'}

        except dbp.ReviewableAlreadyExistsException:
            return {'error': 'ERROR_COMPANY_EXISTS' if revType == 'Company' else 'ERROR_PRODUCT_EXISTS'}

    elif request.method == 'GET':

        if revType == "":  # All products of all types
            revRows = getAllProducts()

        else:  # All Companies or all Products of type revType
            revRows = getReviewablesByType(revType)

        return {'result': revRows}

    return {'error': 'ERROR_SOMETHING_WENT_WRONG'}


@reviewable_endpoint.route("/companies/<id>/answer", methods=['POST'])
@reviewable_endpoint.route("/products/<id>/answer", methods=['POST'])
def answerQuestion(id):
    token = request.args.get('token')
    questionIndex = request.args.get('questionIndex')
    chosenOption = request.args.get('chosenOption')
    if anyNoneIn([token, questionIndex, chosenOption]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        reviewable = Reviewable(id, 'a', 1, 'testURL', 'das', 1, 1)
        reviewable.answerQuestion(id, token, chosenOption, questionIndex)
        idMedal = checkQuestionMedals(token)
        return {'status': 'success',
                'medal': idMedal}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@reviewable_endpoint.route("/companies/<id>", methods=['DELETE'])
@reviewable_endpoint.route("/products/<id>", methods=['DELETE'])
def removeReviewable(id):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        if not user.isAdmin():
            return {'error': 'ERROR_USER_NOT_ADMIN'}
        # check Reviewable exists
        dbr.getReviewableAttributes(id)

        # delete reviewable cascade
        deleteReviewable(id)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_PRODUCT_NOT_EXISTS'}


@reviewable_endpoint.route("/companies/<id>/review", methods=['POST'])
@reviewable_endpoint.route("/products/<id>/review", methods=['POST'])
def reviewReviewable(id):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        review = request.args.get('review')

        reviewable = Reviewable(id, 'a', 1, 'testURL', 'das', 1, 1)
        reviewable.review(id, token, review)
        type = dbr.getTypeName(id)
        if type == "Company":
            idMedal = checkCompanyMedals(token)
        else:
            idMedal = checkProductMedals(token)

        return {'status': 'success',
                'medal': idMedal}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@reviewable_endpoint.route("/products/types", methods=['POST', 'GET'])
def newProductType():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    if request.method == 'POST':

        name = request.args.get('name')
        reqData = request.get_json()

        if anyNoneIn([name, reqData]):
            return {'error': 'ERROR_INVALID_ARGUMENTS'}

        try:
            createType(name)
            revTypeId = getReviewableTypeIdByName(name)
            questions = reqData['questions']

            for q in questions:
                newQuestion = Question(revTypeId, q)
                newQuestion.insert()

            return {'status': 'success'}

        except dbrt.TypeAlreadyExistsException:
            return {'error': 'TYPE_EXISTS'}

    elif request.method == 'GET':
        return {'result': getAllReviewableTypes()}


@reviewable_endpoint.route("/products/types", methods=['PUT'])
def updateProductType():
    token = request.args.get('token')
    oldName = request.args.get('oldName')
    newName = request.args.get('newName')

    if anyNoneIn([token, oldName, newName]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    if oldName == "Company":
        return {'error': 'ERROR_CANNOT_UPDATE_COMPANY_TYPE_NAME'}

    try:
        auth.checkValidToken(token)
        typeId = getReviewableTypeIdByName(oldName)
        updateProductTypeName(typeId, newName)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_INVALID_TYPE_NAME'}

    except dbrt.TypeAlreadyExistsException:
        return {'error': 'ERROR_TYPE_NAME_ALREADY_EXISTS'}


@reviewable_endpoint.route("/products/types", methods=['DELETE'])
def deleteProductType():
    token = request.args.get('token')
    name = request.args.get('name')

    if anyNoneIn([token, name]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    if name == "Company":
        return {'error': 'ERROR_CANNOT_DELETE_COMPANY_TYPE'}

    try:
        auth.checkValidToken(token)
        result = deleteProductTypeByName(name)
        if not result:
            return {'error': 'ERROR_SOMETHING_WENT_WRONG'}
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_INVALID_TYPE_NAME'}


@reviewable_endpoint.route("/companies/<id>", methods=['GET'])
@reviewable_endpoint.route("/products/<id>", methods=['GET'])
def getReviewable(id):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        # return name, image, manufacturer, type, ratings[5], vector, questions{text,num_yes, num_no, user_answer}
        return getProduct(id, token)

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbr.IdWrongTypeException:
        return {'error': 'ID_WRONG_TYPE'}

    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_INCORRECT_ID_REVIEWABLE'}


@reviewable_endpoint.route("/companies/<id>", methods=['POST'])
def updateCompany(id):
    token = request.args.get('token')
    name = request.args.get('name')
    image = request.args.get('imageURL')
    lat = None if request.args.get('lat') is None else float(request.args.get('lat'))
    lon = None if request.args.get('lon') is None else float(request.args.get('lon'))

    if anyNoneIn([token, name, image, lat, lon]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        company = Reviewable(id, name, 'company', image, None, lat, lon)
        company.updateCompany()
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbr.FailedToUpdateCompanyException:
        return {'error': 'ERROR_COMPANY_UPDATE'}

    except dbr.FailedToUpdateReviewableException:
        return {'error': 'ERROR_REVIEWABLE_NAME_EXISTS'}


@reviewable_endpoint.route("/products/<id>", methods=['POST'])
def updateProduct(id):
    token = request.args.get('token')
    name = request.args.get('name')
    manufacturer = request.args.get('manufacturer')
    image = request.args.get('imageURL')
    type = request.args.get('type')

    if anyNoneIn([token, name, manufacturer, image]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        product = Reviewable(id, name, type, image, manufacturer, None, None)
        product.updateProduct()
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbr.FailedToUpdateReviewableException:
        return {'error': 'ERROR_REVIEWABLE_NAME_EXISTS'}

    except dbr.FailedToUpdateProductException:
        return {'error': 'ERROR_PRODUCT_UPDATE'}

    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_TYPE_NOT_EXISTS'}


@reviewable_endpoint.route("/companies/questions", methods=['GET'])
def getCompanyQuestions():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        questions = getQuestionsCompany()
        return {'result': questions}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@reviewable_endpoint.route("/questions/<id>", methods=['PUT'])
def updateQuestion(id):
    token = request.args.get('token')
    newQuestion = request.args.get('newQuestion')

    if anyNoneIn([token, newQuestion]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        updateQuestionName(id, newQuestion)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@reviewable_endpoint.route("/questions/<id>", methods=['DELETE'])
def deleteQuestion(id):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        result = deleteProductTypeQuestion(id)
        if not result:
            return {'error': 'ERROR_INCORRECT_QUESTION'}

        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@reviewable_endpoint.route("/questions", methods=['POST'])
def createQuestion():
    token = request.args.get('token')
    statement = request.args.get('statement')
    type = request.args.get('type')

    if anyNoneIn([token, statement, type]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        typeId = getReviewableTypeIdByName(type)
        question = Question(typeId, statement)
        question.insert()
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    except dbr.IncorrectReviewableTypeException:
        return {'error': 'ERROR_TYPE_NOT_EXISTS'}


@reviewable_endpoint.route("/companies/questions", methods=['POST'])
def createCompanyQuestion():
    token = request.args.get('token')
    statement = request.args.get('statement')

    if anyNoneIn([token, statement]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        typeId = getReviewableTypeIdByName('Company')
        question = Question(typeId, statement)
        question.insert()
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
