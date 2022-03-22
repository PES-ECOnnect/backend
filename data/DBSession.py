from data.DBUtils import *


class DBSession:

    def insert(self, userId, userSessionToken):
        q = "INSERT INTO SessionToken (token, idUser) VALUES (?, ?)"
        res = insertQuery(query=q, args=(userSessionToken, userId))
        if res == False:
            raise FailedToOpenSession()

    def delete(self, token):
        sQuery = "SELECT * FROM SessionToken where token = ?"
        tokenRow = selectQuery(sQuery, (token, ), True)
        if tokenRow is None:
            raise InvalidTokenException()

        dQuery = "DELETE FROM SessionToken where token = ?"
        res = deleteQuery(dQuery, (token, ))
        if res == False:
            raise FailedToRemoveSessionTokenException()

        print("----------", res)


class InvalidTokenException(Exception):
    pass


class FailedToRemoveSessionTokenException(Exception):
    pass

class FailedToOpenSession(Exception):
    pass