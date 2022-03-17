
class DBUser:

	def __init__(self):
		self.__conn = sqlite3.connect('main.db')
		self.__conn.row_factory = sqlite3.Row

	def insert(user):
		pass

	def delete(user):
		pass

	def update(user):
		pass

	def select(username):
		pass