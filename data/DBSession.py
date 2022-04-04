from data.DBUtils import *

def insert(userId, userSessionToken):
    q = "INSERT INTO SessionToken (token, idUser) VALUES (?, ?)"
    res = insert(query=q, args=(userSessionToken, userId))
    if res == False:
        raise FailedToOpenSessionException()

def deleteToken(token):
    dQuery = "DELETE FROM SessionToken where token = ?"
    res = delete(dQuery, (token,))
    if res == False:
        raise FailedToRemoveSessionTokenException()           

def tokenExists(token):
    sQuery = "SELECT * FROM SessionToken where token = ?"
    tokenRow = select(sQuery, (token,), True)
    return tokenRow is not None

def getUserIdForToken(token):
    sQuery = "SELECT * FROM SessionToken where token = ?"
    tokenRow = select(sQuery, (token,), True)
    return tokenRow['idUser'] if tokenRow is not None else None


# ---  Exceptions

class SessionException(Exception):
    pass


class InvalidTokenException(SessionException):
    pass


class FailedToRemoveSessionTokenException(SessionException):
    pass


class FailedToOpenSessionException(SessionException):
    pass