from app import app

import data.DBUtils as db
import data.DBUser as dbu
import domain.User
import domain.Authenticator as auth

def test_initDB():
    #db.insert("INSERT INTO sessiontoken VALUES ('93003eec-b589-11ec-a4e2-00155d3ce0fc',1)")
    dbu.insert('testuseremail@gmail.com', 'testname', 'testPwd')
    dbu.insert('testuserumail2@gmail.com', 'testname2', 'testPwd')
    user = auth.getUserForUsername('testname')
    id = user.getId()
    token = '93003eec-b589-11ec-a4e2-00155d3ce0fa'
    db.insert("INSERT INTO sessiontoken VALUES (%s, %s)", (token, id))

def test_getUserInfo():
    response = app.test_client().get("/users/1")
    assert response.status_code == 200

def test_getPrivateUserInfo():
    response = app.test_client().get("/users/1")
    assert response.data == b'{"error":"ERROR_PRIVATE_USER"}\n'

def test_updateEmail():
    response = app.test_client().put("account/email?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newEmail=testemail@test.test")
    assert response.data == b'{"status":"success"}\n'

def test_emailExists():
    response = app.test_client().put("account/email?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newEmail=testuserumail2@gmail.com")
    assert response.data == b'{"error":"ERROR_EMAIL_EXISTS"}\n'

def test_emailInvalid():
    response = app.test_client().put("account/email?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newEmail=testuserumail2@hola@com")
    assert response.data == b'{"error":"ERROR_INVALID_EMAIL"}\n'

def test_cleanDB():
    db.delete("DELETE FROM sessiontoken where token = '93003eec-b589-11ec-a4e2-00155d3ce0fa'")
    db.delete("DELETE FROM users where name in ('testname', 'testname2')")

