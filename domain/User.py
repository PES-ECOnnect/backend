import data.DBUser as dbu
import domain.Reviewable as rev
import domain.Forum as forum
import domain.Authenticator as auth
import data.DBSession as dbs


class User:

    def __init__(self, id, name, email, enPass, addr, bann, priv, acMedId, isAdmin, about, pictureURL):
        self._id = id
        self._name = name
        self._email = email
        self._enPass = enPass
        self._addr = addr
        self._bann = bann
        self._priv = priv
        self._acMedId = acMedId
        self._isAdmin = isAdmin
        self._about = about
        self._pictureURL = pictureURL
        self._lat = None
        self._lon = None
        self._energyEf = None

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
        return True if self._bann.lower() == "true" else False

    def getIsPrivate(self):
        return self._priv

    def getActiveMedalId(self):
        return self._acMedId

    def isAdmin(self):
        return self._isAdmin

    def getUnlockedMedals(self):
        return dbu.getUnlockedMedals(self._id)

    def getAbout(self):
        return self._about

    def getPictureURL(self):
        return self._pictureURL

    def setEmail(self, newEmail):
        return dbu.setEmail(self._id, newEmail)

    def setUsername(self, newUsername):
        return dbu.setUsername(self._id, newUsername)

    def setHome(self, newHome):
        return dbu.setHome(self._id, newHome)

    def setAbout(self, newAbout):
        self._about = newAbout
        return dbu.setAbout(self._id, newAbout)

    def setPicture(self, newPictureURL):
        self._pictureURL = newPictureURL
        return dbu.setPicture(self._id, newPictureURL)

    def validatePassword(self, pwd):
        if pwd == self.getEncryptedPassword():
            return True
        else:
            return False

    def setPassword(self, newPwd):
        print('new password')
        print(newPwd)
        return dbu.setPassword(self._id, newPwd)

    def setVisibility(self, isPrivate):
        return dbu.setVisibility(self._id, isPrivate)

    def setActiveMedal(self, medalId):
        return dbu.setActiveMedal(self._id, medalId)

    def hasUnlockedMedal(self, medalId):
        return dbu.hasUnlockedMedal(self._id, medalId)

    def deleteUser(self):
        # delete user
        dbu.deleteUser(self._id)

    def banUser(self, id, isBanned):
        if isBanned.lower() == "true":
            dbu.banUser(id)
            dbs.deleteUserTokens(id)
        else:
            dbu.unbanUser(id)
