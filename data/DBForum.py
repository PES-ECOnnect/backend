from data.DBSession import *
import data.DBUtils as db


def likePost(token, idPost, isLike, remove):
    idUser = getUserIdForToken(token)
    if isLike is True and remove is False:
        # comprovar si hi ha dislike i esborrar
        q = 'INSERT INTO likes (idpost, iduser) VALUES (%s, %s)'
        return db.insert(query=q, args=(idPost, idUser,))
    elif isLike is False and remove is False:
        # comprovar si hi ha like i esborrar
        q = 'INSERT INTO dislikes (idpost, iduser) VALUES (%s, %s)'
        return db.insert(query=q, args=(idPost, idUser,))
    elif isLike is True and remove is True:
        # comprovar que hi ha like
        q = 'DELETE FROM likes WHERE idpost = %s AND iduser = %s'
        return db.delete(query=q, args=(idPost, idUser,))
    else:
        # comprovar que hi ha dislike
        q = 'DELETE FROM dislikes WHERE idpost = %s AND iduser = %s'
        return db.delete(query=q, args=(idPost, idUser,))

    return 0