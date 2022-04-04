import data.DBUtils as db


def insert(userId, userSessionToken):
    q = "INSERT INTO sessiontoken (token, iduser) VALUES (%s, %s)"
    print(userSessionToken, userId)
    res = db.insert(query=q, args=(userSessionToken, userId))
    print(res)
    if type(res) == bool and not res:
        raise FailedToOpenSessionException()


def deleteToken(token):
    dQuery = "DELETE FROM sessiontoken where token = %s"
    res = db.delete(dQuery, (token,))
    if type(res) == bool and not res:
        raise FailedToRemoveSessionTokenException()


def tokenExists(token):
    sQuery = "SELECT * FROM sessiontoken where token = %s"
    tokenRow = db.select(sQuery, (token,), True)
    return tokenRow is not None


def getUserIdForToken(token):
    sQuery = "SELECT * FROM sessiontoken where token = %s"
    tokenRow = db.select(sQuery, (token,), True)
    return tokenRow['iduser'] if tokenRow is not None else None


# ---  Exceptions

class SessionException(Exception):
    pass


class InvalidTokenException(SessionException):
    pass


class FailedToRemoveSessionTokenException(SessionException):
    pass


class FailedToOpenSessionException(SessionException):
    pass
