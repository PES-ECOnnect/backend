import traceback

import psycopg2
from flask import Flask, request

# Domain Layer
import domain.Authenticator as auth

from domain.Reviewable import *
from domain.Question import *

from domain.User import *

from domain.Forum import *

# Data Layer (TODO - Remove)
import data.DBSession as dbs
import data.DBReviewable as dbp
import data.DBUser as dbu

import json
import hashlib

app = Flask(__name__)


@app.route("/")
def helloWorld():
    return "PES Econnect Root!"


@app.route("/account", methods=['POST', 'GET'])
def signUp():
    if request.method == "POST":
        email = request.args.get('email')
        username = request.args.get('username')
        password = request.args.get('password')
        if email is None or username is None or password is None:
            return {'error': 'ERROR_INVALID_ARGUMENTS'}

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

        except auth.FailedToInsertUserException:
            return {'error': 'ERROR_FAILED_SIGN_UP'}

        except dbs.FailedToOpenSessionException:
            return json.dumps({'error': 'ERROR_STARTING_USER_SESSION'})

        except Exception:
            return json.dumps({'error': 'ERROR_SOMETHING_WENT_WRONG'})

    elif request.method == "GET":
        token = request.args.get("token")
        if token is None:
            return {'error': 'ERROR_INVALID_ARGUMENTS'}

        try:
            auth.checkValidToken(token)
            u = auth.getUserForToken(token)
            return {
                "username": u.getName(),
                "email": u.getEmail(),
                "activeMedal": u.getActiveMedalId(),
                "medals": u.getUnlockedMedals()
            }

        except dbs.InvalidTokenException:
            return {"error": "ERROR_INVALID_TOKEN"}




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

@app.route("/users/<id>", methods=['GET'])
def getUserInfo(id):
    if request.method != 'GET':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    try:


        user = auth.getUserForId(id)
        if (user.getIsPrivate()==True):
            return {'error': 'ERROR_PRIVATE_USER'}
        result = {
            'username': user.getName(),
            'medals': user.getUnlockedMedals()
        }
        return result
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/account/email", methods=['PUT'])
def updateEmail():
    if request.method != 'PUT':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD '}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        newEmail = request.args.get('newEmail')
        user = auth.getUserForToken(token)
        user.setEmail(newEmail)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    except dbu.EmailExistsException:
        return {'error': 'ERROR_EMAIL_EXISTS'}
    except dbu.InvalidEmailException:
        return {'error': 'ERROR_INVALID_EMAIL'}

@app.route("/account/username", methods=['PUT'])
def updateUsername():
    if request.method != 'PUT':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        newUsername = request.args.get('newUsername')
        user = auth.getUserForToken(token)
        user.setUsername(newUsername)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    except dbu.UsernameExistsException:
        return {'error': 'ERROR_USERNAME_EXISTS'}

@app.route("/account/home", methods=['PUT'])
def setHome():
    if request.method != 'PUT':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        newHome = request.args.get('newHome')
        user = auth.getUserForToken(token)
        user.setHome(newHome)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/account/password", methods=['PUT'])
def updatePassword():
    if request.method != 'PUT':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        oldPassword = request.args.get('oldPassword')
        oldEncryptedPwd = hashlib.sha256(oldPassword.encode('UTF-8')).hexdigest()
        user = auth.getUserForToken(token)

        if user.validatePassword(oldEncryptedPwd):
            newPassword = request.args.get('newPassword')
            enNewPass = hashlib.sha256(newPassword.encode('UTF-8')).hexdigest()
            user.setPassword(enNewPass)
            return {'status': 'success'}
        else:
            return {'error': 'ERROR_INCORRECT_PASSWORD'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/account/visibility", methods=['PUT'])
def updateVisibility():
    if request.method != 'PUT':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        isPrivate = request.args.get('isPrivate')
        user.setVisibility(isPrivate)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/account/medal", methods=['PUT'])
def updateActiveMedal():
    if request.method != 'PUT':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        medalId = request.args.get('medalId')
        user = auth.getUserForToken(token)
        if user.hasUnlockedMedal(medalId) == True:
            user.setActiveMedal(medalId)
            return {'status': 'success'}
        else:
            return {'error': 'ERROR_USER_INVALID_MEDAL'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/medals", methods=['POST'])
def createMedal():
    if request.method != 'POST':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        medalName = request.args.get('medalName')
        newMedal(medalName)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    except dbu.MedalExistsException:
        return {'error': 'ERROR_MEDAL_EXISTS'}

@app.route("/account", methods=['DELETE'])
def deleteAccount():
    if request.method != 'DELETE':
        return {'error': 'ERROR_INVALID_REQUEST_METHOD'}

    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.deleteUser(token)
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

    # check if token is valid
    token = request.args.get('token')
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

    reviewableName = request.args.get('name')

    if request.method == 'POST':
        # Create product

        manufacturer = request.args.get('manufacturer')
        # TODO: Obtain bytes from request body, upload to storage service, obtain URL, save it and return it.
        # imageURL = request.args.get('image')
        imageURL = 'https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-images-product-6_large.png'

        if revType == "Company":
            lat = request.args.get('lat')
            lon = request.args.get('lon')
            newReviewable = Reviewable(id=None, name=reviewableName, type=revType, imageURL=imageURL, manufacturer=None,
                                       lat=lat,
                                       lon=lon)
        else:
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

            index = 0
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
        # return name, image, manufacturer, type, ratings[5], vector, questions{text,num_yes, num_no, user_answer}
        return getProduct(id, token)
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


@app.route("/posts", methods=['POST'])
def NewPost():
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        text = request.args.get('text')

        tags = obtainTags(text)
        saveTags(tags)

        image = request.args.get('image')
        createPost(token, text, image, tags)

        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    except dbf.InsertionErrorException:
        return {'error': 'ERROR_INCORRECT_INSERTION'}
    except Exception:
        return {'error': 'ERROR_SOMETHING_WENT_WRONG', 'traceback': traceback.format_exc()}

      
@app.route("/posts/<id>", methods=['DELETE'])
def DeletePost(id):
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        userId = user.getId()
        deletePost(userId, id)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    except dbf.UserNotPostOwnerException:
        return {'error': 'ERROR_USER_NOT_POST_OWNER'}
    except dbf.DeletingLikesDislikesException:
        return {'error': 'ERROR_DELETING_LIKES_DISLIKES'}
    except dbf.DeletingPostHashtagsException:
        return {'error': 'ERROR_DELETING_LIKES_DISLIKES'}
    except dbf.DeletingPostException:
        return {'error': 'ERROR_DELETING_POST'}


@app.route("/posts/<id>/like", methods=['POST'])
def likePost(id):
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        isLike = request.args.get('isLike').lower() == "true"
        remove = request.args.get('remove').lower() == "true"
        like(token, id, isLike, remove)
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/posts/tags", methods=['GET'])
def getAllTags():
    token = request.args.get('token')
    try:
        auth.checkValidToken(token)
        x = getUsedTags()
        return {'result': x}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/posts", methods=['GET'])
def getPosts():
    # Get and check request MANDATORY arguments are valid (TODO -> for all endpoints)
    token = request.args.get('token')
    num = request.args.get('n')
    if any(x is None for x in [num, token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        tag = request.args.get('tag') if 'tag' in request.args.keys() else None

        return {
            'result': getNPosts(token, num, tag)
        }

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
