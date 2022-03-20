from data.DBUtilities import DBUtilities

class DBSessionToken:
    @staticmethod
    def insert(token,idUser):
        pass

    # First checks if token it is on our system, and deletes it from our DB
    @staticmethod
    def delete(token):
        isavailable = DBSessionToken.select(token)
        if isavailable is None:
            raise ce.InvalidTokenException(token)
        DBUtilities.query_db("DELETE FROM SessionToken where token = ?", (token,), True)
        return

    @staticmethod
    def select(token):
        return DBUtilities.query_db("SELECT * FROM SessionToken where token = ?", [token], True)