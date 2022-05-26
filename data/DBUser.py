import data.DBUtils as db
from domain.User import *

import re


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
        (True if userRow['isadmin'] == 1 else False),
        (str(userRow['about']) if userRow['about'] is not None else None),
        (str(userRow['pictureurl']) if userRow['pictureurl'] is not None else None),
    )


def setEmail(userId, newEmail):
    if (isEmailValid(newEmail)):
        con = db.getConnection()
        c = con.cursor()
        c.execute("begin")
        try:
            c.execute("UPDATE users SET email = %s WHERE iduser = %s", (newEmail, userId))
            c.execute('commit')
        except con.Error:
            c.execute('rollback')
            raise EmailExistsException()
    else:
        raise InvalidEmailException()


def setUsername(userId, newUsername):
    con = db.getConnection()
    c = con.cursor()
    c.execute("begin")
    try:
        c.execute("UPDATE users SET name = %s WHERE iduser = %s", (newUsername, userId))
        c.execute('commit')
    except con.Error:
        c.execute('rollback')
        raise UsernameExistsException()


def setHome(userId, newHome):
    db.update("UPDATE users SET address = %s WHERE iduser = %s", (newHome, userId))


def getHome(userId):
    return db.select("SELECT lat, lon, address FROM users WHERE iduser = %s", (userId,), one=True)


def setPassword(userId, newPwd):
    db.update("UPDATE users SET password = %s WHERE iduser = %s", (newPwd, userId))


def setAbout(userId, newAbout):
    db.update("UPDATE users SET about = %s WHERE iduser = %s", (newAbout, userId))


def setPicture(userId, newPictureURL):
    db.update("UPDATE users SET pictureurl = %s WHERE iduser = %s", (newPictureURL, userId))


def setVisibility(userId, isPrivate):
    db.update("UPDATE users SET privateprofile = %s WHERE iduser = %s", (isPrivate,userId,))


def getPostDisplayInfo(userId: int) -> dict:
    q = "SELECT * FROM users " \
        "WHERE iduser = %s " \

    res = db.select(q, (userId,), True)
    return None if res is None else dict(res)


def insert(email, username, enPass):
    if (isEmailValid(email)):
        q = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        return db.insert(query=q, args=(username, email, enPass))
    else:
        raise InvalidEmailException()


def delete(userId):
    print(userId)
    db.delete("DELETE FROM users WHERE iduser = %s", (userId,))


def update(user):
    pass


def banUser(userId):
    q = "UPDATE users SET banned = TRUE WHERE iduser = %s"
    return db.update(query=q, args=(userId,))


def unbanUser(userId):
    q = "UPDATE users SET banned = FALSE WHERE iduser = %s"
    return db.update(query=q, args=(userId,))


def deleteUser(userId):
    db.delete("DELETE FROM users WHERE iduser = %s", (userId,))

def setLocation(userId,lat,lon):
    db.update("UPDATE users SET lat= %s, lon=%s WHERE iduser = %s",(lat,lon,userId))

def setEfficiency(userId,eff):
    db.update("UPDATE users SET energyef=%s WHERE iduser = %s",(eff,userId))

# OTHER FUNCTIONS
def isEmailValid(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None


def reportUser(userId):
    q = "UPDATE users SET timesreported = timesreported + 1 WHERE iduser = %s"
    return db.update(query=q, args=(userId,))

# EXCEPTIONS

class EmailExistsException(Exception):
    pass

class InvalidEmailException(Exception):
    pass

class UsernameExistsException(Exception):
    pass

class MedalExistsException(Exception):
    pass
