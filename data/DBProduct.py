
from data.DBUtils import *
from domain.Product import *

class DBProduct:

    def __init__(self):
        self._con = getCon()

    def answer(self, idQuestion, idReviewable, token, ChosenOption):
        tokenRow = self._con.cursor().execute("SELECT * FROM SessionToken where token = '%s'" % token).fetchone()
        if tokenRow is None:
            return None
        idUser = tokenRow['idUser']

        cur = self._con.cursor()
        cur.execute("INSERT INTO Answer (idQuestion, idReviewable, idUser, chosenOption) VALUES ('%s', '%s', '%s', '%s')" % (idQuestion, idReviewable, idUser, ChosenOption))
        cur.close()
        self._con.commit()