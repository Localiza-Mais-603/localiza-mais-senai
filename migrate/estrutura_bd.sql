CREATE TABLE categoria (
 id_categoria INT NOT NULL PRIMARY KEY,
 nome VARCHAR(20)
);


CREATE TABLE coordenador (
 cpf VARCHAR(12) NOT NULL PRIMARY KEY,
 nome VARCHAR(30),
 email VARCHAR(20),
 senha VARCHAR(200)
);


CREATE TABLE usuarios (
 email VARCHAR(20) NOT NULL PRIMARY KEY,
 cpf VARCHAR(12) NOT NULL,
 nome VARCHAR(30),
 curso VARCHAR(30),
 senha VARCHAR(200)
);


CREATE TABLE item (
 id_item INT NOT NULL PRIMARY KEY,
 item VARCHAR(20),
 local VARCHAR(20),
 data_encontrado DATE,
 foto VARCHAR(200),
 descricao VARCHAR(200),
 email VARCHAR(20),
 cpf VARCHAR(12),
 status VARCHAR(10),
 data_devolvido_descartado DATE,
 id_categoria INT,

 FOREIGN KEY (email) REFERENCES usuarios (email),
 FOREIGN KEY (cpf) REFERENCES coordenador (cpf),
 FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
);


