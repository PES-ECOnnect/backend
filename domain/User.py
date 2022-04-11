import data.DBUser as dbu

def newMedal(name):
    return dbu.newMedal(name)

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

    def setEmail(self, newEmail):
        return dbu.setEmail(self._id, newEmail)

    def setUsername(self, newUsername):
        return dbu.setUsername(self._id, newUsername)

    def setHome(self, newHome):
        return dbu.setHome(self._id, newHome)

    def validatePassword(self, pwd):
        if pwd == self.getEncryptedPassword():
            return True
        else:
            return False

    def setPassword(self, newPwd):
        print('new password')
        print(newPwd)
        return dbu.setPassword(self._id, newPwd)

    def setVisibility(self):
        return dbu.setVisibility(self._id, self.getIsPrivate())

    def setActiveMedal(self, medalId):
        return dbu.setActiveMedal(self._id, medalId)


