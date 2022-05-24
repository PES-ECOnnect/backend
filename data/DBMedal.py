import data.DBUtils as db

def setActiveMedal(userId, medalId):
    db.update("UPDATE users SET idactivemedal = %s WHERE iduser = %s", (medalId, userId))
    
def removeActiveMedal(userId):
    db.update("UPDATE users SET idactivemedal = NULL WHERE iduser = %s", (userId,))


def hasUnlockedMedal(userId, medalId):
    result = db.select("SELECT * FROM unlockedmedals WHERE iduser=(%s) AND idmedal=(%s)", (userId, medalId))
    if result:
        return True
    else:
        return False

def getUnlockedMedals(userId):
    medals = db.select("SELECT m.idmedal FROM unlockedmedals u, medal m WHERE iduser = %s AND u.idmedal = m.idmedal "
                       "ORDER BY m.idmedal ASC", (userId,))
    return medals

def unlockMedal(idUser, idMedal):
    q = "INSERT INTO unlockedmedals (iduser, idmedal) VALUES (%s, %s)"
    return db.insert(query=q, args=(idUser, idMedal))

def getNumAnsweredQuestions(idUser):
    q = "SELECT COUNT(*) FROM answer WHERE iduser = %s"
    num = db.select(query=q, args=(idUser,), one=True)
    return num["count"]

def getNumReviewedCompanies(idUser):
    q = "SELECT COUNT(v.iduser) FROM valoration v, reviewable r, reviewabletype t WHERE v.iduser = %s AND " \
        "v.idreviewable = r.idreviewable AND r.typeid = t.typeid AND t.name = 'Company'"
    num = db.select(query=q, args=(idUser,), one=True)
    return num["count"]

def getNumReviewedProducts(idUser):
    q = "SELECT COUNT(v.iduser) FROM valoration v, reviewable r, reviewabletype t WHERE v.iduser = %s AND " \
        "v.idreviewable = r.idreviewable AND r.typeid = t.typeid AND t.name <> 'Company'"
    num = db.select(query=q, args=(idUser,), one=True)
    return num["count"]

def getNumPosts(idUser):
    q = "SELECT COUNT(*) FROM post WHERE iduser = %s"
    num = db.select(query=q, args=(idUser,), one=True)
    return num["count"]

def getNumLikes(idUser):
    q = "SELECT COUNT(*) FROM likes WHERE iduser = %s"
    numLikes = db.select(query=q, args=(idUser,), one=True)
    q = "SELECT COUNT(*) FROM dislikes WHERE iduser = %s"
    numDislikes = db.select(query=q, args=(idUser,), one=True)
    return numLikes["count"] + numDislikes["count"]

def getEnergyEficiency(idUser):
    q = "SELECT energyef FROM users WHERE iduser = %s"
    num = db.select(query=q, args=(idUser,), one=True)
    return num["energyef"]

def deleteEfficiencyMedal(idUser):
    q = "DELETE FROM unlockedmedals WHERE iduser = %s AND idmedal IN (1, 2, 3, 4, 5, 6, 7)"
    db.delete(query=q, args=(idUser,))
    q = "SELECT * FROM users WHERE iduser = %s AND idactivemedal IN (1, 2, 3, 4, 5, 6, 7)"
    result = db.select(query=q, args=(idUser,))
    if result:
        setActiveMedal(idUser, None)
    return
