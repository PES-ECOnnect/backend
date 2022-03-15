from flask import Flask, request
from random import randint
from CustomExceptions import UsernameExistsException
from User import User

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
      return 0; 

    except UsernameExistsException as ue:
      print(ue.message) # Debug
      
      # Failed to create user because username already exists
      return ERR_USERNAME_EXISTS;

@app.route("/admin/login")
def adminUser():
  n = request.args.get('name')
  p = request.args.get('password')
  
  return {
    'atok': getAdminToken(n, p)
  }


if __name__ == "__main__":
  app.run()