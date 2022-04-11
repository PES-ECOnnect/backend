import data.DBForum as dbf
import data.DBUtils as db
import data.DBUser as dbu

from data.DBSession import getUserIdForToken


def newPost(token, text, image, tags):
    postId = dbf.newPost(token, text, image)

    for tag in tags:
        tagId = dbf.getTagId(tag)






def deletePost(token, postid):
    userid = getUserIdForToken(token)
    # check userid owns this post
    if dbf.ownsPost(userid, postid) == False:
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


# Obtains all tags that have been used at least once
def getUsedTags():
    tags = dbf.getUsedTags()
    result = {}
    for tag in tags:
        result[tag] = dbf.tagUsages(tag)

    return result


def getNPosts(token, number, tag):
    userId = getUserIdForToken(token)
    userInfo = dbu.getPostDisplayInfo(userId)

    if tag is None:
        posts = dbf.getLatestNPosts(number)
    else:
        posts = dbf.getLatestNPostsWithTag(number, tag)

    result = []
    for postInfo in posts:
        postId = postInfo["idpost"]
        likes = dbf.getPostLikes(postId)
        dislikes = dbf.getPostDislikes(postId)

        if dbf.userLikesPost(userId, postId):
            userOption = 2
        elif dbf.userDislikesPost(userId, postId):
            userOption = 1
        else:
            userOption = 0

        result.append({
            "postid": postInfo["idpost"],
            "text": postInfo["text"],
            "likes": likes,
            "dislikes": dislikes,
            "imageurl": postInfo["imageurl"],
            "timestamp": postInfo["timestamp"],
            "userid": userInfo["iduser"],
            "username": userInfo["name"],
            "useroption": userOption,
            "medal": userInfo["idactivemedal"],
        })

    return result