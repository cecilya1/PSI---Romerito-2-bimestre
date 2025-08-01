from flask import Flask
from flask import redirect, render_template, request, url_for, make_response
from flask_login import UserMixin, login_manager, LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = "Esconda-me"

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
        email = request.form['email']
        senha = request.form['senha']
        senha_crip = generate_password_hash(senha)
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
        sql = 'INSERT INTO usuario (usu_nome, usu_email, usu_senha) VALUES (?, ?, ?)'
        conn.execute(sql, (nome, email, senha_crip))
        conn.commit()
        id = len(conn.execute('SELECT * FROM usuario').fetchall())
        conn.close()
        user = User(nome=nome, email=email, senha=senha_crip)
        user.id = id
        login_user(user)
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        senha_crip = generate_password_hash(senha)
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
        sql = 'SELECT * FROM usuario WHERE usu_email = ?'
        resultado = conn.execute(sql, (email,)).fetchone()
        conn.close()
        if resultado and check_password_hash(resultado['usu_senha'], senha):
            user = User(nome=resultado['usu_nome'], email=resultado['usu_email'], senha=resultado['usu_senha'])
            user.id = resultado['usu_id']
            return redirect(url_for('index'))
        return render_template('login.html')
    return render_template('login.html')