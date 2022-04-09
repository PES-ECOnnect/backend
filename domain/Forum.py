import data.DBForum as dbf
import data.DBUtils as db

def newPost(token, text, image):
    return dbf.newPost(token,text,image)
