from flask import Flask
from flask import redirect, url_for, render_template, request, flash
from flask_login import login_manager, LoginManager, current_user, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = "Esconda-me"

def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn
class User(UserMixin):
    def __init__(self, nome, matricula, senha):
        self.nome = nome
        self.matricula = matricula
        self.senha = senha
    
    @classmethod
    def get(cls, user_id):
        conn = obter_conexao()
        sql = 'SELECT * FROM tb_alunos WHERE alu_id = ?'
        resultado = conn.execute(sql, (user_id,)).fetchone()
        if resultado:
            user = User(nome=resultado['alu_nome'], matricula=resultado['alu_matricula'], senha=resultado['alu_senha'])
            user.id = resultado['alu_id']
            return user
        
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        senha = request.form['senha']
        conn = obter_conexao()
        sql = 'SELECT * FROM tb_alunos WHERE alu_matricula = ?'
        resultado = conn.execute(sql, (matricula,)).fetchone()
        if not resultado:
            sql2 = 'INSERT INTO tb_alunos(alu_nome, alu_matricula, alu_senha) VALUES (?, ?, ?)'
            senha_crip = generate_password_hash(senha)
            conn.execute(sql2, (nome, matricula, senha_crip))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        flash('Já existe uma pessoa cadastrada com essa matricula', category='erro')
        return redirect(url_for('cadastro'))
    return render_template('cadastro.html')

@app.route('/buscar_usuario', methods = ['POST', 'GET'])
def buscar_usuario():
    if request.method == 'POST':
        matricula = request.form["matricula"]
        conn = obter_conexao()
        sql = 'SELECT * FROM tb_alunos WHERE alu_matricula = ?'
        resultado = conn.execute(sql, (matricula,)).fetchone()
        conn.close()
        if resultado:
            resultado = list(resultado)
            flash(resultado, category='mostrar_usuario')
            return redirect(url_for('buscar_usuario'))
        flash('Não existe nenhuma pessoa cadastrada com essa matricula', category='erro')
        return redirect(url_for('buscar_usuario'))
    return render_template('buscar_usuario.html')

@app.route('/mostrar_usuario')
def mostrar_usuario():
    matricula = request.args.get("matricula")
    conn = obter_conexao()
    sql = 'SELECT * FROM tb_alunos WHERE alu_matricula = ?'
    resultado = conn.execute(sql, (matricula,)).fetchone()
    conn.close()
    resultado = list(resultado)
    flash(resultado, category='mostrar_usuario')
    return render_template('mostrar_usuario.html')

@app.route('/cadastrar_peca', methods = ['POST', 'GET'])
def cadastrar_peca():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        turma = request.form['turma']
        conn = obter_conexao()
        sql = 'SELECT * FROM tb_alunos WHERE alu_matricula = ?'
        resultado = conn.execute(sql, (matricula,)).fetchone()
        if resultado:
            sql2 = 'INSERT INTO tb_pecas(pec_nome, pec_turma, pec_alu_id) VALUES (?, ?, ?)'
            conn.execute(sql2, (nome, turma, resultado['alu_id']))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        flash('Não existe nenhuma pessoa cadastrada com essa matricula', category='erro')
        return redirect(url_for('cadastrar_peca'))
    return render_template('cadastrar_peca.html')

@app.route('/listar_usuarios', methods = ['POST', 'GET'])
def listar_usuarios():
    # if request.method == 'POST':
    #     return redirect(url_for('usuario'))
    conn = obter_conexao()
    sql = 'SELECT * FROM tb_alunos'
    resultado = conn.execute(sql).fetchall()
    conn.close()
    return render_template('listar_usuarios.html', lista=resultado)

