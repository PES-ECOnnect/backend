from data.DBSession import *
from data.DBUtils import *


def insertPost(token, text, image):
    userId = getUserIdForToken(token)

    conn = getConnection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO post (idUser,temps,text,imageurl) VALUES (%s,current_timestamp,%s,%s) RETURNING idpost;",
                  (userId, text, image))
        conn.commit()

        lastInsertedPostId = c.fetchone()[0]
        return lastInsertedPostId

    except conn.IntegrityError:
        c.execute("rollback")
        raise PostAlreadyExistsException()
    except conn.Error:
        c.execute("rollback")
        raise FailedToInsertPostException()


def assignTagToPost(postId: int, tagId: int) -> None:
    q = "INSERT INTO posthashtag (idpost, idtag) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    insert(q, (postId, tagId, ))


def insertTag(tag):
    q = "INSERT INTO hashtag (tag) " \
        "VALUES (%s) " \
        "ON CONFLICT (tag) DO NOTHING"

    insert(q, (tag,))


def getTagId(tag: str) -> int:
    q = "SELECT idtag " \
        "FROM hashtag h " \
        "WHERE tag = %s"
    res = select(q, (tag,), True)
    if res is None:
        raise TagDoesntExistException()

    return res["idtag"]


# Deletes all likes and dislikes of the post with id postid
def deletelikesDislikes(postid):
    q = "DELETE FROM likes WHERE idPost = %s"
    result = delete(q, args=(postid,))
    if result == False:
        raise DeletingLikesDislikesException()
    q = "DELETE FROM dislikes WHERE idPost = %s"
    result = delete(q, args=(postid,))
    if result == False:
        raise DeletingLikesDislikesException()


# Deletes all postshashtags of the post with id postid
def deletePosthashtag(postid):
    q = "DELETE FROM posthashtag WHERE idPost = %s"
    result = delete(q, args=(postid,))
    if result == False:
        raise DeletingPostHashtagsException()


# Deletes all likes and dislikes of the post with id postid
def deletePost(postid):
    q = "DELETE FROM post WHERE idPost = %s"
    result = delete(q, args=(postid,))
    if result == False:
        raise DeletingPostException()


# Returns true if userid owns post with postid, false otherwise
def ownsPost(userid, postid):
    q = "SELECT FROM post WHERE idpost = %s AND iduser = %s"
    result = select(q, args=(postid, userid), one=True)
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


def getPostLikes(postId: int) -> int:
    q = "SELECT COUNT(*) " \
        "FROM likes l " \
        "WHERE l.idpost = %s"
    res = select(q, (postId, ), True)
    return 0 if res is None else res['count']


def getPostDislikes(postId: int) -> int:
    q = "SELECT COUNT(*) " \
        "FROM dislikes d " \
        "WHERE d.idpost = %s"
    res = select(q, (postId, ), True)
    return 0 if res is None else res['count']


def userLikesPost(userId: int, postId: int) -> int:
    q = "SELECT 1 as exists " \
        "WHERE EXISTS ( " \
        "   SELECT * " \
        "   FROM likes " \
        "   WHERE iduser = %s AND idpost = %s " \
        ")"
    res = select(q, (userId, postId, ), True)
    return False if res is None else (res['exists'] == 1)


def userDislikesPost(userId: int, postId: int) -> int:
    q = "SELECT 1 as exists " \
        "WHERE EXISTS ( " \
        "   SELECT * " \
        "   FROM dislikes " \
        "   WHERE iduser = %s AND idpost = %s " \
        ")"
    res = select(q, (userId, postId, ), True)
    return False if res is None else (res['exists'] == 1)


# Get latest N posts ordered chronologically
def getLatestNPosts(n: int) -> list:
    q = "SELECT idpost, EXTRACT(EPOCH FROM temps) as timestamp, text, imageurl, iduser as authorid, timesreported " \
        "FROM post p " \
        "ORDER BY temps DESC LIMIT %s"

    rows = select(q, (n,))
    return [] if rows is None else rows


# Get latest N posts that contain a given tag ordered chronologically
def getLatestNPostsWithTag(n: int, tag: str) -> list:
    q = "SELECT p.idpost, EXTRACT(EPOCH FROM temps) as timestamp, p.text, p.imageurl, iduser as authorid, timesreported " \
        "FROM post p " \
        "JOIN posthashtag ph on ph.idpost = p.idpost " \
        "JOIN hashtag h on h.idtag = ph.idtag " \
        "WHERE h.tag = %s " \
        "ORDER BY p.temps DESC LIMIT %s"

    rows = select(q, (tag, n,))
    return [] if rows is None else rows


def getUserPosts(userId):
    return db.select("SELECT idpost FROM post WHERE iduser = (%s)", (userId,))


def reportPost(postId):
    q = "UPDATE post SET timesreported = timesreported + 1 WHERE idpost = %s"
    return update(query=q, args=(postId,))


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


class TagDoesntExistException(Exception):
    pass