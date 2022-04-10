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
        (True if userRow['isadmin'] == 1 else False)
    )

def getUnlockedMedals(userId):
    medals = db.select("SELECT idmedal FROM unlockedmedals WHERE iduser = %s", (userId,))
    return medals

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

def insert(email, username, enPass):
    q = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    return db.insert(query=q, args=(username, email, enPass))

def delete(user):
    pass


def update(user):
    pass

# OTHER FUNCTIONS
def isEmailValid(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None

# EXCEPTIONS

class EmailExistsException(Exception):
    pass

class InvalidEmailException(Exception):
    pass