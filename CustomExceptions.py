
class UsernameExistsException(Exception):
    def __init__(self, username, message="USERNAME_EXISTS"):
        self.message = message + "(" + username + ")"
        super().__init__(self.message)