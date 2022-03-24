import data.DBReviewable as dbr


def getReviewablesByType(type):
    return dbr.selectByType(type)

'''def infoProduct(self, id):
    dbp = DBProduct()
    # return name, image, manufacturer, type, ratings[5], vector, questions{text,num_yes, num_no}
    TypeName =  # select type
    if TypeName == "company":
        # not return manufacturer
    else:
        # add manufacturer
    prod = #select de nom+manufacturer+
    ratings[0..5] = # select ratings
    questions(num_yes num_no) = #select questions from... -> select answers yes + no'''

def getProduct(id):
    TypeName = dbr.getTypeName(id)
    if TypeName == "company":
        # localization
    else:
        # manufacturer
    # ratings MIRAR QUERY
    # QUESTIONS

def getRatings(idReviewable):
    return dbr.getRatings(idReviewable)




class Reviewable:
    def __init__(self, id, name, type, imageURL, manufacturer, lat, lon):
        self._id = id
        self._name = name
        self._type = type
        self._imageURL = imageURL
        self._manufacturer = manufacturer
        self._lat = lat
        self._lon = lon

    def answerQuestion(self, questionId, productId, token, chosenOption):
        return dbr.answer(questionId, productId, token, chosenOption)

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

