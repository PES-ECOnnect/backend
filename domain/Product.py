
from data.DBProduct import *

class Product:
    def __init__(self, id, name, typeId):
        self._id = id
        self._name = name
        self._typeId = typeId

    def answerQuestion(self, idType, QuestionIndex, productId, token, chosenOption):
        dbp = DBProduct()
        return dbp.answer(idType, QuestionIndex, productId, token, chosenOption)

    def deleteQuestion(self,QuestIndex,idTipus):
        dbp = DBProduct()
        return dbp.deleteQuestion(QuestIndex, idTipus)
