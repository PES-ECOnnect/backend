from data.DBSession import *

import data.DBReviewableType as dbrt


# If revType == 'Company', we assume that lat and lon are not None
# If revType != 'Company', we assume that manufacturer is not None
def insert(name, revType, imageURL, manufacturer=None, lat=None, lon=None):
    typeRow = dbrt.getReviewableIdForType(revType)
    if typeRow is None:
        raise IncorrectReviewableTypeException()

    typeId = typeRow['TypeId']

    con = getCon()
    c = con.cursor()
    c.execute("begin")
    try:
        c.execute("INSERT INTO Reviewable (TypeId, name, imageURL) VALUES (?, ?, ?) ", (typeId, name, imageURL))
        reviewableId = c.lastrowid

        if revType == 'Company':
            c.execute("INSERT INTO InstallerCompany (ReviewableId, lat, lon) VALUES (?, ?, ?) ",
                      (reviewableId, lat, lon))
        else:
            c.execute("INSERT INTO EquipmentProduct (ReviewableId, Manufacturer) VALUES (?, ?) ",
                      (reviewableId, manufacturer))

        c.execute("commit")
    except con.Error:
        c.execute("rollback")
        raise FailedToInsertReviewableException()


def selectByType(revType):
    typeRow = dbrt.getReviewableIdForType(revType)
    if typeRow is None:
        raise IncorrectReviewableTypeException()

    typeId = typeRow['TypeId']
    q = "" \
        "SELECT *" \
        " FROM Reviewable r" \
        " JOIN %s t on t.ReviewableId = r.idReviewable" \
        " WHERE r.TypeId = ?" % ("InstallerCompany" if revType == "Company" else "EquipmentProduct")

    print("---")
    print(q)
    print(typeId)
    print("---")

    return selectQuery(q, (typeId,), False)

def getTypeName(idReviewable):
    q = "SELECT t.name FROM ReviewableType t, Reviewable r WHERE r.idReviewable = (?) AND t.TypeId = r.TypeId "
    return selectQuery(q, (idReviewable,), True)

def getRatings(idReviewable):
    # THINK THIS QUERY

def answer(idQuestion, idReviewable, token, chosenOption):
    idUser = getUserIdForToken(token)

    q = "SELECT * FROM Answer WHERE idQuestion = (?) AND idReviewable = (?) AND idUser = (?)"
    answerRow = selectQuery(query=q, args=(idQuestion, idReviewable, idUser,), one=True)
    if answerRow is None:
        q = "INSERT INTO Answer (idQuestion, idReviewable, idUser, chosenOption) VALUES ((?), (?), (?), (?))"
        return insertQuery(query=q, args=(idQuestion, idReviewable, idUser, chosenOption,))
    else:
        q = "UPDATE Answer SET chosenOption = (?) WHERE idQuestion = (?) AND idReviewable = (?) AND idUser = (?)"
        return updateQuery(query=q, args=(chosenOption, idQuestion, idReviewable, idUser,))


class FailedToInsertReviewableException(Exception):
    pass


class IncorrectReviewableTypeException(Exception):
    pass