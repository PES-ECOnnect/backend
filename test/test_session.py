from app import app
import json

import data.DBUtils as db

def test_initDB():
    db.insert("INSERT INTO sessiontoken VALUES ('93003eec-b589-11ec-a4e2-00155d3ce0fb',1)")

def test_homePage():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.data == b"PES Econnect Root!"

def test_isAdmin():
    response = app.test_client().get("/account/isadmin?token=93003eec-b589-11ec-a4e2-00155d3ce0fb")
    assert response.status_code == 200
    assert response.data == b'{"result":"true"}\n'

def test_isAdminNotFound():
    response = app.test_client().get("/account/isadmin?email=admin@email.com&password=adminn&token=xdddd")
    assert response.data == b'{"error":"ERROR_INVALID_TOKEN"}\n'

def test_signUp():
    # crea un usuario con los siguientes datos:
    # username: signUpTest, password: signUpPwd, email: sign@up.test
    response = app.test_client().post("/account?username=signUpTest&password=signUpPwd&email=sign@up.test")
    status = response.json['status']
    assert response.status_code == 200
    assert status == 'success'

def test_signUpEmailExists():
    response = app.test_client().post("/account?username=signUpTest&password=signUpPwd&email=sign@up.test")
    assert response.data == b'{"error":"ERROR_USER_EMAIL_EXISTS"}\n'

def test_signUpUsernameExists():
    response = app.test_client().post("/account?username=signUpTest&password=signUpPwd&email=sign@up.test2")
    assert response.data == b'{"error":"ERROR_USER_USERNAME_EXISTS"}\n'

def test_accountLogIn():
    response = app.test_client().get("/account/login?email=sign@up.test&password=signUpPwd")
    token = response.data
    assert response.status_code == 200
    assert token != None

def test_accountLogInUserNotFound():
    response = app.test_client().get("/account/login?email=newSign@up.test&password=signUpPwd")
    assert response.data == b'{"error": "ERROR_USER_NOT_FOUND"}'

def test_accountLogInIncorrectPassword():
    response = app.test_client().get("/account/login?email=sign@up.test&password=signUpPwdWrong")
    assert response.data == b'{"error": "ERROR_USER_INCORRECT_PASSWORD"}'

def test_cleanDB():
    # clean database
    db.delete("DELETE FROM users where email in ('sign@up.test')")
    db.delete("DELETE FROM sessiontoken where token = '93003eec-b589-11ec-a4e2-00155d3ce0fb'")



