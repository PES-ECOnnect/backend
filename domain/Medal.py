import data.DBMedal as dbm
import domain.Authenticator as auth
from enum import Enum

class Medal(Enum):
    EficienciaA = 1
    EficienciaB = 2
    EficienciaC = 3
    EficienciaD = 4
    EficienciaE = 5
    EficienciaF = 6
    EficienciaG = 7
    EmpresaOr = 8
    EmpresaPlata = 9
    EmpresaBronze = 10
    ProducteOr = 11
    ProductePlata = 12
    ProducteBronze = 13
    ForumOr = 14
    ForumPlata = 15
    ForumBronze = 16
    LikeOr = 17
    LikePlata = 18
    LikeBronze = 19
    PreguntaOr = 20
    PreguntaPlata = 21
    PreguntaBronze = 22

def setActiveMedal(idUser, idMedal):
    return dbm.setActiveMedal(idUser, idMedal)

def hasUnlockedMedal(idUser, idMedal):
    return dbm.hasUnlockedMedal(idUser, idMedal)

def getUnlockedMedals(idUser):
    return dbm.getUnlockedMedals(idUser)

def unlockMedal(idUser, medalla):
    idMedal = medalla.value
    result = dbm.unlockMedal(idUser, idMedal)
    if result:
        return idMedal
    return None

def checkQuestionMedals(token):
    user = auth.getUserForToken(token)
    idUser = user.getId()
    num = dbm.getNumAnsweredQuestions(idUser)
    if num == 1:
        return unlockMedal(idUser, Medal.PreguntaBronze)
    elif num == 15:
        return unlockMedal(idUser, Medal.PreguntaPlata)
    elif num == 50:
        return unlockMedal(idUser, Medal.PreguntaOr)
    return None

def checkCompanyMedals(token):
    user = auth.getUserForToken(token)
    idUser = user.getId()
    num = dbm.getNumReviewedCompanies(idUser)
    if num == 1:
        return unlockMedal(idUser, Medal.EmpresaBronze)
    elif num == 10:
        return unlockMedal(idUser, Medal.EmpresaPlata)
    elif num == 20:
        return unlockMedal(idUser, Medal.EmpresaOr)
    return None

def checkProductMedals(token):
    user = auth.getUserForToken(token)
    idUser = user.getId()
    num = dbm.getNumReviewedProducts(idUser)
    if num == 1:
        return unlockMedal(idUser, Medal.ProducteBronze)
    elif num == 10:
        return unlockMedal(idUser, Medal.ProductePlata)
    elif num == 20:
        return unlockMedal(idUser, Medal.ProducteOr)
    return None

def checkPostMedals(token):
    user = auth.getUserForToken(token)
    idUser = user.getId()
    num = dbm.getNumPosts(idUser)
    if num == 1:
        return unlockMedal(idUser, Medal.ForumBronze)
    elif num == 10:
        return unlockMedal(idUser, Medal.ForumPlata)
    elif num == 25:
        return unlockMedal(idUser, Medal.ForumOr)
    return None

def checkLikeMedals(token):
    user = auth.getUserForToken(token)
    idUser = user.getId()
    num = dbm.getNumLikes(idUser)
    if num == 1:
        return unlockMedal(idUser, Medal.LikeBronze)
    elif num == 20:
        return unlockMedal(idUser, Medal.LikePlata)
    elif num == 100:
        return unlockMedal(idUser, Medal.LikeOr)
    return None

def checkEfficiencyMedals(token):
    user = auth.getUserForToken(token)
    idUser = user.getId()
    dbm.deleteEfficiencyMedal(idUser)
    efficiency = dbm.getEnergyEficiency(idUser)
    if efficiency == 'A':
        return unlockMedal(idUser, Medal.EficienciaA)
    elif efficiency == 'B':
        return unlockMedal(idUser, Medal.EficienciaB)
    elif efficiency == 'C':
        return unlockMedal(idUser, Medal.EficienciaC)
    elif efficiency == 'D':
        return unlockMedal(idUser, Medal.EficienciaD)
    elif efficiency == 'E':
        return unlockMedal(idUser, Medal.EficienciaE)
    elif efficiency == 'F':
        return unlockMedal(idUser, Medal.EficienciaF)
    elif efficiency == 'G':
        return unlockMedal(idUser, Medal.EficienciaG)
    return None
