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

app = Flask(__name__)

def anyNoneIn(l: list) -> bool:
    return any(x is None for x in l)


@app.route("/")
def helloWorld():
    return "PES Econnect Root!"


@app.route("/account", methods=['POST', 'GET'])
def signUp():
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    if anyNoneIn([email, username, password]):
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


@app.route("/account", methods=['GET'])
def getCurrentUserInfo():
    token = request.args.get("token")
    if anyNoneIn([token]):
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
    email = request.args.get('email')
    passwordString = request.args.get('password')
    if any(x is None for x in [email, passwordString]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        u = auth.getUserForEmail(email)
        if u.isBanned():
            return {'error': 'ERROR_BANNED'}

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
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}     

    try:
        auth.checkValidToken(token)
        u = auth.getUserForToken(token)
        return {'result': 'true'} if u.isAdmin() else {'result': 'false'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/account/logout", methods=['GET'])
def logout():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        auth.logOut(token)
        return {'status': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/users/<id>", methods=['GET'])
def getUserInfo(id):
    try:
        user = auth.getUserForId(id)
        if user.getIsPrivate():
            return {'error': 'ERROR_PRIVATE_USER'}
        
        return {
            'username': user.getName(),
            'medals': user.getUnlockedMedals()
        }

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/users/<uid>/ban", methods=['GET'])
def userIsBanned(uid):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        u = auth.getUserForId(uid)
        return {'result': u.isBanned()}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except auth.InvalidUserIdException:
        return {'error': 'ERROR_USER_NOT_EXISTS'}

    except Exception:
        return {'error': 'ERROR_SOMETHING_WENT_WRONG'}


@app.route("/account/email", methods=['PUT'])
def updateEmail():
    token = request.args.get('token')
    newEmail = request.args.get('newEmail')

    if anyNoneIn([token, newEmail]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
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
    token = request.args.get('token')
    newUsername = request.args.get('newUsername')

    if anyNoneIn([token, newUsername]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setUsername(newUsername)
        return {'status': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    
    except dbu.UsernameExistsException:
        return {'error': 'ERROR_USERNAME_EXISTS'}


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


@app.route("/account/password", methods=['PUT'])
def updatePassword():
    token = request.args.get('token')
    oldPassword = request.args.get('oldPassword')
    newPassword = request.args.get('newPassword')

    if anyNoneIn([token, oldPassword, newPassword]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        oldEncryptedPwd = hashlib.sha256(oldPassword.encode('UTF-8')).hexdigest()
        user = auth.getUserForToken(token)

        if user.validatePassword(oldEncryptedPwd):
            enNewPass = hashlib.sha256(newPassword.encode('UTF-8')).hexdigest()
            user.setPassword(enNewPass)
            return {'status': 'success'}
        
        else:
            return {'error': 'ERROR_INCORRECT_PASSWORD'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/account/visibility", methods=['PUT'])
def updateVisibility():
    token = request.args.get('token')
    isPrivate = request.args.get('isPrivate')

    if anyNoneIn([token, isPrivate]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setVisibility(isPrivate)
        return {'status': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/account/medal", methods=['PUT'])
def updateActiveMedal():
    token = request.args.get('token')
    medalId = request.args.get('medalId')
    if anyNoneIn([token, medalId]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        
        if user.hasUnlockedMedal(medalId):
            user.setActiveMedal(medalId)
            return {'status': 'success'}
        
        return {'error': 'ERROR_USER_INVALID_MEDAL'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/account", methods=['DELETE'])
def deleteAccount():
    token = request.args.get('token')
    pwd = request.args.get('password')
    if anyNoneIn([token, pwd]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        if user.validatePassword(pwd):
            user.deleteUser(token)
            return {'status': 'success'}
        return {'error': 'ERROR_INCORRECT_PASSWORD'}

    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@app.route("/users/<id>/ban", methods=['POST'])
def banAccount(id):
    token = request.args.get('token')
    isBanned = request.args.get('isBanned')
    if anyNoneIn([token, isBanned]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        
        if not user.isAdmin():
            return {'error': 'ERROR_USER_NOT_ADMIN'}
        
        if user.getId() == int(id):
            return {'error': 'ERROR_CANNOT_BAN_YOURSELF'}
        
        user.banUser(id, isBanned)
        return {'status': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/companies", methods=['POST', 'GET'])
@app.route("/products", methods=['POST', 'GET'])
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
        manufacturer = request.args.get('manufacturer')
        imageURL = request.args.get('image')
        if anyNoneIn([reviewableName, manufacturer, imageURL]):
            return {'error': 'ERROR_INVALID_ARGUMENTS'}

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
    questionIndex = request.args.get('questionIndex')
    chosenOption = request.args.get('chosenOption')
    if anyNoneIn([token, questionIndex, chosenOption]):
            return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        reviewable = Reviewable(id, 'a', 1, 'testURL', 'das', 1, 1)
        reviewable.answerQuestion(id, token, chosenOption, questionIndex)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/companies/<id>", methods=['DELETE'])
@app.route("/products/<id>", methods=['DELETE'])
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

@app.route("/companies/<id>/review", methods=['POST'])
@app.route("/products/<id>/review", methods=['POST'])
def reviewReviewable(id):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}    

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
        return getAllReviewableTypes()



@app.route("/companies/<id>", methods=['GET'])
@app.route("/products/<id>", methods=['GET'])
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


@app.route("/companies/<id>", methods=['POST'])
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
        company = Reviewable(id, name, 'company', image, None,lat, lon)
        company.updateCompany()
        return {'status': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
    
    except dbr.FailedToUpdateCompanyException:
        return {'error': 'ERROR_COMPANY_UPDATE'}
    
    except dbr.FailedToUpdateReviewableException:
        return {'error': 'ERROR_REVIEWABLE_NAME_EXISTS'}


@app.route("/products/<id>", methods=['POST'])
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


@app.route("/companies/questions", methods=['GET'])
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


@app.route("/question/<id>", methods=['PUT'])
def updateQuestion(id):
    token = request.args.get('token')
    newQuestion = request.args.get('newQuestion')

    if anyNoneIn([token, newQuestion]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'} 

    try:
        auth.checkValidToken(token)
        result = updateQuestionName(id, newQuestion)
        return {'result': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/question/<id>", methods=['DELETE'])
def deleteQuestion(id):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        result = deleteProductTypeQuestion(id)
        if not result:
            return {'error': 'ERROR_INCORRECT_QUESTION'}
        
        return {'result': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/posts", methods=['POST'])
def NewPost():
    token = request.args.get('token')
    text = request.args.get('text')
    image = request.args.get('image')

    if anyNoneIn([token, text, image]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        
        # Extract and save the post's hashtags 
        tags = obtainTags(text)
        saveTags(tags)

        # Creation of the post
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
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

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
    isLike = (request.args.get('isLike').lower() == "true") if request.args.get('isLike') is not None else None 
    remove = (request.args.get('remove').lower() == "true") if request.args.get('remove') is not None else None

    if anyNoneIn([token, isLike, remove]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        like(token, id, isLike, remove)
        return {'status': 'success'}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/posts/tags", methods=['GET'])
def getAllTags():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        return {'result': getUsedTags()}
    
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/posts", methods=['GET'])
def getPosts():
    token = request.args.get('token')
    num = request.args.get('n')
    
    if anyNoneIn([token, num]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        tag = request.args.get('tag') if 'tag' in request.args.keys() else None

        return {
            'result': getNPosts(token, num, tag)
        }

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@app.route("/questions", methods=['POST'])
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

@app.route("/companies/quiestions", methods=['POST'])
def createCompanyQuestion():
    token = request.args.get('token')
    statement = request.args.get('statement')

    if anyNoneIn([token, statement]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken()
        typeId = getReviewableTypeIdByName('Company')
        question = Question(typeId, statement)
        question.insert()
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
