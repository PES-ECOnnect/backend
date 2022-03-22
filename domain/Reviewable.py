import data.DBReviewable as dbp


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
        return dbp.answer(questionId, productId, token, chosenOption)

    def insert(self):
        dbp.insert(name=self._name, revType=self._type, imageURL=self._imageURL, manufacturer=self._manufacturer, lat=self._lat, lon=self._lon)

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
