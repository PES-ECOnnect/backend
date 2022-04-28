from data.DBUtils import *


def getReviewableTypeId(typeName: str) -> int:
    q = "SELECT typeid FROM reviewabletype WHERE name = %s"
    row = select(q, (typeName,), True)
    return None if row is None else row['typeid']


def insertType(name):
    res = insert("INSERT INTO reviewabletype (name) VALUES (%s)", (name, ))
    if type(res) == bool and not res:
        raise TypeAlreadyExistsException()


def getAllReviewableTypes():
    # TODO: Add questions
    # select r.name, q.QuestIndex, q.Statement from Question q, ReviewableType r where r.TypeId = q.idTipus
    sQuery = "SELECT * FROM ReviewableType WHERE name <>'Company'"
    return select(sQuery, (), False)


def updateProductType(id, newName):
    q = "UPDATE reviewabletype SET name = %s WHERE typeid = %s"
    result = update(query=q, args=(newName, id))
    if not result:
        raise TypeAlreadyExistsException()

def deleteProductType(id):
    q = "DELETE FROM reviewabletype WHERE typeid = %s"
    return delete(query=q, args=(id,))


# EXCEPTIONS

class TypeAlreadyExistsException(Exception):
    pass

  
class InvalidTypeNameException(Exception):
    pass

