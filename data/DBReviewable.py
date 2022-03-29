from data.DBSession import *

import data.DBReviewableType as dbrt


# If revType == 'Company', we assume that lat and lon are not None
# If revType != 'Company', we assume that manufacturer is not None
def insert(name, revType, imageURL, manufacturer=None, lat=None, lon=None):
    typeId = dbrt.getReviewableTypeId(revType)
    if typeId is None:
        raise IncorrectReviewableTypeException()

    con = getCon()
    c = con.cursor()
    c.execute("begin")
    try:
        print(typeId, name, imageURL)
        c.execute("INSERT INTO Reviewable (TypeId, name, imageURL) VALUES (?, ?, ?) ", (typeId, name, imageURL))
        reviewableId = c.lastrowid

        if revType == 'Company':
            c.execute("INSERT INTO InstallerCompany (ReviewableId, lat, lon) VALUES (?, ?, ?) ",
                      (reviewableId, lat, lon))
        else:
            c.execute("INSERT INTO EquipmentProduct (ReviewableId, Manufacturer) VALUES (?, ?) ",
                      (reviewableId, manufacturer))

        c.execute("commit")

    except con.IntegrityError:
        c.execute("rollback")
        raise ReviewableAlreadyExistsException()
    except con.Error:
        c.execute("rollback")
        raise FailedToInsertReviewableException()


def selectProducts():
    q = "" \
        "SELECT Manufacturer AS manufacturer, idReviewable AS id, rt.name AS type, imageURL, r.name," \
        " IFNULL(AVG(stars), 0.0) AS avgRating" \
        " FROM Reviewable r" \
        " JOIN EquipmentProduct t on t.ReviewableId = r.idReviewable" \
        " JOIN ReviewableType rt on rt.TypeId = r.TypeId" \
        " LEFT JOIN Valoration v on v.ReviewableId = r.idReviewable" \
        " GROUP BY id" \
        " ORDER BY avgRating DESC"

    return selectQuery(q, (), False)


def selectByType(revType):
    typeId = dbrt.getReviewableTypeId(revType)
    if typeId is None:
        raise IncorrectReviewableTypeException()

    if revType == "Company":

        q = "" \
            "SELECT idReviewable AS id, imageURL, r.name, IFNULL(AVG(stars), 0.0) AS avgRating, lat, lon" \
            " FROM Reviewable r" \
            " JOIN InstallerCompany t on t.ReviewableId = r.idReviewable" \
            " JOIN ReviewableType rt on rt.TypeId = r.TypeId" \
            " LEFT JOIN Valoration v on v.ReviewableId = r.idReviewable" \
            " WHERE r.TypeId = ?" \
            " GROUP BY id" \
            " ORDER BY avgRating DESC"

    else:
        q = "" \
            "SELECT Manufacturer AS manufacturer, idReviewable AS id, rt.name AS type, imageURL, r.name," \
            " IFNULL(AVG(stars), 0.0) AS avgRating" \
            " FROM Reviewable r" \
            " JOIN EquipmentProduct t on t.ReviewableId = r.idReviewable" \
            " JOIN ReviewableType rt on rt.TypeId = r.TypeId" \
            " LEFT JOIN Valoration v on v.ReviewableId = r.idReviewable" \
            " WHERE r.TypeId = ?" \
            " GROUP BY id" \
            " ORDER BY avgRating DESC"

    return selectQuery(q, (typeId,), False)


def getTypeName(idReviewable):
    q = "SELECT t.name FROM ReviewableType t, Reviewable r WHERE r.idReviewable = (?) AND t.TypeId = r.TypeId "
    return selectQuery(q, (idReviewable,), True)


# Returns an integer with the number of times the id of the Reviewable has been valorated with stars Stars.s
def getRatings(idReviewable, stars):
    q = "SELECT count() FROM Valoration WHERE ReviewableId = (?) AND Stars = (?)"
    result = selectQuery(q, (idReviewable, stars,), True)
    return result['count()']


def getLocalization(idReviewable):
    q = "SELECT lat,lon FROM InstallerCompany WHERE ReviewableId = (?)"
    result = selectQuery(q, (idReviewable,), True)
    if result is None:
        raise IdWrongTypeException()
    else:
        return result


def getManufacturer(idReviewable):
    q = "SELECT manufacturer FROM EquipmentProduct WHERE ReviewableId = (?)"
    result = selectQuery(q, (idReviewable,), True)
    if result is None:
        raise IdWrongTypeException()
    else:
        return result


def getReviewableAttributes(idReviewable):
    q = "SELECT * FROM Reviewable WHERE idReviewable = (?)"
    result = selectQuery(q, (idReviewable,), True)
    if result is None:
        raise IncorrectReviewableTypeException()
    else:
        return result


def answer(idReviewable, token, chosenOption, questionIndex):
    idUser = getUserIdForToken(token)

    q = "SELECT * FROM Reviewable WHERE idReviewable = (?)"
    TipusRow = selectQuery(query=q, args=(idReviewable,), one=True)
    idTipus = TipusRow['TypeId']

    q = "SELECT * FROM Answer WHERE idReviewable = (?) AND idUser = (?) AND idTipus = (?) AND QuestionIndex = (?)"
    answerRow = selectQuery(query=q, args=(idReviewable, idUser, idTipus, questionIndex,), one=True)
    if answerRow is None:
        q = "INSERT INTO Answer (idReviewable, idUser, ChosenOption, idTipus, QuestionIndex) VALUES ((?), (?), (?), (?), (?))"
        return insertQuery(query=q, args=(idReviewable, idUser, chosenOption, idTipus, questionIndex,))
    else:
        q = "UPDATE Answer SET ChosenOption = (?) WHERE idReviewable = (?) AND idUser = (?) AND idTipus = (?) AND QuestionIndex = (?)"
        return updateQuery(query=q, args=(chosenOption, idReviewable, idUser, idTipus, questionIndex,))


def review(idReviewable, token, review):
    idUser = getUserIdForToken(token)

    q = "SELECT * FROM Valoration WHERE UserId = (?) AND ReviewableId = (?)"
    answerRow = selectQuery(query=q, args=(idUser, idReviewable,), one=True)
    if answerRow is None:
        q = "INSERT INTO Valoration (UserId, ReviewableId, Stars) VALUES ((?), (?), (?))"
        return insertQuery(query=q, args=(idUser, idReviewable, review,))
    else:
        q = "UPDATE Valoration SET Stars = (?) WHERE UserId = (?) AND ReviewableId = (?)"
        return updateQuery(query=q, args=(review, idUser, idReviewable,))


class FailedToInsertReviewableException(Exception):
    pass


class IncorrectReviewableTypeException(Exception):
    pass


class IdWrongTypeException(Exception):
    pass


class IncorrectIdReviewableException(Exception):
    pass


class ReviewableAlreadyExistsException(Exception):
    pass
