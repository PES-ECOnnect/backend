from app import app
import json
import hashlib

def test_homePage():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.data == b"PES Econnect Root!"

def test_isAdmin():
    response = app.test_client().get("/account/isadmin", data=dict(email="admin@econnect.com", password="admin"))
    assert response.status_code == 200

def test_isAdminNotFound():
    response = app.test_client().get("/account/isadmin", data=dict(email="admin@econnect.cat", pasword="admin"))
    assert response.data == b'{"error":"ERROR_INVALID_TOKEN"}\n'

def test_isAdminIncorrectPassword():
    response = app.test_client().get("/account/isadmin", data=dict(email="admin@econnect.com", password="hola"))
    assert response.data == b'{"error":"ERROR_INVALID_TOKEN"}\n'

def test_signUp():
    response = app.test_client().post('/account', data=dict(email="test@test.com", username="test", password="pwdtest"))
    assert response.status_code == 200


'''
# LOGIN

def test_accountLogIn():
    response = app.test_client().get("/account/login", data=dict(email="gmail", password="1234"))
    assert response.status_code == 200
    assert response.data is not null

def test_accountLogInUserNotFound():

def test_accountLogInIncorrectPassword():

def test_accountLoginFailedToOpenSession():

# SIGNUP

def test_signUp():

def test_signUpEmailExists():

def test_signUpUsernameExists():

# LOGOUT

def test_logOut():
    assert response.status_code == 200
    
def test_logOut():

def test_logOutInvalidToken():

'''

