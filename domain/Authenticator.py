import hashlib
import uuid
from data.DBUser import *
from data.DBSession import *


class Authenticator:
    def __init__(self):
        self._dbUser = DBUser()

    def logIn(self, email, passwordString):
        guessPassword = hashlib.sha256(passwordString.encode('UTF-8')).hexdigest()

        u = self._dbUser.selectByEmail(email)

        if u is None:
            raise UserNotFoundException(email)

        correctPassword = u.getEncryptedPassword()
        if guessPassword != correctPassword:
            print(guessPassword, correctPassword)
            raise IncorrectUserPasswordException(email)

        # Correct email and password
        userSessionToken = uuid.uuid1()
        try:
            dbs = DBSession()
            dbs.insert(u.getId(), userSessionToken)
        except Exception:
            raise FailedStartingSessionForUserException(email)

        return userSessionToken

    @staticmethod
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
