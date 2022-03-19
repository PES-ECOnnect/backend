
class UsernameExistsException(Exception):
    def __init__(self, username, message="USERNAME_EXISTS"):
        if username:
        	self.message = "Username " + username + " already exists."
        else:
        	self.message = message
        super().__init__(self.message)


class IncorrectUserPasswordException(Exception):
    def __init__(self, username, message="Incorrect password."):
        if username:
        	self.message = "Incorrect password for username " + username
        else:
        	self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, username, message="USER_NOT_FOUND"):
        if username:
        	self.message = "No User found for username: " + username
        else:
        	self.message = message
        super().__init__(self.message)

class InvalidTokenException(Exception):
    def __init__(self, token, message = "Invalid Token."):
        if token:
            self.message = "Token " + token + " is not registered on the system."
        else:
            self.message = message
        super().__init__(self.message)