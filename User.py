from DBHandler import DBHandler
import CustomExceptions as ce
import uuid

class User:

	# Construct new instance
	def __init__(self, username):
		self.username = username
		self.utok = utok


	# Defines Hash method for user passwords
	@staticmethod
	def passwordHash(self, passwordString):
		return passwordString


	# Register new user into database
	@staticmethod
	def register(username, passwordString):
		# TODO: h = passwordHash(passwordString)
		h = passwordString

		dbh = DBHandler()
		res = dbh.insertUser(username, h)
		print("User with username " + username + " created successfully.")


	# Log into account
	@staticmethod
	def login(username, passwordString) -> str:
		# TODO: requestHash = passwordHash(passwordString)
		requestHash = passwordString

		dbh = DBHandler()
		correctHash = dbh.selectUserPassword(username)
		
		if requestHash != correctHash:
			raise ce.IncorrectUserPasswordException(username)

		userSessionToken = uuid.uuid1()
		dbh.setSessionToken(username, userSessionToken)

		return userSessionToken

	# Check if username correponds to an admin user
	@staticmethod
	def isAdmin(username):
		# May raise UsernameExistsException 
		dbh = DBHandler()
		return dbh.selectUserIsAdmin(username)
		

