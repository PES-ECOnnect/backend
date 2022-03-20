from data.DBUtils import getCon


class DBSession:

    def __init__(self):
        self._con = getCon()

    def insert(self, userId, userSessionToken):
        cur = self._con.cursor()
        cur.execute("INSERT INTO SessionToken (token, idUser) VALUES ('%s', '%s')" % (userSessionToken, userId))
        cur.close()
        self._con.commit()

    def delete(self, token):
        tokenRow = self._con.cursor().execute("SELECT * FROM SessionToken where token = '%s'" % token).fetchone()
        if tokenRow is None:
            raise InvalidTokenException()

        self._con.cursor().execute("DELETE FROM SessionToken where token = '%s'" % token)
        self._con.commit()


class InvalidTokenException(Exception):
    pass
