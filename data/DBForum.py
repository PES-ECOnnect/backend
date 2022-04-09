from data.DBUtils import *
from data.DBSession import getUserIdForToken

def newPost(token,text,image):
    idUser = getUserIdForToken(token)
    q = "INSERT INTO post (idUser,temps,text,imageurl) values (%s,current_timestamp,%s,%s)"
    result = insert(q,args=(idUser,text,image))
    if result == False:
        raise InsertionError()


# Exceptions
class InsertionError(Exception):
    pass