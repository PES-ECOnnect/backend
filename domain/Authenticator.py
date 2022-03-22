import hashlib
import uuid
import data.DBUser as dbu
import data.DBSession as dbs


def logOut(token):
    dbs.deleteToken(token)

def logIn(email, passwordString):
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
    dbs.insert(u.getId(), userSessionToken)

    return userSessionToken

def checkValidToken(token):
    if not dbs.tokenExists(token):
        raise dbs.InvalidTokenException()

def getUserForToken(token):
    userId = dbs.getUserIdForToken(token)
    return dbu.selectById(userId)

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

