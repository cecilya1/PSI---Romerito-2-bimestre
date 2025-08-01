
-- DROP TABLE tb_alunos;

CREATE TABLE IF NOT EXISTS tb_alunos(
    alu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alu_nome TEXT NOT NULL,
    alu_matricula TEXT NOT NULL,
    alu_senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_pecas(
    pec_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pec_nome TEXT NOT NULL,
    pec_turma TEXT NOT NULL,
    pec_alu_id INTEGER REFERENCES tb_alunos 
);

CREATE TABLE IF NOT EXISTS tb_dancas(
    dan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dan_nome TEXT NOT NULL,
    dan_categoria TEXT NOT NULL,
    dan_descricao TEXT NOT NULL,
    dan_alu_id INTEGER REFERENCES tb_alunos 
);