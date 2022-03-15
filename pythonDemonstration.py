from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Hello World!"

@app.route("/random-inserts")
def random_inserts():
  con = sqlite3.connect('main.db')
  cur = con.cursor()
  for i in range(0,10):
    cur.execute("INSERT INTO user (name, email) VALUES ('User %d','Email %d')" % (i, i))

  # Save (commit) the changes
  con.commit()
  con.close()
  
  return "Inserted random users successfully."

@app.route("/list-users")
def list_users():
  con = sqlite3.connect('main.db')
  con.row_factory = sqlite3.Row # allow associative query result in form of python dictionary
  cur = con.cursor()
  s = "<table><tr><th>ID</th><th>Name</th><th>Email</th></tr>"
  i = 0
  for row in cur.execute("SELECT * FROM user"):
  	bgColor = "white" if i%2 else "#DBDBDB"  
  	s += "<tr style= 'background-color: %s'>" % (bgColor)
  	s += "<td>[%d]</td><td>%s</td><td>%s</td></tr>" % (row['id'], row['name'], row['email'])
  	i += 1

  s += "</table>"

  return s


if __name__ == "__main__":
  app.run()
  
  
