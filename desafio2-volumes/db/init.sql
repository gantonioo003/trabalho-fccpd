CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL
);

INSERT INTO usuarios (nome) VALUES
('Ana'),
('Bruno'),
('Carlos');
