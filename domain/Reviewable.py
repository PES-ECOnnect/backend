import data.DBReviewable as dbr
import data.DBReviewableType as dbrt
import data.DBQuestion as dbq
import domain.Authenticator as auth

def getReviewablesByType(type):
    return dbr.selectByType(type)


def getAllProducts():
    return dbr.selectProducts()


def createType(name):
    return dbrt.insertType(name)


def getReviewableTypeIdByName(typeName) -> int:
    revTypeId = dbrt.getReviewableTypeId(typeName)
    if revTypeId is None:
        raise dbr.IncorrectReviewableTypeException()
    return revTypeId

def updateProductTypeName(typeId, newName):
    return dbrt.updateProductType(typeId, newName)


def deleteProductTypeByName(typeName):
    typeId = getReviewableTypeIdByName(typeName)
    return dbrt.deleteProductType(typeId)

def getAllReviewableTypes():
    types = dbrt.getAllReviewableTypes()
    result = []
    for t in types:
        questions = dbq.getQuestionsFromType(int(t['typeid']))
        aux = {'name': t['name'], 'questions': questions}
        result.append(aux)
    return result


def getProduct(id, token):
    attribs = dbr.getReviewableAttributes(id)
    # ratings
    Ratings = []
    for i in range(6):
        Ratings.append(dbr.getRatings(id, i))
    # type
    TypeName = dbr.getTypeName(id)
    # QUESTIONS
    Questions = dbq.getQuestions(id, attribs["typeid"], token)

    user = auth.getUserForToken(token)
    userRate = dbr.getUserRate(id, user.getId())
    if userRate is None:
        userRate = 0

    if TypeName == "Company":
        localization = dbr.getLocalization(id)
        return {'name': attribs["name"],
                'imageURL': attribs["imageurl"],
                'latitude': localization["lat"],
                'longitude': localization["lon"],
                'type': TypeName,
                'ratings': Ratings,
                'questions': Questions,
                'userRate': userRate}

    else:
        manufacturer = dbr.getManufacturer(id)
        return {'name': attribs["name"],
                'imageURL': attribs["imageurl"],
                'manufacturer': manufacturer["manufacturer"],
                'type': TypeName,
                'ratings': Ratings,
                'questions': Questions,
                'userRate': userRate}


def getRatings(idReviewable):
    return dbr.getRatings(idReviewable)


def getQuestionsCompany():
    typeId = dbrt.getReviewableTypeId("Company")
    return dbq.getQuestionsFromType(typeId)

def deleteUserAnswers(userId):
    return dbr.deleteUserAnswers(userId)

def deleteUserReviews(userId):
    return dbr.deleteUserReviews(userId)

def deleteReviewable(idreviewable):
    return dbr.deleteReviewable(idreviewable)


class Reviewable:
    def __init__(self, id, name, type, imageURL, manufacturer, lat, lon):
        self._id = id
        self._name = name
        self._type = type
        self._imageURL = imageURL
        self._manufacturer = manufacturer
        self._lat = lat
        self._lon = lon

    def answerQuestion(self, productId, token, chosenOption, questionIndex):
        return dbr.answer(productId, token, chosenOption, questionIndex)

    def review(self, productId, token, review):
        return dbr.review(productId, token, review)

    def insert(self):
        dbr.insert(name=self._name, revType=self._type, imageURL=self._imageURL, manufacturer=self._manufacturer,
                   lat=self._lat, lon=self._lon)

    def getId(self):
        return self._id

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getManufacturer(self):
        return self._manufacturer

    def getImageURL(self):
        return self._imageURL

    def getLat(self):
        return self._lat

    def getLon(self):
        return self._lon

    def updateCompany(self):
        return dbr.updateCompany(self._name, self._imageURL, self._lat, self._lon,self._id)

    def updateProduct(self):
        typeid = getReviewableTypeIdByName(self._type)
        return dbr.updateProduct(self._name, typeid, self._imageURL, self._manufacturer, self._id)