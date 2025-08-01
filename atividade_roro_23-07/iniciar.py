import sqlite3

# estabelecer uma conexão
# --"banco.db" é o databasse
conexao = sqlite3.connect('banco.db')

# executar instrução de criação de tabela(s)

with open('schema.sql') as f:
    # manda a conexão executar como SCRIPTS
    conexao.executescript(f.read())
    # conexao.executemany(f.read())

# fechar conexão
conexao.close()