from flask import Flask, jsonify, request 
import sqlite3 as sql 
import time


app = Flask(__name__, template_folder='views')

# Pega os usuários todos
db = sql.connect("users.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM users")
fetch = cursor.fetchall()
db.close()

print(f"Usuarios: {len(fetch)}")

for user in fetch:
  print(user[0])

print(fetch)

#db = sql.connect("users.db")
#cursor = db.cursor()
#cursor.execute("DELETE FROM users WHERE username = 'gustavorochabr'")
#db.commit()
#db.close()

from views import *

if __name__ == "__main__":
    app.run(port=9090, host="0.0.0.0", debug=True)