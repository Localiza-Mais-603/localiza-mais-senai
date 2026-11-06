-- INSERÇÃO DE CATEGORIAS
INSERT INTO `db_localiza`.`categoria` (`nome`) VALUES ('acessórios');
INSERT INTO `db_localiza`.`categoria` (`nome`) VALUES ('EPI');

-- INSERÇÃO DE COORDENADOR
INSERT INTO `db_localiza`.`coordenador` (`cpf`, `nome`, `email`, `senha`) 
VALUES ('23465478921', 'Godofredo Alex', 'godoalex@gmail.com', 'godo12');

--INSERÇÃO DE USUARIOS
INSERT INTO `db_localiza`.`usuarios` (`email`, `cpf`, `nome`, `curso`, `senha`) 
VALUES ('felizsnts@gmail.com', '12367898765', 'felizberta santos', 'desenvolvimento de sistemas', 'feliz09');
INSERT INTO `db_localiza`.`usuarios` (`email`, `cpf`, `nome`, `curso`, `senha`) 
VALUES ('gabriela.p.silva10@aluno.senai.br', '48693273841', 'Gabriela Peratello', 'Desenvolvimento de Sistemas', '1');

-- INSERÇÃO DE ITENS
INSERT INTO `db_localiza`.`item` (`item`, `local`, `data_encontrado`, `descricao`, `cpf_coordenador`, `status`, `id_categoria`, `destino_objeto`) 
VALUES ('óculos', 'biblioteca', '2026-10-09', 'óculos rosa', '23465478921', 'perdido', 1, 'Entregue na coordenação');
INSERT INTO `db_localiza`.`item` (`item`, `local`, `data_encontrado`, `descricao`, `email`, `status`, `id_categoria`, `destino_objeto`) 
VALUES ('garrafinha', 'refeitório', '2026-10-09', 'Garrafinha azul', 'felizsnts@gmail.com', 'perdido', 1, 'Deixado no local');