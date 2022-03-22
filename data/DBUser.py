
from data.DBUtils import *
from domain.User import *

def selectByEmail(email):
    q = "SELECT * FROM User WHERE email = (?)"
    userRow = selectQuery(query=q, args=(email,), one=True)

    if userRow is None:
        return None

    return User(
        int(userRow['idUser']),
        str(userRow['name']),
        str(userRow['email']),
        str(userRow['password']),
        str(userRow['address']),
        str(userRow['banned']),
        bool(userRow['privateProfile']),
        (int(userRow['idActiveMedal']) if userRow['idActiveMedal'].isdigit() else None),
        (True if userRow['isAdmin'] == 'true' else False)
    )

def selectById(id):
    q = "SELECT * FROM User WHERE idUser = (?)"
    userRow = selectQuery(query=q, args=(id,), one=True)

    if userRow is None:
        return None

    return User(
        int(userRow['idUser']),
        str(userRow['name']),
        str(userRow['email']),
        str(userRow['password']),
        str(userRow['address']),
        str(userRow['banned']),
        bool(userRow['privateProfile']),
        (int(userRow['idActiveMedal']) if userRow['idActiveMedal'].isdigit() else None),
        (True if userRow['isAdmin'] == 'true' else False)
    )

def insert(user):
        pass

def delete(user):
    pass

def update(user):
    pass

    
    
