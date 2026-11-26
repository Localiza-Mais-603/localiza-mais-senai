CREATE DATABASE IF NOT EXISTS db_localiza;
USE db_localiza;

-- TABELA DE CATEGORIAS
CREATE TABLE categoria (
    id_categoria INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL
);

-- TABELA DE COORDENADORES (Setor de Apoio)
CREATE TABLE coordenador (
    cpf VARCHAR(11) NOT NULL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    senha VARCHAR(200) NOT NULL,
    token_recuperacao VARCHAR(255) NULL
);

-- TABELA DE USUÁRIOS (Alunos)
CREATE TABLE usuarios (
    email VARCHAR(200) NOT NULL PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    curso VARCHAR(50),
    senha VARCHAR(200) NOT NULL,
    token_recuperacao VARCHAR(255) NULL
);

-- TABELA DE ITENS (Perdidos / Encontrados)
CREATE TABLE item (
    id_item INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(50) NOT NULL,
    local VARCHAR(50),
    data_encontrado DATE,
    foto VARCHAR(200),
    descricao VARCHAR(255) NOT NULL,
    email VARCHAR(200),
    cpf_coordenador VARCHAR(11),
    status VARCHAR(20) NOT NULL,
    id_categoria INT,
    destino_objeto VARCHAR(150) NULL,

    FOREIGN KEY (email) REFERENCES usuarios (email),
    FOREIGN KEY (cpf_coordenador) REFERENCES coordenador (cpf),
    FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
);

-- TABELA DE ITENS RETIRADOS
CREATE TABLE retirada (
    id_retirada INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_item INT NOT NULL,
    nome_retirante VARCHAR(100) NOT NULL,
    telefone_retirante VARCHAR(20) NOT NULL,
    curso_retirante VARCHAR(50) NOT NULL,
    email_retirante VARCHAR(200) NULL,
    cpf_retirante VARCHAR(11) NULL,
    data_retirada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_item) REFERENCES item (id_item)
);

-- TABELA DE OPÇÕES DE DESTINO (para o dropdown)
CREATE TABLE destino_opcao (
    id_destino INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    descricao VARCHAR(150) NOT NULL
);

ALTER TABLE item
ADD COLUMN nome_retirante VARCHAR(150) NULL,
ADD COLUMN email_retirante VARCHAR(150) NULL,
ADD COLUMN data_retirada DATETIME NULL;