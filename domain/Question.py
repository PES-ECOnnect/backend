import data.DBQuestion as dbq


def updateQuestionName(id, newQuestion):
    return dbq.updateQuestion(id, newQuestion)


def deleteProductTypeQuestion(id):
    return dbq.deleteQuestion(id)



class Question:
    """
    @def modifyQuestion()
    @def deleteQuestion()
    @def getInfo()
    """

    def __init__(self, typeId, statement):
        self._typeId = typeId
        self._statement = statement

    def insert(self):
        return dbq.insertQuestion(typeId=self._typeId, statement=self._statement)
