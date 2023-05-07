from main import app 
import sqlite3 as sql 
from datetime import datetime
import time as tm 
import random

def getWeek():
    # cria um dicionário com os nomes dos dias da semana em inglês e português
    dias_da_semana = {'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
                      'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
    
    # cria uma data
    data = datetime.now()
    
    # formata a data para exibir o dia da semana em inglês
    dia_da_semana_en = data.strftime('%A')
    
    # obtém o nome correspondente em português
    dia_da_semana_pt = dias_da_semana[dia_da_semana_en]
    
    # exibe o dia da semana em português
    return dia_da_semana_pt



class Task():
    def __init__(self, file, user):
        self.file = file 
        self.user = user 
        self.timeDefault = "Nenhum"

    def create_task(self, name, description, time):
        if name == "" or description == "" or time == "" or not time:
            return "Preciso de nome e descrição válido"
    
        # Salva tudo no banco de dados 
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('INSERT INTO tasks (name,description,autor,time,status) VALUES (?,?,?,?,?)', (name,description,self.user,time,"pendente"))
        db.commit()
        db.close()

        return "Tarefa adicionada"
    
    def concluir_task(self,name,description, coin):
        # Verificando se concluiu antes do prazo
        tm.sleep(random.randint(0,5))
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('SELECT time FROM tasks WHERE autor = ? AND name = ? AND description = ?', (self.user, name, description))
        dia_estimado = cursor.fetchone()
        db.close()
        print(dia_estimado)
        data_estimada_formatada = dia_estimado[0].split('/')
        data_estimada = datetime(int(data_estimada_formatada[2]), int(data_estimada_formatada[1]), int(data_estimada_formatada[0]))
        print(data_estimada)
        hoje = datetime.now()
        r = ""
        if hoje < data_estimada:
            r = "Tarefa concluída antes do prazo, ganhou mais 10 pontos!!" 
            Users('users.db', self.user).add_coin(self.user, 10, coin)
        if hoje > data_estimada:
            r = "Tarefa concluída depois do prazo, perdeu 5 pontos..."
            Users('users.db', self.user).delete_coin(self.user, 10, coin)
        else:
          r = "Tarefa concluída dentro do prazo, ganhou 5 pontos!"
          Users("users.db", self.user).add_coin(self.user, 5, coin)

        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('UPDATE tasks SET status = ?, dia_concluido = ? WHERE name = ? AND description = ? AND autor = ?', ("concluido", getWeek() ,name,description,self.user))
        db.commit()
        db.close()

        return {
            "message": "Tarefa concluída com sucesso",
            "status": r 
        }
    
    def excluir_task(self,name,description):
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('DELETE FROM tasks WHERE name = ? AND description = ? AND autor = ?', (name,description,self.user))
        db.commit()
        db.close()

        return {
            "message": "Tarefa excluída com sucesso!"
        }

    def editar(self,name,description,newName,prazo):
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('UPDATE tasks SET name = ?, description = ?, time = ? WHERE name = ? AND autor = ?', (newName, description,prazo,name,self.user))
        db.commit()
        db.close()

        return {
            "message": "Tarefa editada com sucesso!"
        }

    def getDiasMaisProdutivos(self):
      db = sql.connect("tasks.db")
      cursor = db.cursor()
      cursor.execute("""
      SELECT dia_concluido, COUNT(*) as total_concluidas
FROM tasks
WHERE status = 'concluido' AND autor = ?
GROUP BY dia_concluido
ORDER BY total_concluidas DESC;
      """, (self.user,))
      fetch = cursor.fetchall()
      db.close()

      dias = []

      if len(fetch) >= 0:
        for dia in fetch:
          dias.append(f"{dia[0]} - {dia[1]} <br>")

      else:
        dias.append("Sem tarefas Concluídas")

      return dias

Task("tasks.db", "guxtavodev").getDiasMaisProdutivos()
    
class Users():
    def __init__(self, file, user) -> None:
        self.file = file 
        self.user = user or None
    
    def criar_usuario(self, username, password):
        # Verificando se já existe uma pessoa com o mesmo nome de usuário
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        fe = cursor.fetchone()
        db.close()
        print(fe)
        if fe != None:
            return {
                "message": "Já existe usuário com este nome"
            }
        
        # Salvando no banco de dados
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username,password) VALUES (?,?)', (username,password))
        db.commit()
        db.close()

        return {
            "message": "Usuário cadastrado com sucesso!",
            "coins": 0
        }
    
    def excluir_usuario(self, username):
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username))
        db.commit()
        db.close()

        return {
            "message": "Usuário excluido com sucesso"
        }
    
    def add_coin(self, username, coins, coin):
        db = sql.connect('coins.db')
        cursor = db.cursor()
        cursor.execute('SELECT coins FROM coins_users WHERE user = ?', (username,))
        coins_antes = cursor.fetchone()
        db.close()

        if coins_antes == None:
            db = sql.connect('coins.db')
            cursor = db.cursor()
            cursor.execute('INSERT INTO coins_users (coins,user) VALUES (?,?)', (0,username))
            db.commit()
            db.close()
            coins_antes = 0

        # Soma com o novo valor
        coins_depois = coin + coins

        # Adiciona 
        db = sql.connect('coins.db')
        cursor = db.cursor()
        cursor.execute('UPDATE coins_users SET coins = ? WHERE user = ?', (coins_depois, username))
        db.commit()
        db.close()

    def delete_coin(self, username, coins, coin):
        db = sql.connect('coins.db')
        cursor = db.cursor()
        cursor.execute('SELECT coins FROM coins_users WHERE user = ?', (username,))
        coins_antes = cursor.fetchone()
        db.close()

        if coins_antes == None:
            db = sql.connect('coins.db')
            cursor = db.cursor()
            cursor.execute('INSERT INTO coins_users (coins,user) VALUES (?,?)', (0,username))
            db.commit()
            db.close()
            coins_antes = 0

        # Soma com o novo valor
        coins_depois = coin - int(coins)

        # Adiciona 
        db = sql.connect('coins.db')
        cursor = db.cursor()
        cursor.execute('UPDATE coins_users SET coins = ? WHERE user = ?', (coins_depois, username))
        db.commit()
        db.close()

    def get_coins(self, username):
        db = sql.connect('coins.db')
        cursor = db.cursor()
        cursor.execute('SELECT coins FROM coins_users WHERE user = ?', (username,))
        fetch = cursor.fetchone()
        db.close()

        if fetch is None:
          return {
            "user": self.user,
            "coins":0 
          }

        return {
            "user": self.user,
            "coins": int(fetch[0]) 
        }

    def auth_user(self, username, password):
        db = sql.connect(self.file)
        cursor = db.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        fetch = cursor.fetchone()
        db.close()

        if fetch == None:
            return {
                "message": "Usuário não existe"
            }
        
        if password == fetch[0]:
          
            return {
                "message": "Senha correta",
                "coins": self.get_coins(username)["coins"]
            }
          
        else:
            return {
                "message": "Senha incorreta"
            }