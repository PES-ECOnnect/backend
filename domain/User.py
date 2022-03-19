from data.DBSessionToken import DBSessionToken
import CustomExceptions as ce
import json

class User:

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password



	@staticmethod
	def logout(token):
		return DBSessionToken.delete(token)



'''

# Insert a new user into the 'user' table
	def insertUser(self, username, passwordHash):
		cur = self.__conn.cursor()
		try:
			cur.execute("INSERT INTO user (username, password) VALUES ('%s', '%s')" % (username, passwordHash))
			self.__conn.commit()
			cur.close()

		except sqlite3.IntegrityError as ie:
			raise ce.UsernameExistsException(username)

	# Insert a new user into the 'user' table
	def existsUser(self, username):
		cur = self.__conn.cursor()
		cur.execute("SELECT 1 FROM user WHERE EXISTS username = '%s'" % username)
		self.__conn.commit()

		b = cur.fetchone()
		cur.close()
		return b

	# Insert a new user into the 'user' table
	def selectUserPassword(self, username):
		cur = self.__conn.cursor()
		cur.execute("SELECT password FROM user WHERE username = '%s'" % username)
		row = cur.fetchone()
		cur.close()
		self.__conn.commit()

		if row['password'] == None:
			raise ce.UsernameNotFound(username)

		return row['password']

			
	def selectUserIsAdmin(self, username):
		cur = self.__conn.cursor()
		isAdmin = cur.execute("SELECT isAdmin FROM user WHERE username = '%s'" % username).fetchone()
		self.__conn.commit()

		if isAdmin == None:
			raise ce.UserNotFoundException(username)

		print(isAdmin, "---------------------")
		return isAdmin


'''