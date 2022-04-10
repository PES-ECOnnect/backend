from data.DBSession import *
from data.DBUtils import *


def newPost(token,text,image):
    idUser = getUserIdForToken(token)
    q = "INSERT INTO post (idUser,temps,text,imageurl) values (%s,current_timestamp,%s,%s)"
    result = insert(q,args=(idUser,text,image))
    if result == False:
        raise InsertionErrorException()

# Deletes all likes and dislikes of the post with id postid
def deletelikesDislikes(postid):
    q = "DELETE FROM likes WHERE idPost = %s"
    result = delete(q,args=(postid))
    if result == False:
        raise DeletingLikesDislikesException()
    q = "DELETE FROM dislikes WHERE idPost = %s"
    result = delete(q, args=(postid))
    if result == False:
        raise DeletingLikesDislikesException()

# Deletes all postshashtags of the post with id postid
def deletePosthashtag(postid):
    q = "DELETE FROM posthashtag WHERE idPost = %s"
    result = delete(q,args=(postid))
    if result == False:
        raise DeletingPostHashtagsException()

# Deletes all likes and dislikes of the post with id postid
def deletePost(postid):
    q = "DELETE FROM post WHERE idPost = %s"
    result = delete(q, args=(postid))
    if result == False:
        raise DeletingPostException()

# Returns true if userid owns post with postid, false otherwise
def ownsPost(userid,postid):
    q = "SELECT FROM post WHERE idpost = %s AND iduser = %s"
    result = select(q,args=(postid,userid),one=True)
    if result is None:
        return False
    else:
        return True


def likePost(token, idPost, isLike, remove):
    idUser = getUserIdForToken(token)
    if isLike is True and remove is False:
        # comprovar si hi ha dislike i esborrar
        q = 'INSERT INTO likes (idpost, iduser) VALUES (%s, %s)'
        return insert(query=q, args=(idPost, idUser,))
    elif isLike is False and remove is False:
        # comprovar si hi ha like i esborrar
        q = 'INSERT INTO dislikes (idpost, iduser) VALUES (%s, %s)'
        return insert(query=q, args=(idPost, idUser,))
    elif isLike is True and remove is True:
        # comprovar que hi ha like
        q = 'DELETE FROM likes WHERE idpost = %s AND iduser = %s'
        return delete(query=q, args=(idPost, idUser,))
    else:
        # comprovar que hi ha dislike
        q = 'DELETE FROM dislikes WHERE idpost = %s AND iduser = %s'
        return delete(query=q, args=(idPost, idUser,))

    return 0

# Exceptions
class InsertionErrorException(Exception):
    pass

class DeletingLikesDislikesException(Exception):
    pass

class UserNotPostOwnerException(Exception):
    pass

class DeletingPostHashtagsException(Exception):
    pass

class DeletingPostException(Exception):
    pass
