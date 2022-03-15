import sqlite3

class DBHandler():

	def __init__(self):
		self.__conn = sqlite3.connect('main.db')

	# Access connection to database
	def getCon(self):
		return self.__conn


	# Insert a new user into the 'user' table
	def insertUser(self, username, passwordHash):
		cur = self.__conn.cursor()
		try:
			cur.execute("INSERT INTO user (username, password) VALUES ('%s', '%s')" % (username, passwordHash))
			self.__conn.commit()

		except sqlite3.IntegrityError as ie:
			raise UsernameExistsException(username)
