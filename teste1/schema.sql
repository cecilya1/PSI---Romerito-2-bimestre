PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuario(
    usu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usu_nome TEXT NOT NULL,
    usu_email TEXT NOT NULL,
    usu_senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evento(
    eve_id INTEGER PRIMARY KEY AUTOINCREMENT,
    eve_nome TEXT NOT NULL,
    eve_data DATE NOT NULL,
    eve_usu_id INTEGER REFERENCES usuario
)