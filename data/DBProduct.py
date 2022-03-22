
from data.DBUtils import *
from domain.Product import *

class DBProduct:

    def __init__(self):
        self._con = getCon()

    def answer(self, idQuestion, idReviewable, token, chosenOption):
        tokenRow = self._con.cursor().execute("SELECT * FROM SessionToken where token = '%s'" % token).fetchone()
        idUser = tokenRow['idUser']

        cur = self._con.cursor()
        answerRow = cur.execute("SELECT * FROM Answer WHERE idQuestion = '%s' AND idReviewable = '%s' AND idUser = '%s'" % (idQuestion, idReviewable, idUser))
        if answerRow is None:
            cur.execute("INSERT INTO Answer (idQuestion, idReviewable, idUser, chosenOption) VALUES ('%s', '%s', '%s', '%s')" % (idQuestion, idReviewable, idUser, chosenOption))
        else:
            cur.execute("UPDATE Answer SET chosenOption = '%s' WHERE idQuestion = '%s' AND idReviewable = '%s' AND idUser = '%s'" % (chosenOption, idQuestion, idReviewable, idUser))
        cur.close()
        self._con.commit()
