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

def test_doPost():
    response = app.test_client().post("posts?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&text=testdopost&image=a")
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'


def test_getNLastPosts():
    resp = app.test_client().get("posts?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&n=1")
    assert resp.status_code == 200
    correct = ({
            "authorbanned": False,
            "dislikes": 0,
            "imageurl": "a",
            "likes": 0,
            "ownpost": True,
            "text": "testdopost",
            "userid": 1,
            "useroption": 0
    })
    response = json.loads(resp.get_data(as_text=True))
    response = response["result"]

    print(response)
    assert (
        response[0]["authorbanned"] == correct["authorbanned"] and
        response[0]["dislikes"] == correct["dislikes"] and
        response[0]["imageurl"] == correct["imageurl"] and
        response[0]["likes"] == correct["likes"] and
        response[0]["ownpost"] == correct["ownpost"] and
        response[0]["text"] == correct["text"] and
        response[0]["userid"] == correct["userid"] and
        response[0]["useroption"] == correct["useroption"]
    )

def test_cleanDB():
    db.delete("DELETE FROM post where iduser = '1' and text = 'testdopost'")
    db.delete("DELETE FROM sessiontoken where token = '93003eec-b589-11ec-a4e2-00155d3ce0fb'")
