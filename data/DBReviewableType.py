from data.DBUtils import *


def getReviewableIdForType(typeName: str) -> int:
    q = "SELECT TypeId FROM ReviewableType WHERE name = ?"
    return selectQuery(q, (typeName,), True)

def insertType(name):
    iQuery = "INSERT INTO reviewableType (name) VALUES (?)"
    res = insertQuery(query=iQuery, args=(name, ))
    if res == False:
        raise FailedToAddReviewableTypeException()

def getAllReviewableTypes():
    # TODO: Add questions
    # select r.name, q.QuestIndex, q.Statement from Question q, ReviewableType r where r.TypeId = q.idTipus
    sQuery = "SELECT * FROM ReviewableType WHERE name <>'Company'"
    return selectQuery(sQuery, (), False)



