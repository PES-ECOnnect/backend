from data.DBUtils import getCon


class DBSession:

    def __init__(self):
        self._con = getCon()

    def insert(self, userId, userSessionToken):
        cur = self._con.cursor()
        cur.execute("INSERT INTO SessionToken (token, idUser) VALUES ('%s', '%s')" % (userSessionToken, userId))
        cur.close()
        self._con.commit()
