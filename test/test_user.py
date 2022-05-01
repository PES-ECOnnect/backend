from app import app

import data.DBUtils as db
import data.DBUser as dbu
import domain.User
import domain.Authenticator as auth
import hashlib

def test_initDB():
    #db.insert("INSERT INTO sessiontoken VALUES ('93003eec-b589-11ec-a4e2-00155d3ce0fc',1)")
    email = 'testuseremail@gmail.com'
    name = 'testname'
    pwd = 'testPwd'
    encPwd = hashlib.sha256(pwd.encode('UTF-8')).hexdigest()
    dbu.insert(email, name, encPwd)
    dbu.insert('testuserumail2@gmail.com', 'testname2', 'testPwd')
    user = auth.getUserForUsername('testname')
    id = user.getId()
    token = '93003eec-b589-11ec-a4e2-00155d3ce0fa'
    db.insert("INSERT INTO sessiontoken VALUES (%s, %s)", (token, id))
    db.insert("INSERT INTO unlockedmedals VALUES (%s, %s)", (id, 3))

def test_getUserInfo():
    response = app.test_client().get("/users/1")
    assert response.status_code == 200

def test_updateEmail():
    response = app.test_client().put("account/email?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newEmail=testemail@test.test")
    assert response.data == b'{"status":"success"}\n'

def test_emailExists():
    response = app.test_client().put("account/email?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newEmail=testuserumail2@gmail.com")
    assert response.data == b'{"error":"ERROR_EMAIL_EXISTS"}\n'

def test_emailInvalid():
    response = app.test_client().put("account/email?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newEmail=testuserumail2@hola@com")
    assert response.data == b'{"error":"ERROR_INVALID_EMAIL"}\n'

def test_updateUsername():
    response = app.test_client().put("account/username?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newUsername=newTestName")
    assert response.data == b'{"status":"success"}\n'

def test_usernameExists():
    response = app.test_client().put("account/username?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&newUsername=testname2")
    assert response.data == b'{"error":"ERROR_USERNAME_EXISTS"}\n'


def test_setVisibility():
    response = app.test_client().put("account/visibility?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&isPrivate=True")
    assert response.status_code == 200

def test_getPrivateUserInfo():
    token = '93003eec-b589-11ec-a4e2-00155d3ce0fa'
    user = auth.getUserForToken(token)
    id = user.getId()
    req = "users/"+str(id)
    print(req)
    response = app.test_client().get(req)
    assert response.data == b'{"error":"ERROR_PRIVATE_USER"}\n'

def test_changePassword():
    response = app.test_client().put("account/password?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&oldPassword=testPwd&newPassword=newPwd")
    assert response.status_code == 200

def test_errorUpdatePassword():
    response = app.test_client().put("account/password?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&oldPassword=testPwd&newPassword=newPwd")
    assert response.data == b'{"error":"ERROR_INCORRECT_PASSWORD"}\n'

def test_updateActiveMedal():
    response = app.test_client().put("account/medal?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&medalId=3")
    assert response.status_code == 200

def test_invalidMedal():
    response = app.test_client().put("account/medal?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&medalId=1")
    assert response.data == b'{"error":"ERROR_USER_INVALID_MEDAL"}\n'

def test_deleteAccount():
    user = auth.getUserForToken('93003eec-b589-11ec-a4e2-00155d3ce0fa')
    id = user.getId()
    response = app.test_client().delete("account?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&password=newPwd")
    assert response.status_code == 200
    query = db.select("SELECT * FROM users WHERE iduser = (%s)", (id,), True)
    assert query is None


def test_cleanDB():
    db.delete("DELETE FROM sessiontoken where token = '93003eec-b589-11ec-a4e2-00155d3ce0fa'")
    db.delete("DELETE FROM users where name in ('testname', 'testname2', 'newTestName')")

