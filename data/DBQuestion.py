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
    sQuery = "SELECT questionid, statement FROM question WHERE typeid = %s ORDER BY (questionid)"
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
    q = "SELECT questionid, statement FROM question WHERE typeid = %s ORDER BY (questionid)"
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
            'questionid': questionid,
            'user_answer': userAns_str
        })
    return Result


def updateQuestion(id, newQuestion):
    q = "UPDATE question SET statement = %s WHERE questionid = %s"
    return update(query=q, args=(newQuestion, id))


def deleteQuestion(id):
    q = "DELETE FROM question WHERE questionid = %s"
    return delete(query=q, args=(id,))

# EXCEPTIONS

class FailedToAddQuestionException(Exception):
    pass

class InvalidAnswerException(Exception):
    pass
