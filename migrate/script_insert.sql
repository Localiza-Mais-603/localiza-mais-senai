INSERT INTO `db_localiza`.`categoria` (`nome`) VALUES ('acessórios');
INSERT INTO `db_localiza`.`categoria` (`nome`) VALUES ('EPI');

INSERT INTO `db_localiza`.`coordenador` (`cpf`, `nome`, `email`, `senha`) VALUES ('234654789222', 'Godofredo Alex', 'godoalex@gmail.com', 'godo12');

INSERT INTO `db_localiza`.`usuarios` (`email`, `cpf`, `nome`, `curso`, `senha`) VALUES ('felizsnts@gmail.com', '12367898765', 'felizberta santos', 'desenvolvimento de sistemas ', 'feliz09');

INSERT INTO `db_localiza`.`item` (`item`, `local`, `data_encontrado`, `descricao`, `cpf_coordenador`, `status`, `id_categoria`) VALUES ('óculos', 'biblioteca', '2026-10-09', 'óculos rosa', '234654789222', 'perdido', '1');
INSERT INTO `db_localiza`.`item` (`item`, `local`, `data_encontrado`, `descricao`, `email`, `status`, `id_categoria`) VALUES ('garrafinha', 'referitório', '2026-10-09', 'Garrafinha azul', 'felizsnts@gmail.com', 'perdido', '1');
