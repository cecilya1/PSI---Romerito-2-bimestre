PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pecas(
    id INTEGER PRIMARY KEY NOT NULL,
    nome TEXT NOT NULL UNIQUE,
    turma TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dancas(
    id INTEGER PRIMARY KEY NOT NULL,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL,
    user_id REFERENCES users
);