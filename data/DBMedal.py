import data.DBUtils as db

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
