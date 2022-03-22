
from data.DBUtils import *
from domain.User import *

class DBUser:

    def insert(self, user):
        pass

    def delete(self, user):
        pass

    def update(self, user):
        pass

    def selectByEmail(self, email):
        q = "SELECT * FROM User WHERE email = ?"
        userRow = query_db(query=q, args=(email), one=True)

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
