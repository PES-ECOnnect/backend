
from data.DBUtils import *
from data.DBSession import *
from domain.Product import *

class DBProduct:

    def __init__(self):
        self._con = getCon()

    def answer(self,idType, QuestionIndex, idReviewable, token, chosenOption):
        idUser = getUserIdForToken(token)

        q = "SELECT * FROM Answer WHERE idTipus = (?) AND QuestionIndex = (?) AND idReviewable = (?) AND idUser = (?)"
        answerRow = selectQuery(query=q, args=(idType, QuestionIndex, idReviewable, idUser,), one=True)
        print(answerRow)
        if answerRow is None:
            print ("hola")
            q = "INSERT INTO Answer (idTipus, QuestionIndex, idReviewable, idUser, chosenOption) VALUES ((?), (?), (?), (?), (?))"
            return insertQuery(query=q, args=(idType, QuestionIndex, idReviewable, idUser, chosenOption,))
        else:
            print("adios")
            q = "UPDATE Answer SET chosenOption = (?) WHERE idTipus = (?) AND QuestionIndex = (?) AND idReviewable = (?) AND idUser = (?)"
            return updateQuery(query=q, args=(chosenOption, idType, QuestionIndex, idReviewable, idUser,))

    def deleteQuestion(self,QuestIndex,idtipus):
        # First we delete all Answers of this question
        q = "DELETE FROM Answer WHERE idTipus = (?) AND QuestionIndex = (?)"
        if deleteQuery(query=q,args=(idtipus, QuestIndex,)) is False:
            return False
        # then we delete answer
        q = "DELETE FROM Question WHERE idTipus = (?) AND QuestIndex = (?)"
        return deleteQuery(query=q, args=(idtipus, QuestIndex,))