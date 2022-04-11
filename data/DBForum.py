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


def likePost(userId, postId):
    q = 'SELECT FROM likes WHERE idpost = %s AND iduser = %s'
    result = select(q, args=(postId, userId), one=True)
    if result is not None:
        raise LikeExistsException()

    q = 'SELECT FROM dislikes WHERE idpost = %s AND iduser = %s'
    result = select(q, args=(postId, userId), one=True)
    if result is not None:
        q = 'DELETE FROM dislikes WHERE idpost = %s AND iduser = %s'
        result = delete(q, args=(postId, userId))
        if not result:
            raise RemoveDislikePostException()

    q = 'INSERT INTO likes (idpost, iduser) VALUES (%s, %s)'
    result = insert(q, args=(postId, userId))
    if not result:
        raise LikePostException()


def dislikePost(userId, postId):
    q = 'SELECT FROM dislikes WHERE idpost = %s AND iduser = %s'
    result = select(q, args=(postId, userId), one=True)
    if result is not None:
        raise DislikeExistsException()

    q = 'SELECT FROM likes WHERE idpost = %s AND iduser = %s'
    result = select(q, args=(postId, userId), one=True)
    if result is not None:
        q = 'DELETE FROM likes WHERE idpost = %s AND iduser = %s'
        result = delete(q, args=(postId, userId))
        if not result:
            raise RemoveLikePostException()

    q = 'INSERT INTO dislikes (idpost, iduser) VALUES (%s, %s)'
    result = insert(q, args=(postId, userId))
    if not result:
        raise DislikePostException()


def removeLikePost(userId, postId):
    q = 'SELECT FROM likes WHERE idpost = %s AND iduser = %s'
    result = select(q, args=(postId, userId), one=True)
    if result is None:
        raise LikeDoesntExistException()

    q = 'DELETE FROM likes WHERE idpost = %s AND iduser = %s'
    result = delete(q, args=(postId, userId))
    if not result:
        raise RemoveLikePostException()


def removeDislikePost(userId, postId):
    q = 'SELECT FROM dislikes WHERE idpost = %s AND iduser = %s'
    result = select(q, args=(postId, userId), one=True)
    if result is None:
        raise DislikeDoesntExistException()

    q = 'DELETE FROM dislikes WHERE idpost = %s AND iduser = %s'
    result = delete(q, args=(postId, userId))
    if not result:
        raise RemoveDislikePostException()



def getUsedTags() -> list:
    q = "SELECT DISTINCT tag " \
        "FROM hashtag h " \
        "JOIN posthashtag ph ON h.idtag = ph.idtag"

    rows = select(q)
    return [] if rows is None else list(row['tag'] for row in rows)


def tagUsages(tag: str) -> int:
    q = "SELECT COUNT(*) " \
        "FROM posthashtag ph " \
        "JOIN hashtag h on h.idtag = ph.idtag " \
        "WHERE h.tag = %s"

    res = select(q, (tag,), True)
    return None if res is None else res['count']

  
def getPosts(userId, n):
    q = 'SELECT p.idpost AS postId, u.name AS username, p.iduser AS userId, u.idactivemedal AS medal, ' \
        'p.text AS text, p.imageurl AS imageUrl,' \
        '(SELECT COUNT(*) FROM likes l WHERE l.idpost = p.idpost) AS likes, ' \
        '(SELECT COUNT(*) FROM dislikes l WHERE l.idpost = p.idpost) AS dislikes, ' \
        'TRUNC(EXTRACT(EPOCH FROM temps)) as timestamp, ' \
        '((SELECT COUNT(*) FROM likes l WHERE l.iduser = %s AND l.idpost = p.idpost)*2 + ' \
        '(SELECT COUNT(*) FROM dislikes d WHERE d.iduser = %s AND d.idpost = p.idpost)) AS userOption ' \
        'FROM post p, users u ' \
        'WHERE p.iduser = u.iduser ' \
        'ORDER BY temps DESC LIMIT %s'
    result = select(q, (userId, userId, n,), False)
    if result is None:
        raise NoPostsException()
    return result


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

class LikePostException(Exception):
    pass

class DislikePostException(Exception):
    pass

class RemoveLikePostException(Exception):
    pass

class RemoveDislikePostException(Exception):
    pass

class LikeExistsException(Exception):
    pass

class DislikeExistsException(Exception):
    pass

class LikeDoesntExistException(Exception):
    pass

class DislikeDoesntExistException(Exception):
    pass

class NoPostsException(Exception):
    pass