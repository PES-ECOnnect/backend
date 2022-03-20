import pytest
import CustomExceptions as ce
import sqlite3
from DBHandler import DBHandler

class TestDBHandlerClass:

	# ------------ 
	# --- USER --- 
	# ------------ 


	# 1. Insert new user

	def testInsertUserSuccess(self):
		u = "TestUsername"
		p = "TestPasswordHash"
		dbh = DBHandler()

		# Insert only one
		dbh.insertUser(u, p)
	
	def testInsertUserDuplicateUsername(self):
		with pytest.raises(ce.UsernameExistsException):
			u = "TestUsername2"
			p = "TestPasswordHash2"
			dbh = DBHandler()
			
			# Insert the same user twice, expect error
			dbh.insertUser(u, p)
			dbh.insertUser(u, p)

	# 2. User not found
	def testExistsUserSuccess(self):
		# Valid username, return valid passwordHash
		dbh = DBHandler()
		before = dbh.existsUser("123456789")
		dbh.insertUser("123456789", "p")
		after = dbh.existsUser("123456789")
		
		assert before == False and after == True

	def testExistsUserNotFound(self):
		with pytest.raises(ce.UserNotFoundException):
			dbh = DBHandler()
			row = dbh.existsUser("987654321")

	# 2. Insert 

	def testSelectUserPassword(self):
		# Valid username, return valid passwordHash
		dbh = DBHandler()
		p = dbh.selectUserPassword("TestUsername")
		assert p == "TestPasswordHash"









	