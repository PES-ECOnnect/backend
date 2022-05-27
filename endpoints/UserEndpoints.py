# Import Blueprint
from flask import Flask, request
from flask import Blueprint
user_endpoint = Blueprint('user_endpoint', __name__, template_folder='templates')

# LIBRARIES AND FILES
# Domain Layer
import domain.Authenticator as auth

from domain.Reviewable import *
from domain.Question import *

from domain.User import *
from domain.Question import *
from domain.Medal import *

# Data Layer (TODO - Remove)
import data.DBSession as dbs
import data.DBReviewable as dbp
import data.DBUser as dbu

import json
import hashlib

import os

# Generalitat Dataset
from sodapy import Socrata

client_gene = Socrata("analisi.transparenciacatalunya.cat", os.environ.get('ECONNECT_GENE_TOKEN'))

def anyNoneIn(l: list) -> bool:
    return any(x is None for x in l)

@user_endpoint.route("/userprova")
def helloWorldprova():
    return "OK"

@user_endpoint.route("/account", methods=['POST'])
def signUp():
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    if anyNoneIn([email, username, password]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    enPass = hashlib.sha256(password.encode('UTF-8')).hexdigest()

    if auth.getUserForEmail(email) is not None:
        return {'error': 'ERROR_USER_EMAIL_EXISTS'}

    if auth.getUserForUsername(username) is not None:
        return {'error': 'ERROR_USER_USERNAME_EXISTS'}

    try:
        auth.signUp(email, username, enPass)
        token = auth.logIn(email, password)
        return {'status': 'success',
                'token': str(token)}

    except auth.FailedToInsertUserException:
        return {'error': 'ERROR_FAILED_SIGN_UP'}

    except dbs.FailedToOpenSessionException:
        return json.dumps({'error': 'ERROR_STARTING_USER_SESSION'})

    except dbu.InvalidEmailException:
        return {'error': 'ERROR_INVALID_EMAIL'}

    except Exception:
        return json.dumps({'error': 'ERROR_SOMETHING_WENT_WRONG'})


@user_endpoint.route("/account", methods=['GET'])
def getCurrentUserInfo():
    token = request.args.get("token")
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        u = auth.getUserForToken(token)
        return {
            "result": {
                "username": u.getName(),
                "email": u.getEmail(),
                "activeMedal": u.getActiveMedalId(),
                "medals": getUnlockedMedals(u.getId()),
                "isPrivate": u.getIsPrivate(),
                "home": u.getAddress(),
                "about": u.getAbout(),
                "pictureURL": u.getPictureURL()
            }
        }

    except dbs.InvalidTokenException:
        return {"error": "ERROR_INVALID_TOKEN"}


@user_endpoint.route("/account/login", methods=['GET'])
def accountLogin():
    email = request.args.get('email')
    passwordString = request.args.get('password')
    if anyNoneIn([email, passwordString]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        u = auth.getUserForEmail(email)
        if u is None:
            return json.dumps({'error': 'ERROR_USER_NOT_FOUND'})

        if u.isBanned():
            return {'error': 'ERROR_BANNED'}

        token = auth.logIn(email, passwordString)
        return json.dumps({
            'token': str(token)
        })

    except auth.IncorrectUserPasswordException:
        return json.dumps({'error': 'ERROR_USER_INCORRECT_PASSWORD'})

    except dbs.FailedToOpenSessionException:
        return json.dumps({'error': 'ERROR_STARTING_USER_SESSION'})


@user_endpoint.route("/account/isadmin", methods=['GET'])
def isAdmin():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        u = auth.getUserForToken(token)
        return {'result': 'true'} if u.isAdmin() else {'result': 'false'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/account/logout", methods=['GET'])
def logout():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        auth.logOut(token)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/users/<id>", methods=['GET'])
def getUserInfo(id):
    try:
        user = auth.getUserForId(id)
        if user.getIsPrivate():
            return {'error': 'ERROR_PRIVATE_USER'}

        return {
            'username': user.getName(),
            'medals': getUnlockedMedals(id),
            'activeMedal': user.getActiveMedalId(),
            'about': user.getAbout(),
            'pictureURL': user.getPictureURL()
        }

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/users/<uid>/ban", methods=['GET'])
def userIsBanned(uid):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        u = auth.getUserForId(uid)
        return {'result': u.isBanned()}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except auth.InvalidUserIdException:
        return {'error': 'ERROR_USER_NOT_EXISTS'}

    except Exception:
        return {'error': 'ERROR_SOMETHING_WENT_WRONG'}


@user_endpoint.route("/account/email", methods=['PUT'])
def updateEmail():
    token = request.args.get('token')
    newEmail = request.args.get('newEmail')

    if anyNoneIn([token, newEmail]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setEmail(newEmail)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbu.EmailExistsException:
        return {'error': 'ERROR_EMAIL_EXISTS'}

    except dbu.InvalidEmailException:
        return {'error': 'ERROR_INVALID_EMAIL'}


@user_endpoint.route("/account/username", methods=['PUT'])
def updateUsername():
    token = request.args.get('token')
    newUsername = request.args.get('newUsername')

    if anyNoneIn([token, newUsername]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setUsername(newUsername)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

    except dbu.UsernameExistsException:
        return {'error': 'ERROR_USERNAME_EXISTS'}


@user_endpoint.route("/account/password", methods=['PUT'])
def updatePassword():
    token = request.args.get('token')
    oldPassword = request.args.get('oldPassword')
    newPassword = request.args.get('newPassword')

    if anyNoneIn([token, oldPassword, newPassword]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        oldEncryptedPwd = hashlib.sha256(oldPassword.encode('UTF-8')).hexdigest()
        user = auth.getUserForToken(token)

        if user.validatePassword(oldEncryptedPwd):
            enNewPass = hashlib.sha256(newPassword.encode('UTF-8')).hexdigest()
            user.setPassword(enNewPass)
            return {'status': 'success'}

        else:
            return {'error': 'ERROR_INCORRECT_PASSWORD'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/account/visibility", methods=['PUT'])
def updateVisibility():
    token = request.args.get('token')
    isPrivate = request.args.get('isPrivate')

    if anyNoneIn([token, isPrivate]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setVisibility(isPrivate)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/account/medal", methods=['PUT'])
def updateActiveMedal():
    token = request.args.get('token')
    medalId = request.args.get('medalId')
    if anyNoneIn([token, medalId]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        
        if int(medalId) == 0:
            dbm.removeActiveMedal(user.getId())
            return {'status': 'success'}
        if dbm.hasUnlockedMedal(user.getId(), medalId):
            dbm.setActiveMedal(user.getId(), medalId)
            return {'status': 'success'}

        return {'error': 'ERROR_USER_INVALID_MEDAL'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@user_endpoint.route("/account/about", methods=['PUT'])
def updateAbout():
    token = request.args.get('token')
    newAbout = request.args.get('newAbout')

    if anyNoneIn([token, newAbout]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setAbout(newAbout)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/account/picture", methods=['PUT'])
def updatePicture():
    token = request.args.get('token')
    newPictureURL = request.args.get('newPictureURL')

    if anyNoneIn([token, newPictureURL]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.setPicture(newPictureURL)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/account", methods=['DELETE'])
def deleteAccount():
    token = request.args.get('token')
    if anyNoneIn([token, ]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        user = auth.getUserForToken(token)
        user.deleteUser()
        return {'status': 'success'}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}


@user_endpoint.route("/users/<id>/ban", methods=['POST'])
def banAccount(id):
    token = request.args.get('token')
    isBanned = request.args.get('isBanned')
    if anyNoneIn([token, isBanned]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)

        user = auth.getUserForToken(token)

        if not user.isAdmin():
            return {'error': 'ERROR_USER_NOT_ADMIN'}
        if user.getId() == int(id):
            return {'error': 'ERROR_CANNOT_BAN_YOURSELF'}

        user.banUser(id, isBanned)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@user_endpoint.route("/homes/cities/<zipcode>")
def getStreetNames(zipcode):
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}
    try:
        auth.checkValidToken(token)
        # Get json cities with zipcode
        results = client_gene.get("j6ii-t3w2",codi_postal=str(zipcode))
        if results == []:
            return {'error': 'CITY_NOT_EXISTS'}
        # Recorrem tots els objectes del json

        # serà alias : streets

        streets_total = []
        for house in results:
            street = house["adre_a"]
            nomCorrecte = street.upper()
            traduccions = {"AVENIDA": "AVINGUDA",
                           "CALLE": "CARRER",
                           " DE ": " ",
                           "C.": "CARRER",
                           "C/": "CARRER",
                           "AV.": "AVINGUDA",
                           "AV/": "AVINGUDA",
                           "AVDA": "AVINGUDA",
                           "PASEO": "PASSEIG",
                           " D'": "",
                           "ST.": "SANT",
                           "' ": "'",
                           "À": "A",
                           "Á": "A",
                           "È": "E",
                           "É": "E",
                           "Í": "I",
                           "Ò": "O",
                           "Ó": "O",
                           "Ú": "U"
            }
            for orig in traduccions:
                nomCorrecte = nomCorrecte.replace(orig,traduccions[orig])

            trobat = False
            for elem in streets_total:
                if elem['name'] == nomCorrecte: trobat = True
            if not trobat:
                streets_total.append({
                    'name': nomCorrecte,
                    'aliases': [street,]
                })
            else:
                for elem in streets_total:
                    if elem['name'] == nomCorrecte:
                        # Check bad name not already in array
                        found = False
                        for badst in elem['aliases']:
                            #print(badst + ' ' + street)
                            if badst == street:
                                found = True
                        if not found:
                            elem['aliases'].append(street)
        return {'result': streets_total}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@user_endpoint.route("/homes/building")
def getDomiciles():
    token = request.args.get('token')
    street = request.args.get('street').split("#") # SPLIT PER #
    number = request.args.get('number')
    zipcode = request.args.get('zipcode')
    if anyNoneIn([token,street]): # The number may be null?
        return {'error': 'ERROR_INVALID_ARGUMENTS'}
    try:
        houses = []
        auth.checkValidToken(token)
        for st in street:
            if number is None:
                results = client_gene.get("j6ii-t3w2",codi_postal=zipcode,adre_a=st)
            else:
                results = client_gene.get("j6ii-t3w2",codi_postal=zipcode,adre_a=st,numero=number)
            for house in results:
                #print(house)
                casa = {"numero":house["numero"]}
                if "pis" in house:
                    casa["pis"] = house["pis"]
                if "porta" in house:
                    casa["porta"] = house["porta"]
                if "escala" in house:
                    casa["escala"] = house["escala"]
                if "num_cas" in house:
                    casa["num_cas"] = house["num_cas"]
                if "adre_a" in house:
                    casa["carrer"] = house["adre_a"]
                houses.append(casa)
        if len(houses)== 0:
            return {'error': 'ERROR_BUILDING_NOT_EXISTS'}
        return {'result': houses}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@user_endpoint.route("/account/home", methods=['PUT'])
def setHome():
    token = request.args.get('token')
    street = request.args.get('street')
    number = request.args.get('number')
    zipcode = request.args.get('zipcode')
    escala = request.args.get('escala')
    pis = request.args.get('pis')
    porta = request.args.get('porta')
    if anyNoneIn([token,street,number,zipcode]): # The number may be null?
        return {'error': 'ERROR_INVALID_ARGUMENTS'}
    try:
        auth.checkValidToken(token)
        
        # Get house
        escalanull = (escala is None)
        pisnull = (pis is None)
        portanull = (porta is None)
        if not escalanull and not pisnull and not portanull:
            house = client_gene.get("j6ii-t3w2",codi_postal=zipcode,adre_a=street,numero=number,porta=porta,escala=escala,pis=pis)
        else:
            if escalanull and not pisnull and not portanull:
                house = client_gene.get("j6ii-t3w2",codi_postal=zipcode,adre_a=street,numero=number,porta=porta,pis=pis)
            else:
                if not escalanull and pisnull and portanull:
                    house = client_gene.get("j6ii-t3w2",codi_postal=zipcode,adre_a=street,numero=number,escala=escala)
                else:
                    if escalanull and pisnull and not portanull:
                        house = client_gene.get("j6ii-t3w2",codi_postal=zipcode,adre_a=street,numero=number,porta=porta)
                    else: 
                        house = client_gene.get("j6ii-t3w2",codi_postal=zipcode,adre_a=street,numero=number)
        #print(house[0]["comarca"])
        # Get House Efficiency Letter:
        if house is None or len(house) == 0:
            return {'error': 'ERROR_BUILDING_NOT EXISTS'}
        qualif = gethouseEfficiency(house[0])
        # Set house (address, lat, lon, efficiency)?
        print(house[0])
        
        user = auth.getUserForToken(token)
        address = house[0]["adre_a"]+' '+house[0]["numero"]+', '+house[0]["poblacio"]
        user.setHome(address)
        if ("latitud" in house[0] and "longitud" in house[0]):
            user.setLocation(house[0]["latitud"],house[0]["longitud"])
        user.setEfficiency(qualif)
        # Call function to set medal
        idmedal = checkEfficiencyMedals(token)
        return {'status': 'success',
                'medal': idmedal}
    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@user_endpoint.route("/account/home", methods=['GET'])
def getUserHome():
    token = request.args.get('token')
    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}
    try:
        id = auth.getUserForToken(token).getId()
        home = getHomeLocation(id)
        return {
            'lat': home['lat'],
            'lon': home['lon'],
            'address': home['address']
        }

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}

@user_endpoint.route("/users/<id>/report", methods=['POST'])
def reportUser(id):
    token = request.args.get('token')

    if anyNoneIn([token]):
        return {'error': 'ERROR_INVALID_ARGUMENTS'}

    try:
        auth.checkValidToken(token)
        report(id)
        return {'status': 'success'}

    except dbs.InvalidTokenException:
        return {'error': 'ERROR_INVALID_TOKEN'}
