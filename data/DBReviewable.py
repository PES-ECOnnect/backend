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


def answer(idReviewable, token, chosenOption, idTipus, questionIndex):
    idUser = getUserIdForToken(token)

    q = "SELECT * FROM Answer WHERE idReviewable = (?) AND idUser = (?) AND idTipus = (?) AND QuestionIndex = (?)"
    answerRow = selectQuery(query=q, args=(idReviewable, idUser, idTipus, questionIndex,), one=True)
    if answerRow is None:
        q = "INSERT INTO Answer (idReviewable, idUser, ChosenOption, idTipus, QuestionIndex) VALUES ((?), (?), (?), (?), (?))"
        return insertQuery(query=q, args=(idReviewable, idUser, chosenOption, idTipus, questionIndex,))
    else:
        q = "UPDATE Answer SET ChosenOption = (?) WHERE idReviewable = (?) AND idUser = (?) AND idTipus = (?) AND QuestionIndex = (?)"
        return updateQuery(query=q, args=(chosenOption, idReviewable, idUser, idTipus, questionIndex,))


class FailedToInsertReviewableException(Exception):
    pass


class IncorrectReviewableTypeException(Exception):
    pass
