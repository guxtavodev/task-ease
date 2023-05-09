from app import app 
from models import Users, Task 
from flask import request, render_template, jsonify
import sqlite3 as sql
import time 
import random

@app.route('/api/cadastro', methods=['POST'])
def cadastrarUser():
    data = request.get_json()

    return jsonify({
        "response": Users('users.db', data["username"]).criar_usuario(data['username'], data['password'])
    })

@app.route('/api/auth', methods=["GET"])
def entrar():
    username = request.args.get('username')
    password = request.args.get('password')

    return jsonify({
        "response": Users('users.db', username).auth_user(username, password)
    })

@app.route("/cadastro")
def cadastroPage():
    return render_template('cadastro.html')

@app.route("/conectar")
def conectarPage():
    return render_template('entrar.html')

@app.route('/api/create-task', methods=['POST'])
def criarTask():
    data = request.get_json()
    time.sleep(random.randint(0,3))

    return jsonify({
        "response": Task('tasks.db', data['user']).create_task(data['name'], data['description'], data['conclusion'])
    })

@app.route('/home/')
def homepage():
    return render_template('index.html')

@app.route('/api/tasks/<user>', methods=['GET'])
def getTasks(user):
    db = sql.connect('tasks.db')
    cursor = db.cursor()
    cursor.execute('SELECT name, description, time, status FROM tasks WHERE autor = ?', (user,))
    fetch = cursor.fetchall()
    db.close()

    

    tasks = []

    for task in fetch:
        tasks.append({
            "name": task[0],
            "description": task[1],
            "conclusion": task[2],
            "status": task[3]
        })

    return jsonify({
        "message": tasks,
        "days": Task("tasks.db", user).getDiasMaisProdutivos()
    })

@app.route("/api/concluir-task", methods=['POST'])
def concluirTask():
    data = request.get_json()

    return jsonify({
        'message': Task('tasks.db', data['user']).concluir_task(data['name'], data['description'], data["coin"])
    })

@app.route('/api/delete', methods=['POST'])
def deleteAccount():
    data = request.get_json()

    return jsonify({
        'response': Users('users.db').excluir_usuario(data['user'])
    })

@app.route("/api/delete/all", methods=["POST"])
def deleteAll():
  data = request.get_json()
  db = sql.connect("tasks.db")
  cursor = db.cursor()
  cursor.execute("DELETE FROM tasks WHERE autor = ?", (data["autor"],))
  db.commit()
  db.close()

  return jsonify({
    "message": "sucesso"
  })

@app.route("/api/delete-task", methods=["POST"])
def deleteTask():
  data = request.get_json()
  return jsonify({
    "message": Task("tasks.db", data["user"]).excluir_task(data["name"], data["description"])
  })

@app.route("/api/edit-username", methods=["POST"])
def editUsername():
    data = request.get_json()

    db = sql.connect("users.db")
    cursor = db.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (data["usernameNew"],))
    fe = cursor.fetchone()
    db.close()
    print(fe)
    if fe != None:
        return jsonify({
                "message": "Já existe usuário com este nome"
            })
    
    with sql.connect("users.db") as db:
      cursor = db.cursor()
    
      # Obtém a senha do usuário atual
      cursor.execute("SELECT password FROM users WHERE username = ?", (data["user"],))
      password = cursor.fetchone()[0]
    
    # Verifica se a senha está correta
      if data["password"] != password:
          return jsonify({"message": "incorrect password"})
    
    # Atualiza o nome de usuário
      cursor.execute("UPDATE users SET username = ? WHERE username = ?", (data["usernameNew"], data["user"]))
      db.commit()

    db = sql.connect("tasks.db")
    cursor.execute("UPDATE tasks SET autor = ? WHERE autor = ?", (data["usernameNew"], data["user"]))
    db.commit()
    db.close()


    return jsonify({"message": "success"})


@app.route("/api/edit-password", methods=["POST"])
def editPassword():
    data =request.get_json()
    db = sql.connect("users.db")
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (data["user"],))
    password = cursor.fetchone()[0]
    db.close()
    
    if data["password"] == password:
        db = sql.connect("users.db")
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (data["passwordNew"], data["user"]))
        db.commit()
        db.close()
        
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "incorret password"})

@app.route("/settings")
def settingsPage():
  return render_template("settings.html")
