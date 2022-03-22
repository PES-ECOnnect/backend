import hashlib
import uuid
from data.DBUser import *
from data.DBSession import *


def logOut(token):
    DBSession().delete(token)

def logIn(email, passwordString):
    dbu = DBUser()
    guessPassword = hashlib.sha256(passwordString.encode('UTF-8')).hexdigest()

    u = dbu.selectByEmail(email)
    if u is None:
        raise UserNotFoundException(email)

    correctPassword = u.getEncryptedPassword()
    if guessPassword != correctPassword:
        print(guessPassword, correctPassword)
        raise IncorrectUserPasswordException(email)

    # Correct email and password
    userSessionToken = str(uuid.uuid1())
    dbs = DBSession()
    dbs.insert(u.getId(), userSessionToken)

    return userSessionToken


def register(self):
    pass


# --- Exceptions

class AuthenticationException(Exception):
    def _init_(self, email):
        super().__init__(email)
        self.email = email


class IncorrectUserPasswordException(AuthenticationException):
    pass


class UserNotFoundException(AuthenticationException):
    pass


class UserAlreadyExistsException(AuthenticationException):
    pass


class FailedStartingSessionForUserException(AuthenticationException):
    pass
