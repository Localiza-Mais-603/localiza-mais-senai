CREATE TABLE cadastro_coor (
 cpf_coor VARCHAR(11)  PRIMARY KEY,
 id_coor INT,
 nome VARCHAR(50),
 email VARCHAR(100),
 senha VARCHAR(100)
);

CREATE TABLE cadastro_item (
 id_item INT PRIMARY KEY,
 id_coord INT,
 item VARCHAR(10),
 descricao VARCHAR(500),
 data DATE,
 local VARCHAR(20),
 status CHAR(15)
);


CREATE TABLE cadastro_usuario (
 cpf_usuario VARCHAR(11) PRIMARY KEY,
 id_usuario INT,
 nome VARCHAR(50),
 curso VARCHAR(50),
 email VARCHAR(100),
 senha VARCHAR(100)
);


CREATE TABLE item_devolvido (
 id_item_devolvido INT PRIMARY KEY,
 id_item_0 INT NOT NULL,
 data DATE,
 id_usuario INT,
CONSTRAINT FK_item_devolvido_0 FOREIGN KEY (id_item_0) REFERENCES cadastro_item (id_item)
);