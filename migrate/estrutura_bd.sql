CREATE DATABASE IF NOT EXISTS db_localiza;
USE db_localiza;

CREATE TABLE categoria (
 id_categoria INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 nome VARCHAR(20) NOT NULL
);


CREATE TABLE coordenador (
 cpf VARCHAR(12) NOT NULL PRIMARY KEY,
 nome VARCHAR(30) NOT NULL,
 email VARCHAR(200) NOT NULL,
 senha VARCHAR(200) NOT NULL
);


CREATE TABLE usuarios (
 email VARCHAR(200) NOT NULL PRIMARY KEY,
 cpf VARCHAR(12) NOT NULL,
 nome VARCHAR(30) NOT NULL,
 curso VARCHAR(30),
 senha VARCHAR(200) NOT NULL
);


CREATE TABLE item (
 id_item INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 item VARCHAR(20) NOT NULL,
 local VARCHAR(20),
 data_encontrado DATE NOT NULL,
 foto VARCHAR(200),
 descricao VARCHAR(200) NOT NULL,
 email VARCHAR(200),
 cpf_coordenador VARCHAR(12),
 status VARCHAR(10) NOT NULL,
 data_devolvido_descartado DATE,
 id_categoria INT,

 FOREIGN KEY (email) REFERENCES usuarios (email),
 FOREIGN KEY (cpf_coordenador) REFERENCES coordenador (cpf),
 FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
);


