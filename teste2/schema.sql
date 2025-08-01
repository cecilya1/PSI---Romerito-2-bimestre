PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuario(
    usu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usu_nome TEXT NOT NULL,
    usu_email TEXT NOT NULL,
    usu_senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tarefa(
    taf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    taf_titulo TEXT NOT NULL,
    taf_descricao TEXT NOT NULL,
    taf_status  TEXT NOT NULL,
    taf_data_criacao DATE NOT NULL,
    taf_usu_id INTEGER REFERENCES usuario
);