
from data.DBProduct import *

class Product:
    def __init__(self, id, name, typeId):
        self._id = id
        self._name = name
        self._typeId = typeId

    def answerQuestion(self, questionId, productId, token, chosenOption):
        dbp = DBProduct()
        return dbp.answer(questionId, productId, token, chosenOption)
