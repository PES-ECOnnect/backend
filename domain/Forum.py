import data.DBForum as dbf


def like(token, postId, isLike, remove):
    return dbf.likePost(token, postId, isLike, remove)
