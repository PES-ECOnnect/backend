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


def getUserForEmail(email):
    return dbu.selectByEmail(email)


def getUserForUsername(username):
    return dbu.selectByUsername(username)


def getUserForId(id):
    u = dbu.selectById(id)
    if u is None:
        raise InvalidUserIdException()
    return u

def signUp(email, username, enPass):
    b = dbu.insert(email, username, enPass)
    if not b:
        raise FailedToInsertUserException()


# --- Exceptions

class AuthenticationException(Exception):
    def _init_(self, email):
        super().__init__(email)
        self.email = email


class InvalidUserIdException(AuthenticationException):
    pass

class IncorrectUserPasswordException(AuthenticationException):
    pass


class UserNotFoundException(AuthenticationException):
    pass


class UserAlreadyExistsException(AuthenticationException):
    pass

class FailedToInsertUserException(AuthenticationException):
    pass
