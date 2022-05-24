import data.DBUser as dbu
import domain.Reviewable as rev
import domain.Forum as forum
import domain.Authenticator as auth
import data.DBSession as dbs
from enum import Enum


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

    def deleteUser(self):
        # delete user
        dbu.deleteUser(self._id)

    def banUser(self, id, isBanned):
        if isBanned.lower() == "true":
            dbu.banUser(id)
            dbs.deleteUserTokens(id)
        else:
            dbu.unbanUser(id)
    
    def setLocation(self,lat,lon):
        return dbu.setLocation(self._id,lat,lon)
    
    def setEfficiency(self,eff):
        return dbu.setEfficiency(self._id,eff)

##################################### END OF CLASS USER #####################################
 
def gethouseEfficiency(house):
    # Calculates the efficiency of a house (medium letter)
    # qualificaci_emissions calefaccio
    # qualificaci_emissions_1 refrigeracio
    # qualificaci_emissions_2 enllumenament
    # qualificaci_de_consum_d energia primaria no renovable
    # qualificacio_d_emissions emissions CO2
    emisco2 = house.get("qualificacio_d_emissions")
    consener = house.get("qualificaci_de_consum_d")
    calefaccio = house.get("qualificaci_emissions")
    refrigeracio = house.get("qualificaci_emissions_1")
    enllumenament = house.get("qualificaci_emissions_2")

    qualificacions = {emisco2,consener,calefaccio,refrigeracio,enllumenament}
    suma = 0
    nombre = 0
    for quali in qualificacions:
        if quali:
            num = getNumQualificacio(quali, 1)
            if num == "Invalid Qualification":
                print("Invalid Qualification")
                return -1
            suma += num
            nombre += 1
    if nombre > 0:
        return getNumQualificacio(int(round(suma/nombre,0)), 0) 
    else:
        return -1
    
def getNumQualificacio(quali, option):
    switcher = {
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4,
        'E': 5,
        'F': 6,
        'G': 7
    }
    
    if option: return switcher.get(quali,"Invalid Qualification")
    else:
        switcher_2 = {y:x for x, y in switcher.items()} 
        return switcher_2.get(quali,"Error!")

def getHomeLocation(userId):
    return dbu.getHome(userId)


def report(id):
    return dbu.reportUser(id)
