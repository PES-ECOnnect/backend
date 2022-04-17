from data.DBUtils import *


def getReviewableTypeId(typeName: str) -> int:
    q = "SELECT typeid FROM reviewabletype WHERE name = %s"
    row = select(q, (typeName,), True)
    return None if row is None else row['typeid']


def insertType(name):
    con = getCon()
    c = con.cursor()
    c.execute("begin")
    try:
        c.execute("INSERT INTO reviewabletype (name) VALUES %s", (name,))
        c.execute('commit')
    except con.Error:
        c.execute('rollback')
        raise TypeAlreadyExistsException()


def getAllReviewableTypes():
    # TODO: Add questions
    # select r.name, q.QuestIndex, q.Statement from Question q, ReviewableType r where r.TypeId = q.idTipus
    sQuery = "SELECT * FROM ReviewableType WHERE name <>'Company'"
    return select(sQuery, (), False)


# EXCEPTIONS

class TypeAlreadyExistsException(Exception):
    pass

  
class InvalidTypeNameException(Exception):
    pass

