from DBHandler import DBHandler
from CustomExceptions import UsernameExistsException


class User:

	# Construct new instance
	def __init__(self, username, utok):
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

		# May raise UsernameExistsException 
		dbh = DBHandler()
		res = dbh.insertUser(username, h)
		print("User with username " + username + " created successfully.")

		


