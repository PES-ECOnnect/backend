from data.DBUtils import *


# def modifyQuestion()
# def deleteQuestion()
# @def getInfo()


def insertQuestion(typeId, statement, index):
    iQuery = "INSERT INTO question (typeid, statement, questionindex) VALUES (%s, %s, %s)"
    res = insert(query=iQuery, args=(str(typeId), statement, index))
    if type(res) == bool and not res:
        raise FailedToAddQuestionException()


def getQuestionsFromType(typeId):
    sQuery = "SELECT statement FROM question WHERE typeid = %s"
    qResult = select(sQuery, (typeId,), False)
    result = []
    if qResult is not None:
        for qr in qResult:
            result.append(qr['statement'])
    return result


# Returns the Statement, the number of yes answers, and number of no answers
def getQuestions(idReviewable, TypeId):
    Result = []
    q = "SELECT questionindex, statement FROM question WHERE typeid = %s"
    quest = select(q, (TypeId,), False)
    for i in quest:
        q = "SELECT COUNT() from answer where idreviewable = %s AND questionindex = %s AND typeid = %s AND " \
            "chosenoption = 1 "
        yes = select(q, (idReviewable, i["questionindex"], TypeId), False)
        q = "SELECT COUNT() from answer where idreviewable = %s AND questionindex = %s AND typeid = %s AND " \
            "chosenoption = 0 "
        no = select(q, (idReviewable, i["questionindex"], TypeId), False)

        Result.append({
            'text': i["statement"],
            'num_yes': yes[0]["COUNT()"],
            'num_no': no[0]["COUNT()"]
        })
    return Result


# EXCEPTIONS

class FailedToAddQuestionException(Exception):
    pass
