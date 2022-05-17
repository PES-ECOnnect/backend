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
