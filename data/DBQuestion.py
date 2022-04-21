from data.DBUtils import *
from data.DBSession import getUserIdForToken


# def modifyQuestion()
# def deleteQuestion()
# @def getInfo()


def insertQuestion(typeId, statement):
    '''
    iQuery = "INSERT INTO question (typeid, statement, questionid) VALUES (%s, %s, %s)"
    res = insert(query=iQuery, args=(str(typeId), statement, index))
    if type(res) == bool and not res:
        raise FailedToAddQuestionException()
    '''
    res = insert("INSERT INTO question (typeid, statement) VALUES (%s, %s)", (typeId, statement))
    if type(res) == bool and not res:
        raise FailedToAddQuestionException()

def getQuestionsFromType(typeId):
    sQuery = "SELECT questionid, statement FROM question WHERE typeid = %s"
    qResult = select(sQuery, (typeId,), False)
    result = []
    if qResult is not None:
        for qr in qResult:
            result.append(qr)
    return result


# Returns the Statement, the number of yes answers, and number of no answers. Also return the answer of the logged user
def getQuestions(idReviewable, TypeId, token):
    Result = []
    idUser = getUserIdForToken(token)
    q = "SELECT questionid, statement FROM question WHERE typeid = %s"
    quest = select(q, (TypeId,), one=False)
    for i in quest:
        questionid = i['questionid']
        q = "SELECT COUNT(*) from answer where idreviewable = %s AND questionid = %s AND " \
            "chosenoption = 1 "
        yes = select(q, (idReviewable, questionid), one=True)
        q = "SELECT COUNT(*) from answer where idreviewable = %s AND questionid = %s  AND " \
            "chosenoption = 0 "
        no = select(q, (idReviewable, questionid), one=True)
        
        q = "SELECT chosenoption FROM answer WHERE idreviewable = %s AND iduser = %s AND questionid = %s"
        userAns = select(q, (idReviewable, idUser, questionid), one=True)
        
        if userAns is None:
            userAns_str = "none"
        elif userAns['chosenoption'] == 1:
            userAns_str = "yes"
        elif userAns['chosenoption'] == 0:
            userAns_str = "no"
        else:
            raise InvalidAnswerException()

        Result.append({
            'text': i["statement"].strip(),
            'num_yes': yes["count"],
            'num_no': no["count"],
            'user_answer': userAns_str
        })
    return Result


# EXCEPTIONS

class FailedToAddQuestionException(Exception):
    pass

class InvalidAnswerException(Exception):
    pass
