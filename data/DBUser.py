from data.DBUtils import *
from domain.User import *


def selectByEmail(email):
    q = "SELECT * FROM User WHERE email = (?)"
    userRow = selectQuery(query=q, args=(email,), one=True)

    if userRow is None:
        return None

    return userFromRow(userRow)


def selectById(userId):
    q = "SELECT * FROM User WHERE idUser = (?)"
    userRow = selectQuery(query=q, args=(userId,), one=True)

    if userRow is None:
        return None

    return userFromRow(userRow)


def selectByUsername(username):
    q = "SELECT * FROM User WHERE name = (?)"
    userRow = selectQuery(query=q, args=(username,), one=True)

    if userRow is None:
        return None

    return userFromRow(userRow)


def userFromRow(userRow) -> User:
    return User(
        int(userRow['idUser']),
        str(userRow['name']),
        str(userRow['email']),
        str(userRow['password']),
        str(userRow['address']),
        str(userRow['banned']),
        bool(userRow['privateProfile']),
        (int(userRow['idActiveMedal']) if userRow['idActiveMedal'] is not None else None),
        (True if userRow['isAdmin'] == 'true' else False)
    )


def insert(email, username, enPass):
    q = "INSERT INTO user (name, email, password) VALUES (?, ?, ?)"
    return insertQuery(query=q, args=(username, email, enPass))


def delete(user):
    pass


def update(user):
    pass
