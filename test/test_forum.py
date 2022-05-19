from app import app
import json
import re
import data.DBUtils as db


def test_forum_getRevpollutionPosts_ErrorInvalidToken():
    response = app.test_client().get("/revp/posts?token=INVALID_TOKEN&n=10&lastDate=none&tag=TestTag")
    assert response.status_code == 200
    assert response.data == b'{"error":"ERROR_INVALID_TOKEN"}\n'

def test_forum_getRevpollutionPosts_ErrorInvalidArgs():
    response = app.test_client().get("/revp/posts?token=TEST_POL&n=10&lastDate=none")
    assert response.status_code == 200
    assert response.data == b'{"error":"ERROR_INVALID_ARGUMENTS"}\n'

    response = app.test_client().get("/revp/posts?token=TEST_POL&n=10&tag=TestTag")
    assert response.status_code == 200
    assert response.data == b'{"error":"ERROR_INVALID_ARGUMENTS"}\n'

    response = app.test_client().get("/revp/posts?n=10&lastDate=none&tag=TestTag")
    assert response.status_code == 200
    assert response.data == b'{"error":"ERROR_INVALID_ARGUMENTS"}\n'

def test_forum_getRevpollutionPosts_WithoutLastDate():
    response = app.test_client().get("/revp/posts?n=10&token=TEST_POL&tag=TestTag&lastDate=none")
    assert response.status_code == 200
    d = dict(response.get_json())
    posts = d["result"]

    for post in posts:
        tags = re.findall(r"#(\w+)", post["text"])
        assert "TestTag" in tags

def test_forum_getRevpollutionPosts_WithLastDate():
    response = app.test_client().get("/revp/posts?n=10&token=TEST_POL&tag=TestTag&lastDate=1649936459.640000")
    assert response.status_code == 200
    d = dict(response.get_json())
    posts = d["result"]

    for post in posts:
        tags = re.findall(r"#(\w+)", post["text"])
        assert "TestTag" in tags
        assert float(post["timestamp"]) >= 1649936459.640000

def test_forum_getRevpollutionPosts_WithWrongLastDate():
    response = app.test_client().get("/revp/posts?n=10&token=TEST_POL&tag=TestTag&lastDate=ThisIsNotAUnixTimestamp")
    assert response.status_code == 200
    assert response.data == b'{"error":"ERROR_INVALID_DATE"}\n'


def test_initDB():
    db.insert("INSERT INTO sessiontoken VALUES ('93003eec-b589-11ec-a4e2-00155d3ce0fb',1)")


def test_forum_getAvailablePostTags():
    response = app.test_client().get("/posts/tags?token=TEST_POL")
    assert response.status_code == 200
    assert b"result" in response.data


def test_forum_getAvailablePostTags_InvalidArguments():
    response = app.test_client().get("/posts/tags")
    assert response.status_code == 200
    assert response.data == b'{"error":"ERROR_INVALID_ARGUMENTS"}\n'


def test_forum_getAvailablePostTags_InvalidToken():
    response = app.test_client().get("/posts/tags?token=")
    assert response.status_code == 200
    assert response.data == b'{"error":"ERROR_INVALID_TOKEN"}\n'


def test_forum_getPostsForTag():
    response = app.test_client().get("/posts?token=TEST_POL&tag=TEST_POL&n=10")
    assert response.status_code == 200
    d = dict(response.get_json())
    posts = d["result"]

    for post in posts:
        tags = re.findall(r"#(\w+)", post["text"])
        assert "TEST_POL" in tags


def test_doLikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=True&remove=False")
    assert response.status_code == 200
    assert b"status" in response.data


def test_removeLikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=True&remove=True")
    assert response.status_code == 200
    assert b"status" in response.data


def test_doDislikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=False&remove=False")
    assert response.status_code == 200
    assert b"status" in response.data


def test_removeDislikePost():
    response = app.test_client().post(
        "posts/1/like?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&isLike=False&remove=True")
    assert response.status_code == 200
    assert b"status" in response.data


def test_doPost():
    response = app.test_client().post("posts?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&text=testdopost&image=a")
    assert response.status_code == 200
    assert b"status" in response.data


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
