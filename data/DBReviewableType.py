from data.DBUtils import *


def getReviewableTypeId(typeName: str) -> int:
    q = "SELECT TypeId FROM ReviewableType WHERE name = ?"
    row = selectQuery(q, (typeName,), True)
    return None if row is None else row['TypeId']



def insertType(name):
    con = getCon()
    c = con.cursor()
    c.execute("begin")
    try:
        c.execute("INSERT INTO reviewableType (name) VALUES (?)", (name, ))
        c.execute('commit')
    except con.Error:
        c.execute('rollback')
        raise TypeAlreadyExistsException()


def getAllReviewableTypes():
    # TODO: Add questions
    # select r.name, q.QuestIndex, q.Statement from Question q, ReviewableType r where r.TypeId = q.idTipus
    sQuery = "SELECT * FROM ReviewableType WHERE name <>'Company'"
    return selectQuery(sQuery, (), False)


# EXCEPTIONS

class TypeAlreadyExistsException(Exception):
    pass

class IndavlidTypeNameException(Exception):
    pass



