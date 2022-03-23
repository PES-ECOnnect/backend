import data.DBQuestion as dbq

class Question:

    '''
    @def modifyQuestion()
    @def deleteQuestion()
    @def getInfo()
    '''

    def __init__(self, typeId, statement, index):
        self._typeId = typeId
        self._statement = statement
        self._index = index

    def insert(self):
        return dbq.insertQuestion(typeId=self._typeId, statement=self._statement, index=self._index)