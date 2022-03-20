
from data.DBUtils import *
from domain.User import *

class DBUser:

    def __init__(self):
        self._con = getCon()

    def insert(self, user):
        pass

    def delete(self, user):
        pass

    def update(self, user):
        pass

    def selectByEmail(self, email):
        cur = self._con.cursor()
        cur.execute("SELECT * FROM User WHERE email = '%s'" % email)
        userRow = cur.fetchone()
        cur.close()

        if userRow is None:
            return None

        return User(
            userRow['idUser'],
            userRow['name'],
            userRow['email'],
            userRow['password'],
            userRow['address'],
            userRow['banned'],
            userRow['privateProfile'],
            userRow['idActiveMedal'],
        )
