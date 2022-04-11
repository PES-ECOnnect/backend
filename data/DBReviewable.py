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
        c.execute("INSERT INTO reviewable (typeid, name, imageurl) VALUES (%s, %s, %s) RETURNING idreviewable;",
                  (typeId, name, imageURL))
        reviewableId = c.fetchone()[0]


        if revType == 'Company':
            c.execute("INSERT INTO InstallerCompany (ReviewableId, lat, lon) VALUES (?, ?, ?) ",
                      (reviewableId, lat, lon))
        else:
            c.execute("INSERT INTO equipmentproduct (idreviewable, manufacturer) VALUES (%s, %s) ",
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
        "SELECT t.manufacturer AS manufacturer, r.idreviewable AS id, rt.name AS type, r.imageurl, r.name," \
        " COALESCE(AVG(stars), 0.0) AS avgRating" \
        " FROM reviewable r" \
        " JOIN equipmentproduct t on t.idreviewable = r.idreviewable" \
        " JOIN reviewabletype rt on rt.typeid = r.typeid" \
        " LEFT JOIN valoration v on v.idreviewable = r.idreviewable" \
        " GROUP BY id, t.manufacturer, rt.name, r.imageurl, r.name" \
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
    return db.select(q, (idReviewable,), True)


# Returns an integer with the number of times the id of the Reviewable has been valorated with stars Stars.s
def getRatings(idReviewable, stars):
    q = "SELECT count() FROM valoration WHERE idreviewable = %s AND stars = %s"
    result = db.select(q, (idReviewable, stars,), True)
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
        q = "INSERT INTO answer (idreviewable, iduser, chosenoption, typeid, questionindex) VALUES (%s, %s, %s, %s, " \
            "%s) "
        return db.insert(query=q, args=(idReviewable, idUser, chosenOption, idTipus, questionIndex,))
    else:
        q = "UPDATE answer SET chosenoption = %s WHERE idreviewable = %s AND iduser = %s AND typeid = %s AND " \
            "questionindex = %s "
        return db.update(query=q, args=(chosenOption, idReviewable, idUser, idTipus, questionIndex,))


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
