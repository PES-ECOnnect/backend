import data.DBUser as dbu
import domain.Reviewable as rev
import domain.Forum as forum
import domain.Authenticator as auth



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
        return True if self._bann.lower() == "true" else False

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

    def setVisibility(self, isPrivate):
        return dbu.setVisibility(self._id, isPrivate)

    def setActiveMedal(self, medalId):
        return dbu.setActiveMedal(self._id, medalId)

    def hasUnlockedMedal(self, medalId):
        return dbu.hasUnlockedMedal(self._id, medalId)

    def deleteUser(self, token):
        # delete ratings
        rev.deleteUserReviews(self._id)
        # delete answers
        rev.deleteUserAnswers(self._id)
        # delete posts
        forum.deleteUserPosts(self._id)
        # logout
        auth.logOut(token)
        # delete user
        dbu.delete(self._id)
