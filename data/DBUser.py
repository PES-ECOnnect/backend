import data.DBUtils as db
from domain.User import *


def selectByEmail(email):
    q = "SELECT * FROM users WHERE email = %s"

    userRow = db.select(query=q, args=(email,), one=True)

    if userRow is None:
        return None

    return userFromRow(userRow)


def selectById(userId):
    q = "SELECT * FROM users WHERE iduser = %s"

    userRow = db.select(query=q, args=(userId,), one=True)

    if userRow is None:
        return None

    return userFromRow(userRow)


def selectByUsername(username):
    q = "SELECT * FROM users WHERE name = %s"

    userRow = db.select(query=q, args=(username,), one=True)

    if userRow is None:
        return None

    return userFromRow(userRow)


def userFromRow(userRow) -> User:
    return User(
        int(userRow['iduser']),
        str(userRow['name']),
        str(userRow['email']),
        str(userRow['password']),
        (str(userRow['address']) if userRow['address'] is not None else None),
        (str(userRow['banned']) if userRow['banned'] is not None else None),
        (bool(userRow['privateprofile']) if userRow['privateprofile'] is not None else None),
        (int(userRow['idactivemedal']) if userRow['idactivemedal'] is not None else None),
        (True if userRow['isadmin'] == 1 else False)
    )


def getPostDisplayInfo(userId: int) -> dict:
    q = "SELECT * FROM users " \
        "WHERE iduser = %s " \

    res = db.select(q, (userId,), True)
    return None if res is None else dict(res)


def insert(email, username, enPass):
    q = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    return db.insert(query=q, args=(username, email, enPass))


def delete(user):
    pass


def update(user):
    pass
