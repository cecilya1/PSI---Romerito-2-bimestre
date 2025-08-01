from flask import Flask, render_template
from flask import request, session, redirect, url_for
from flask import flash

from flask_login import LoginManager, UserMixin, logout_user
from flask_login import login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = 'chave_secreta'

def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn


class User(UserMixin):
    def __init__(self, nome, senha) -> None:
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        # user_id nesse caso é um nome
        conexao = obter_conexao()
        sql = "select * from users where id = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        if resultado:
            user = User(nome=resultado['nome'], senha=resultado['senha'])
            user.id = resultado['id']
            return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']
        
        conexao = obter_conexao()
        sql = "select * from users where nome = ? and senha = ?"
        resultado = conexao.execute(sql, (nome,senha)).fetchone()
        if resultado:
            user = User(nome=resultado['nome'], senha=resultado['senha'])
            id = len(conexao.execute('SELECT * FROM users').fetchall())
            user.id = id
            login_user(user)
            return redirect(url_for('dash'))
        flash('Dados incorretos', category='error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']

        # obter uma conexao
        conexao = obter_conexao()
        sql = "select * from users where nome = ?"
        resultado = conexao.execute(sql, (nome,)).fetchone()
        if not resultado:
            sql = "INSERT INTO users(nome, senha) VALUES (?, ?)"
            conexao.execute(sql, (nome, senha))
            conexao.commit()
            
            user = User(nome=nome, senha=senha)
            id = len(conexao.execute('SELECT * FROM users').fetchall())
            user.id = id

            login_user(user)

            #flash('Cadastro realizado com secesso', category='error')
            return redirect(url_for('login'))

        conexao.close()
        flash('Problema no cadastro', category='error')
        return redirect(url_for('register'))

    return render_template('register.html')

@login_required
@app.route('/festa', methods=['GET', 'POST'])
def festa():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        conexao = obter_conexao()
        conexao.execute('PRAGMA foreign_keys = ON')
        sql = 'INSERT INTO festa(nome, valor, user_id) VALUES(?, ?, ? )'
        conexao.execute(sql, (nome, valor, current_user.id)).fetchone()
        conexao.commit()
        return 'A festa foi cadastrada'
    return render_template('festa.html')

@app.route('/dashboard')
@login_required
def dash():
    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))