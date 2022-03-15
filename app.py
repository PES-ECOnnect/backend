from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "PES Econnect Root!"

@app.route("/")
def hello_world():


if __name__ == "__main__":
  app.run()
  
  
