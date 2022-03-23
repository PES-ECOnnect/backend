from data.DBUtils import *

#def modifyQuestion()
#def deleteQuestion()
# @def getInfo()


def insertQuestion(typeId, statement, index):
    iQuery = "INSERT INTO Question (idTipus, Statement, QuestIndex) VALUES ((?), (?), (?))"
    res = insertQuery(query=iQuery, args=(str(typeId), statement, index))
    if res == False:
        raise FailedToAddQuestionException()

def getQuestionsFromType(typeId):
    sQuery = "SELECT Statement, QuestIndex FROM Question WHERE idTipus = (?)"
    return selectQuery(sQuery, (typeId,), False)


