from flask import Flask, request
from random import randint
import CustomExceptions as ce
from domain.User import User
import json

# Error codes
# TODO: Move into separate file
ERR_USERNAME_EXISTS = 10001


app = Flask(__name__)

@app.route("/")
def helloWorld():
	return "PES Econnect Root!"

@app.route("/account", methods = ['POST'])
def registerUser():
	# TODO: Use POST request instead of test data

	if request.method == 'POST':
		# Create account
		username = request.form['username']
		username = request.form['email']
		password = request.form['password']

		username = "TestUser" + str(randint(1, 10000))
		password = "TestPass" + str(randint(1, 10000))

		try:
			User.register(username, password)
			
			# User created successfully
			return 0 

		except UsernameExistsException as ue:
			print(ue.message) # Debug
			
			# Failed to create user because username already exists
			return ERR_USERNAME_EXISTS;

@app.route("/account/logout", methods = ['GET'])
def logout():
	tok = request.args.get('token')
	try:
		User.logout(tok);
	except ce.InvalidTokenException as invalidTokenException:
		return json.dumps({
			'error': {
				'name': 'ERROR_INVALID_TOKEN',
				'message': invalidTokenException.message
			}
		})
	return json.dumps({})


@app.route("/admin/login")
def adminUser():
	aUsername = request.args.get('name')
	aPassword = request.args.get('password')
	
	try:
		# If user is not even admin, error.
		if not User.isAdmin(aUsername):
			return json.dumps({
				'error' : {
					'name': 'ERROR_USER_NOT_ADMIN',
					'message': "Username " + aUsername + " is not admin" 
				}
			})

		# Try to log in
		token = User.login(aUsername, aPassword)
		return json.dumps({
			'token': token
		})

	except ce.UserNotFoundException as userNotFoundException:
		return json.dumps({
			'error' : {
				'name': 'ERROR_USER_NOT_FOUND',
				'message': userNotFoundException.message 
			}
		})

	except ce.IncorrectUserPasswordException as incorrectUserException:
		return json.dumps({
			'error' : {
				'name': 'ERROR_USER_INCORRECT_PASSWORD',
				'message': incorrectUserException.message 
			}
		})

'''@app.route("/products/<id>/answer")
def adminUser(id):'''
if __name__ == "__main__":
		app.debug = True
		app.run()