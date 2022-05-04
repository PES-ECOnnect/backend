from app import app
import json

import data.DBUtils as db

def test_initDB():
    db.insert("INSERT INTO sessiontoken VALUES ('93003eec-b589-11ec-a4e2-00155d3ce0fb',1)")
'''
def test_getUsedTags():
    #response = app.test_client().get("/")
    #assert response.status_code == 200
    #assert response.data == b"PES Econnect Root!"

def test_cleanDB():
    # clean database
    # db.delete("DELETE FROM users where email in ('sign@up.test')")

'''
def test_doLikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=True&remove=False")
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'


def test_removeLikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=True&remove=True")
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'


def test_doDislikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=False&remove=False")
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'


def test_removeDislikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=False&remove=True")
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'

def test_cleanDB():
    db.delete("DELETE FROM sessiontoken where token = '93003eec-b589-11ec-a4e2-00155d3ce0fb'")
