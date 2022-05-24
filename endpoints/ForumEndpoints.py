# Import Blueprint
from flask import Flask, request
from flask import Blueprint
forum_endpoint = Blueprint('forum_endpoint', __name__, template_folder='templates')

# Domain Layer
import domain.Authenticator as auth

from domain.Reviewable import *
from domain.Question import *

from domain.User import *
from domain.Question import *
from domain.Forum import *
from domain.Medal import *

# Data Layer (TODO - Remove)
import data.DBSession as dbs
import data.DBReviewable as dbp
import data.DBUser as dbu

import json
import hashlib

def anyNoneIn(l: list) -> bool:
    return any(x is None for x in l)


@forum_endpoint.route("/posts", methods=['POST'])
def NewPost():
    token = request.args.get('token')
    text = request.args.get('text')
    image = request.args.get('image')

    if anyNoneIn([token, text, image]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)

        # Extract and save the post's hashtags
        tags = obtainTags(text)
        saveTags(tags)

        # Creation of the post
        createPost(token, text, image, tags)
        idMedal = checkPostMedals(token)

        return {'status': 'success',
                'medal': idMedal}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbf.InsertionErrorException:
        return {'error': 'ERROR_INCORRECT_INSERTION'}

    except Exception:
        return {'error': 'ERROR_SOMETHING_WENT_WRONG', 'traceback': traceback.format_exc()}


@forum_endpoint.route("/posts/<id>", methods=['DELETE'])
def DeletePost(id):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        userId = user.getId()
        deletePost(userId, id)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbf.UserNotPostOwnerException:
        return {'error': 'ERROR_USER_NOT_POST_OWNER'}

    except dbf.DeletingLikesDislikesException:
        return {'error': 'ERROR_DELETING_LIKES_DISLIKES'}

    except dbf.DeletingPostHashtagsException:
        return {'error': 'ERROR_DELETING_LIKES_DISLIKES'}

    except dbf.DeletingPostException:
        return {'error': 'ERROR_DELETING_POST'}


@forum_endpoint.route("/posts/<id>/like", methods=['POST'])
def likePost(id):
    token = request.args.get('token')
    isLike = (request.args.get('isLike').lower() == "true") if request.args.get('isLike') is not None else None
    remove = (request.args.get('remove').lower() == "true") if request.args.get('remove') is not None else None

    if anyNoneIn([token, isLike, remove]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        like(token, id, isLike, remove)
        idMedal = checkLikeMedals(token)

        return {'status': 'success',
                'medal': idMedal}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@forum_endpoint.route("/posts/tags", methods=['GET'])
def getAllTags():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        return {'result': getUsedTags()}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@forum_endpoint.route("/posts", methods=['GET'])
def getPosts():
    token = request.args.get('token')
    num = request.args.get('n')

    if anyNoneIn([token, num]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        tag = request.args.get('tag') if 'tag' in request.args.keys() else None

        return {
            'result': getNPosts(token, num, tag)
        }

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@forum_endpoint.route("/revp/posts", methods=['GET'])
def getRevpPosts():
    token = request.args.get('token')
    lastDate = request.args.get('lastDate')
    tag = request.args.get('tag')
    n = request.args.get('n')

    if anyNoneIn([token, lastDate, tag, n]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)

        return {
            'result': getRevPollutionPosts(n, tag, lastDate)
        }

    except InvalidDateException:
        return {'error': 'ERROR_INVALID_DATE'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@forum_endpoint.route("/posts/<id>/report", methods=['POST'])
def reportPost(id):
    token = request.args.get('token')

    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        report(id)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
