from data.DBSession import *
import data.DBReviewableType as dbrt
import data.DBUtils as db


# If revType == 'Company', we assume that lat and lon are not None
# If revType != 'Company', we assume that manufacturer is not None
def insert(name, revType, imageURL, manufacturer=None, lat=None, lon=None):
    typeId = dbrt.getReviewableTypeId(revType)
    if typeId is None:
        raise IncorrectReviewableTypeException()

    conn = db.getConnection()
    c = conn.cursor()
    c.execute("begin")
    try:
        c.execute("INSERT INTO reviewable (typeid, name, imageurl) VALUES (%s, %s, %s) RETURNING idreviewable;", (typeId, name, imageURL))
        reviewableId = c.fetchone()[0]

        if revType == 'Company':
            c.execute("INSERT INTO installercompany (idreviewable, lat, lon) VALUES (%s, %s, %s) ",
                      (reviewableId, lat, lon))
        else:

            c.execute("INSERT INTO equipmentproduct (idreviewable, manufacturer) VALUES (%s, %s) ",
                      (reviewableId, manufacturer))

        c.execute("commit")

    except conn.IntegrityError:
        c.execute("rollback")
        raise ReviewableAlreadyExistsException()
    except conn.Error:
        c.execute("rollback")
        raise FailedToInsertReviewableException()


def selectProducts():
    q = "" \
        "SELECT Manufacturer AS manufacturer, idReviewable AS id, rt.name AS type, imageURL, r.name," \
        " IFNULL(AVG(stars), 0.0) AS avgRating" \
        " FROM reviewable r" \
        " JOIN EquipmentProduct t on t.ReviewableId = r.idReviewable" \
        " JOIN reviewabletype rt on rt.TypeId = r.TypeId" \
        " LEFT JOIN valoration v on v.ReviewableId = r.idReviewable" \
        " GROUP BY id" \
        " ORDER BY avgRating DESC"

    return db.select(q, (), False)


def selectByType(revType):
    typeId = dbrt.getReviewableTypeId(revType)
    if typeId is None:
        raise IncorrectReviewableTypeException()

    if revType == "Company":

        q = "" \
            "SELECT r.idreviewable AS id, imageurl, r.name, COALESCE(AVG(stars), 0.0) AS avgRating, lat, lon" \
            " FROM reviewable r" \
            " JOIN installercompany t on t.idreviewable = r.idreviewable" \
            " JOIN reviewabletype rt on rt.typeid = r.typeid" \
            " LEFT JOIN valoration v on v.idreviewable = r.idreviewable" \
            " WHERE r.typeid = %s" \
            " GROUP BY id, r.idreviewable, lat, lon" \
            " ORDER BY avgRating DESC"

    else:
        q = "" \
            "SELECT t.manufacturer AS manufacturer, r.idreviewable AS id, rt.name AS type, imageurl, r.name," \
            " COALESCE(AVG(stars), 0.0) AS avgRating" \
            " FROM reviewable r" \
            " JOIN equipmentproduct t on t.idreviewable = r.idreviewable" \
            " JOIN reviewabletype rt on rt.typeid = r.typeid" \
            " LEFT JOIN valoration v on v.idreviewable = r.idreviewable" \
            " WHERE r.typeid = %s" \
            " GROUP BY id, t.manufacturer, rt.name" \
            " ORDER BY avgRating DESC"

    return db.select(q, (typeId,), False)


def getTypeName(idReviewable):
    q = "SELECT t.name FROM reviewabletype t, reviewable r WHERE r.idreviewable = %s AND t.typeid = r.typeid "
    return db.select(q, (idReviewable,), True)


# Returns an integer with the number of times the id of the Reviewable has been valorated with stars Stars.s
def getRatings(idReviewable, stars):
    q = "SELECT count() FROM valoration WHERE idreviewable = %s AND stars = %s"
    result = db.select(q, (idReviewable, stars,), True)
    return result['count()']


def getLocalization(idReviewable):
    q = "SELECT lat, lon FROM installercompany WHERE idreviewable = %s"
    result = db.select(q, (idReviewable,), True)
    if result is None:
        raise IdWrongTypeException()
    else:
        return result


def getManufacturer(idReviewable):
    q = "SELECT manufacturer FROM equipmentproduct WHERE idreviewable = %s"
    result = db.select(q, (idReviewable,), True)
    if result is None:
        raise IdWrongTypeException()
    else:
        return result


def getReviewableAttributes(idReviewable):
    q = "SELECT * FROM reviewable WHERE idreviewable = %s"
    result = db.select(q, (idReviewable,), True)
    if result is None:
        raise IncorrectReviewableTypeException()
    else:
        return result


def answer(idReviewable, token, chosenOption, questionIndex):
    idUser = getUserIdForToken(token)

    q = "SELECT * FROM reviewable WHERE idreviewable = %s"
    TipusRow = db.select(query=q, args=(idReviewable,), one=True)
    idTipus = TipusRow['typeid']

    q = "SELECT * FROM answer WHERE idreviewable = %s AND iduser = %s AND typeid = %s AND questionindex = %s"
    answerRow = db.select(query=q, args=(idReviewable, idUser, idTipus, questionIndex,), one=True)
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

    q = "SELECT * FROM valoration WHERE iduser = %s AND idreviewable = %s"
    answerRow = db.select(query=q, args=(idUser, idReviewable,), one=True)
    if answerRow is None:
        q = "INSERT INTO valoration (iduser, idreviewable, stars) VALUES (%s, %s, %s)"
        return db.insert(query=q, args=(idUser, idReviewable, review,))
    else:
        q = "UPDATE valoration SET stars = %s WHERE iduser = %s AND idreviewable = %s"
        return db.update(query=q, args=(review, idUser, idReviewable,))


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
