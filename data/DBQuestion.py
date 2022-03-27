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
    sQuery = "SELECT Statement FROM Question WHERE idTipus = (?)"
    qResult = selectQuery(sQuery, (typeId,), False)
    result = []
    if qResult is not None:
        for qr in qResult:
            result.append(qr['Statement'])
    return result

#Returns the Statement, the number of yes answers, and number of no answers
def getQuestions(idReviewable,TypeId):
    Result = []
    q = "SELECT QuestIndex, Statement FROM Question WHERE idTipus = (?)"
    quest = selectQuery(q, (TypeId,), False)
    for i in quest:
        q = "SELECT COUNT() from Answer where idReviewable = (?) AND QuestionIndex = (?) AND idTipus = (?) AND ChosenOption = 1"
        yes = selectQuery(q,(idReviewable,i["QuestIndex"],TypeId),False)
        q = "SELECT COUNT() from Answer where idReviewable = (?) AND QuestionIndex = (?) AND idTipus = (?) AND ChosenOption = 0"
        no = selectQuery(q, (idReviewable, i["QuestIndex"], TypeId), False)
        Result.append({
            'text': i["Statement"],
            'num_yes': yes[0]["COUNT()"],
            'num_no': no[0]["COUNT()"]
        })
    return Result


# EXCEPTIONS

class FailedToAddQuestionException(Exception):
    pass