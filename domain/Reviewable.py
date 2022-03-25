import data.DBReviewable as dbr
import data.DBReviewableType as dbrt
import data.DBQuestion as dbq


def getReviewablesByType(type):
    return dbr.selectByType(type)

def createType(name):
    return dbrt.insertType(name)

def getTypeIdByName(typeName) ->int:
    id = dbrt.getReviewableIdForType(typeName)
    if id is None:
        raise IncorrectReviewableTypeException()
    return id

def getAllReviewableTypes():
    types = dbrt.getAllReviewableTypes()
    result = []
    for t in types:
        questions = dbq.getQuestionsFromType(int(t['TypeId']))
        aux = {}
        aux['name'] = t['name']
        aux['questions'] = questions
        result.append(aux)
    return result

def getProduct(id):
    attribs = dbr.getReviewableAttributes(id)
    # ratings MIRAR QUERY
    Ratings = []
    for i in range(6):
        Ratings.append(dbr.getRatings(id, i))
    # type
    TypeName = dbr.getTypeName(id)
    # QUESTIONS
    Questions = dbq.getQuestions(id,attribs["TypeId"])

    if TypeName["name"] == "Company":
        localization = dbr.getLocalization(id)
        return {'name': attribs["name"],
                'image': attribs["imageURL"],
                'latitude': localization["lat"],
                'longitude': localization["lon"],
                'type': TypeName["name"],
                'ratings': Ratings,
                'questions': Questions}

    else:
        manufacturer = dbr.getManufacturer(id)
        return {'name': attribs["name"],
                'image': attribs["imageURL"],
                'manufacturer': manufacturer["Manufacturer"],
                'type': TypeName["name"],
                'ratings': Ratings,
                'questions': Questions}

def getRatings(idReviewable):
    return dbr.getRatings(idReviewable)

def getQuestionsCompany():
    typeId = dbrt.getReviewableIdForType("Company")
    id = typeId['TypeId']
    return dbq.getQuestionsFromType(id)

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

