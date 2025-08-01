from flask import Flask
from flask import redirect, render_template, url_for, request, make_response
from flask_login import UserMixin, login_manager, LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = 'Esconda-me'

class User(UserMixin):
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
    
    @classmethod
    def get(cls, user_id):
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
        sql = 'SELECT * FROM usuario WHERE usu_id = ?'
        resultado = conn.execute(sql, (user_id,)).fetchone()
        conn.close()
        if resultado:
            user = User(nome=resultado['usu_nome'], email=resultado['usu_email'], senha=resultado['usu_senha'])
            user.id = resultado['usu_id']
            return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']
        senha_crip = generate_password_hash(senha)
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
        sql = 'INSERT INTO usuario (usu_nome, usu_email, usu_senha) VALUES(?, ?, ?)'
        conn.execute(sql, (nome, email, senha_crip))
        conn.commit()
        sql = 'SELECT * FROM usuario'
        id = len(conn.execute(sql).fetchall())
        user = User(nome=nome, email=email, senha=senha_crip)
        user.id = id
        login_user(user)
        conn.close()
        ##  Tem que olhar se o Email não já existe no DB
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        senha = request.form['senha']
        email = request.form['email']
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
        sql = 'SELECT * FROM usuario WHERE usu_email = ?'
        resultado = conn.execute(sql, (email,)).fetchone()
        conn.close()
        if resultado and check_password_hash(resultado['usu_senha'], senha):
            user = User(nome=resultado['usu_nome'], email=resultado['usu_email'], senha=resultado['usu_senha'])
            user.id = resultado['usu_id']
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html')
    return render_template('login.html')


@app.route('/registrar_tarefa', methods=['POST', 'GET'])
def registrar_tarefa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form['status']
        data_criacao = request.form['data_criacao']
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
        sql = 'INSERT INTO tarefa (taf_titulo, taf_descricao, taf_status, taf_data_criacao, taf_usu_id) VALUES(?, ?, ?, ?, ?)'
        resultado = conn.execute(sql, (titulo, descricao, status, data_criacao, current_user.id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('registrar_tarefa.html')

@app.route('/tarefas')
def tarefas():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    sql = 'SELECT * FROM tarefa'
    resultado = conn.execute(sql).fetchall()
    conn.close()
    return render_template('tarefas.html', resultado=resultado)

        
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))