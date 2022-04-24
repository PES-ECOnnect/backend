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

        c.execute("INSERT INTO reviewable (typeid, name, imageurl) VALUES (%s, %s, %s) RETURNING idreviewable;",
                  (typeId, name, imageURL))
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
        "SELECT t.manufacturer AS manufacturer, r.idreviewable AS id, rt.name AS type, r.imageurl, r.name," \
        " COALESCE(AVG(stars), 0.0) AS avgRating" \
        " FROM reviewable r" \
        " JOIN equipmentproduct t on t.idreviewable = r.idreviewable" \
        " JOIN reviewabletype rt on rt.typeid = r.typeid" \
        " LEFT JOIN valoration v on v.idreviewable = r.idreviewable" \
        " GROUP BY id, t.manufacturer, rt.name, r.imageurl, r.name" \
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
    result = db.select(q, (idReviewable,), True)
    return result['name']


# Returns an integer with the number of times the id of the Reviewable has been valorated with stars Stars.s
def getRatings(idReviewable, stars):
    q = "SELECT count(*) FROM valoration WHERE idreviewable = %s AND stars = %s"
    result = db.select(q, (idReviewable, stars,), True)
    return result['count']


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


def answer(idReviewable, token, chosenOption, questionid):
    idUser = getUserIdForToken(token)

    q = "SELECT * FROM reviewable WHERE idreviewable = %s"
    TipusRow = db.select(query=q, args=(idReviewable,), one=True)
    idTipus = TipusRow['typeid']

    q = "SELECT * FROM answer WHERE idreviewable = %s AND iduser = %s AND questionid = %s"
    answerRow = db.select(query=q, args=(idReviewable, idUser, questionid,), one=True)
    if answerRow is None:
        q = "INSERT INTO answer (idreviewable, iduser, chosenoption, questionid) VALUES (%s, %s, %s, " \
            "%s) "
        return db.insert(query=q, args=(idReviewable, idUser, chosenOption, questionid,))
    else:
        q = "UPDATE answer SET chosenoption = %s WHERE idreviewable = %s AND iduser = %s AND " \
            "questionid = %s "
        return db.update(query=q, args=(chosenOption, idReviewable, idUser, questionid,))


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


def deleteUserAnswers(userId):
    db.delete("DELETE FROM answer WHERE iduser = %s", (userId,))

def deleteUserReviews(userId):
    db.delete("DELETE FROM valoration WHERE iduser = %s", (userId,))

def deleteReviewable(idreviewable):
    db.delete("DELETE FROM reviewable WHERE idreviewable = %s",(idreviewable,))

def getUserRate(revId, userId):
    rate = db.select("SELECT stars FROM valoration WHERE iduser = %s AND idreviewable = %s", (userId, revId))
    if rate:
        aux = rate[0]
        stars = aux['stars']
        return stars
    else:
        return None

def updateCompany(name, image, lat, lon, id):
    res = db.update("UPDATE reviewable SET name=%s, imageurl=%s WHERE idreviewable=%s", (name, image, id))
    if type(res) == bool and not res:
        raise FailedToUpdateReviewableException()
    res = db.update("UPDATE installercompany SET lat=%s, lon=%s WHERE idreviewable = %s", (lat, lon, id))
    if type(res) == bool and not res:
        raise FailedToUpdateCompanyException()

def updateProduct(name, type, image, manufacturer, id):
    res = db.update("UPDATE reviewable SET name=%s, typeid=%s, imageurl=%s WHERE idreviewable = %s", (name, type, image, id))
    print(res)
    if not res:
        raise FailedToUpdateReviewableException()
    db.update("UPDATE equipmentproduct SET  manufacturer=%s WHERE idreviewable=%s", (manufacturer, id))


# EXCEPTIONS

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

class FailedToUpdateCompanyException(Exception):
    pass

class FailedToUpdateReviewableException(Exception):
    pass

class FailedToUpdateProductException(Exception):
    pass