@app.route('/buscar_peca', methods = ['POST', 'GET'])
def buscar_peca():
    if request.method == 'POST':
        matricula = request.form["matricula"]
        nome = request.form['nome']
        conn = obter_conexao()
        resultado2 = conn.execute('SELECT * FROM tb_alunos WHERE alu_matricula = ?', (matricula,)).fetchone()
        if resultado2:
            sql = 'SELECT * FROM tb_pecas WHERE pec_nome = ? AND pec_alu_id = ?'
            resultado = conn.execute(sql, (nome, resultado2['alu_id'])).fetchone()
            conn.close()
            if resultado:
                resultado = list(resultado)
                flash(resultado, category='mostrar_peca')
                return redirect(url_for('buscar_peca'))
        flash('Não existe nenhuma peça cadastrada com esses dados', category='erro')
        return redirect(url_for('buscar_peca'))
    return render_template('buscar_peca.html')

@app.route('/listar_pecas', methods = ['POST', 'GET'])
def listar_pecas():
    if request.method == 'POST':
        id = request.form["id"]
        conn = obter_conexao()
        sql = 'DELETE FROM tb_pecas WHERE pec_id = ?'
        conn.execute(sql, (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pecas'))
    conn = obter_conexao()
    sql = 'SELECT * FROM tb_pecas'
    resultado = conn.execute(sql).fetchall()
    conn.close()
    return render_template('listar_pecas.html', lista=resultado)

@app.route('/mostrar_peca')
def mostrar_peca():
    id = request.args.get("id")
    conn = obter_conexao()
    sql = 'SELECT * FROM tb_pecas WHERE pec_id = ?'
    resultado = conn.execute(sql, (id,)).fetchone()
    conn.close()
    resultado = list(resultado)
    flash(resultado, category='mostrar_peca')
    return render_template('mostrar_peca.html')

@app.route('/cadastrar_danca', methods = ['POST', 'GET'])
def cadastrar_danca():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        categoria = request.form['categoria']
        discricao = request.form['descricao']
        conn = obter_conexao()
        sql = 'SELECT * FROM tb_alunos WHERE alu_matricula = ?'
        resultado = conn.execute(sql, (matricula,)).fetchone()
        if resultado:
            sql2 = 'INSERT INTO tb_dancas(dan_nome, dan_categoria, dan_descricao, dan_alu_id) VALUES (?, ?, ?, ?)'
            conn.execute(sql2, (nome, categoria, discricao, resultado['alu_id']))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        flash('Não existe nenhuma pessoa cadastrada com essa matricula', category='erro')
        return redirect(url_for('cadastrar_danca'))
    return render_template('cadastrar_danca.html')


@app.route('/editar_peca', methods = ['POST', 'GET'])
def editar_peca():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        turma = request.form['turma']
        id = request.form["id"]
        conn = obter_conexao()
        resultado = conn.execute('SELECT * FROM tb_alunos WHERE alu_matricula = ?', (matricula,))
        if resultado:
            sql = 'UPDATE tb_peca SET pec_nome = ?, pec_turma = ?, pec_alu_id = ? WHERE pec_id = ?'
            conn.execute(sql, (nome, turma, resultado['alu_id'], id))
            conn.commit()
            conn.close()
        flash('Não existe nenhuma pessoa cadastrada com essa matricula', category='erro')
        return redirect(url_for('editar_peca', resultado=resultado))

    id = request.args.get("id")
    conn = obter_conexao()
    sql = 'SELECT * FROM tb_pecas WHERE pec_id = ?'
    resultado = conn.execute(sql, (id,))
    conn.close()
    return redirect(url_for('editar_peca', resultado=resultado))


@app.route('/editar_peca', methods = ['POST', 'GET'])
def finalizar_peca():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        turma = request.form['turma']
        id = request.form["id"]
        conn = obter_conexao()
        resultado = conn.execute('SELECT * FROM tb_alunos WHERE alu_matricula = ?', (matricula,))
        if resultado:
            sql = 'UPDATE tb_peca SET pec_nome = ?, pec_turma = ?, pec_alu_id = ? WHERE pec_id = ?'
            conn.execute(sql, (nome, turma, resultado['alu_id'], id))
            conn.commit()
            conn.close()
        flash('Não existe nenhuma pessoa cadastrada com essa matricula', category='erro')
        return redirect(url_for('editar_peca', resultado=resultado))
    return redirect(url_for('editar_peca'))