import data.DBForum as dbf
import data.DBUtils as db
import data.DBUser as dbu
import re
from data.DBSession import getUserIdForToken
import datetime

def obtainTags(text: str) -> list:
    return re.findall(r"#(\w+)", text)


def saveTags(tags: list) -> None:
    for tag in tags:
        dbf.insertTag(tag)

    return tags

def createPost(token, text, image, tags):
    postId = dbf.insertPost(token, text, image)

    for tag in tags:
        tagId = dbf.getTagId(tag)
        dbf.assignTagToPost(postId, tagId)

    return postId


def deletePost(userid, postid):
    #userid = dbu.getUserIdForToken(token)

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

def deleteUserPosts(userId):
    posts = dbf.getUserPosts(userId)
    if posts:
        for pid in posts:
            idpost = str(pid['idpost'])
            deletePost(userId, idpost)
            print(pid['idpost'])


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
    result = []
    for tag in tags:
        result.append({
            'tag' : tag,
            'count' : dbf.tagUsages(tag)
        })

    return sorted(result, key=lambda d: -d['count'])


def getNPosts(token, number, tag):
    currentUserId = getUserIdForToken(token)

    if tag is None:
        posts = dbf.getLatestNPosts(number)
    else:
        posts = dbf.getLatestNPostsWithTag(number, tag)

    result = []
    for postInfo in posts:
        postId = postInfo["idpost"]
        authorId = postInfo["authorid"]

        likes = dbf.getPostLikes(postId)
        dislikes = dbf.getPostDislikes(postId)
        authorInfo = dbu.getPostDisplayInfo(authorId)

        if dbf.userLikesPost(currentUserId, postId):
            userOption = 2
        elif dbf.userDislikesPost(currentUserId, postId):
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
            "userid": authorInfo["iduser"],
            "username": authorInfo["name"],
            "useroption": userOption,
            "medal": authorInfo["idactivemedal"],
            "ownpost": authorId == currentUserId
        })

    return result

