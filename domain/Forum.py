import data.DBForum as dbf
import data.DBUtils as db
from data.DBSession import getUserIdForToken


def newPost(token, text, image):
    return dbf.newPost(token,text,image)


def deletePost(token,postid):
    userid = getUserIdForToken(token)
    # check userid owns this post
    if dbf.ownsPost(userid,postid) == False:
        raise dbf.UserNotPostOwnerException()
    else:
        # delete likes and dislikes
        dbf.deletelikesDislikes(postid)
        # delete posthashtags
        dbf.deletePosthashtag(postid)
        # delete the post
        dbf.deletePost(postid)


def like(token, postId, isLike, remove):
    userId = getUserIdForToken(token)

    if isLike and not remove:
        return dbf.likePost(userId, postId)
    elif not isLike and not remove:
        return dbf.dislikePost(userId, postId)
    elif isLike and remove:
        return dbf.removeLikePost(userId, postId)
    else:
        return dbf.removeDislikePost(userId, postId)


def getNPosts(token, number):
    #comprovar que user token no està banejat
    posts = dbf.getPosts(number)
    return {'result': posts}

