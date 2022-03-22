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
        raise FailedToInsertProductException()


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


class FailedToInsertProductException(Exception):
    pass


class IncorrectReviewableTypeException(Exception):
    pass
