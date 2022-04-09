import data.DBUser as dbu

class User:

    def __init__(self, id, name, email, enPass, addr, bann, priv, acMedId, isAdmin):
        self._id = id
        self._name = name
        self._email = email
        self._enPass = enPass
        self._addr = addr
        self._bann = bann
        self._priv = priv
        self._acMedId = acMedId
        self._isAdmin = isAdmin

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getEmail(self):
        return self._email

    def getEncryptedPassword(self):
        return self._enPass

    def getAddress(self):
        return self._addr

    def isBanned(self):
        return self._bann

    def getIsPrivate(self):
        return self._priv

    def getActiveMedalId(self):
        return self._acMedId

    def isAdmin(self):
        return self._isAdmin

    def getUnlockedMedals(self):
        return dbu.getUnlockedMedals(self._id)