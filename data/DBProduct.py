
from data.DBUtils import *
from data.DBSession import *
from domain.Product import *

class DBProduct:

    def __init__(self):
        self._con = getCon()

    def answer(self, idQuestion, idReviewable, token, chosenOption):
        idUser = getUserIdForToken(token)

        q = "SELECT * FROM Answer WHERE idQuestion = (?) AND idReviewable = (?) AND idUser = (?)"
        answerRow = selectQuery(query=q, args=(idQuestion, idReviewable, idUser,), one=True)
        if answerRow is None:
            q = "INSERT INTO Answer (idQuestion, idReviewable, idUser, chosenOption) VALUES ((?), (?), (?), (?))"
            return insertQuery(query=q, args=(idQuestion, idReviewable, idUser, chosenOption,))
        else:
            q = "UPDATE Answer SET chosenOption = (?) WHERE idQuestion = (?) AND idReviewable = (?) AND idUser = (?)"
            return updateQuery(query=q, args=(chosenOption, idQuestion, idReviewable, idUser,))
