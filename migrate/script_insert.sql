-- =============================================
-- 0. COORDENADORES DE EXEMPLO
-- (a FK item.cpf_coordenador exige CPF existente em coordenador)
-- =============================================

INSERT IGNORE INTO coordenador (cpf, nome, email, senha) VALUES
('23465478921', 'Coordenação Exemplo 1', 'coordenacao1@senai.br', 'senha-ficticia-sem-login'),
('34567890122', 'Coordenação Exemplo 2', 'coordenacao2@senai.br', 'senha-ficticia-sem-login'),
('45678901233', 'Coordenação Exemplo 3', 'coordenacao3@senai.br', 'senha-ficticia-sem-login');

SET @cpf1 = '23465478921';
SET @cpf2 = '34567890122';
SET @cpf3 = '45678901233';

-- =============================================
-- 1. NOVAS CATEGORIAS
-- =============================================

-- só insere as categorias que ainda não existem (pode rodar mais de uma vez)
INSERT INTO categoria (nome)
SELECT t.nome FROM (
SELECT 'Papelaria' AS nome UNION ALL
SELECT 'Documentos' AS nome UNION ALL
SELECT 'Bolsas e mochilas' AS nome UNION ALL
SELECT 'Garrafas e utensílios' AS nome UNION ALL
SELECT 'Livros e apostilas' AS nome UNION ALL
SELECT 'Ferramentas' AS nome UNION ALL
SELECT 'Material esportivo' AS nome UNION ALL
SELECT 'Calçados' AS nome UNION ALL
SELECT 'Informática' AS nome UNION ALL
SELECT 'Acessórios' AS nome UNION ALL
SELECT 'Outros' AS nome
) t
WHERE NOT EXISTS (SELECT 1 FROM categoria c WHERE c.nome = t.nome);

-- =============================================
-- 1.1 ALUNOS DE EXEMPLO
-- (a FK item.email exige e-mail existente em usuarios;
--  INSERT IGNORE pula quem já estiver cadastrado)
-- =============================================

INSERT IGNORE INTO usuarios (email, cpf, nome, curso, senha) VALUES
('lucas.ferreira@aluno.senai.br', '51234567890', 'Lucas Ferreira', 'Desenvolvimento de Sistemas', 'senha-ficticia-sem-login'),
('ana.beatriz@aluno.senai.br', '62345678901', 'Ana Beatriz Souza', 'Eletroeletrônica', 'senha-ficticia-sem-login'),
('rafael.mendes@aluno.senai.br', '73456789012', 'Rafael Mendes', 'Mecânica', 'senha-ficticia-sem-login'),
('camila.oliveira@aluno.senai.br', '84567890123', 'Camila Oliveira', 'Logística', 'senha-ficticia-sem-login'),
('gabriela.p.silva10@aluno.senai.br', '95678901234', 'Gabriela Silva', 'Administração', 'senha-ficticia-sem-login');


-- =============================================
-- 2. NOVOS ITENS DISPONÍVEIS
-- =============================================

INSERT INTO item
(item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto)
VALUES

('Mochila preta', 'Sala 103', '2026-11-25', NULL,
'Mochila preta com três compartimentos e zíper cinza',
NULL, @cpf1, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Bolsas e mochilas' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Garrafa térmica', 'Refeitório', '2026-08-14', NULL,
'Garrafa térmica azul de aproximadamente 500ml',
NULL, @cpf2, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Garrafas e utensílios' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Caderno universitário', 'Biblioteca', '2026-05-29', NULL,
'Caderno de capa vermelha com espiral e 10 matérias',
'lucas.ferreira@aluno.senai.br', NULL, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Papelaria' LIMIT 1),
'Ainda estou com o objeto e vou levar à coordenação.'),

('Mouse sem fio', 'Laboratório de Informática', '2026-11-10', NULL,
'Mouse preto sem fio com receptor USB',
NULL, @cpf1, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Informática' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Livro de matemática', 'Sala 205', '2026-06-03', NULL,
'Livro didático de matemática com capa azul',
'ana.beatriz@aluno.senai.br', NULL, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Livros e apostilas' LIMIT 1),
'Ainda estou com o objeto e vou levar à coordenação.'),

('Estojo rosa', 'Corredor do bloco B', '2026-09-21', NULL,
'Estojo rosa com canetas coloridas e lápis',
NULL, @cpf2, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Papelaria' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Chaveiro de coração', 'Estacionamento', '2026-05-27', NULL,
'Chaveiro de coração vermelho com argola metálica',
'rafael.mendes@aluno.senai.br', NULL, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'acessórios' LIMIT 1),
'Ainda estou com o objeto e vou levar à coordenação.'),

('Tênis esportivo', 'Quadra poliesportiva', '2026-07-08', NULL,
'Tênis esportivo preto com detalhes brancos',
NULL, @cpf3, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Calçados' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Óculos de grau', 'Cantina', '2026-11-26', NULL,
'Óculos de grau com armação preta e estojo azul',
NULL, @cpf1, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'acessórios' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Pendrive 32GB', 'Laboratório de Informática', '2026-10-02', NULL,
'Pendrive preto de 32GB com tampa',
'camila.oliveira@aluno.senai.br', NULL, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Informática' LIMIT 1),
'Ainda estou com o objeto e vou levar à coordenação.'),

('Marmita azul', 'Refeitório', '2026-11-21', NULL,
'Marmita de plástico azul com tampa e talheres',
NULL, @cpf2, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Garrafas e utensílios' LIMIT 1),
'Já entreguei o objeto na coordenação.');


-- =============================================
-- 3. NOVOS RELATÓRIOS DE PERDA
-- =============================================

INSERT INTO item
(item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto)
VALUES

('Documento estudantil', 'Biblioteca', '2026-11-26', NULL,
'Carteirinha estudantil com identificação do aluno',
'lucas.ferreira@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'Documentos' LIMIT 1), NULL),

('Fone de ouvido branco', 'Refeitório', '2026-08-03', NULL,
'Fone de ouvido branco sem fio com estojo',
'ana.beatriz@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'acessórios' LIMIT 1), NULL),

('Apostila de elétrica', 'Laboratório de Eletroeletrônica', '2026-10-12', NULL,
'Apostila de atividades práticas com capa amarela',
'rafael.mendes@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'Livros e apostilas' LIMIT 1), NULL),

('Mochila azul', 'Quadra poliesportiva', '2026-05-18', NULL,
'Mochila azul marinho com bolso frontal e zíper preto',
'camila.oliveira@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'Bolsas e mochilas' LIMIT 1), NULL),

('Calculadora financeira', 'Sala 201', '2026-11-19', NULL,
'Calculadora preta com teclas cinzas e visor digital',
'gabriela.p.silva10@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'Papelaria' LIMIT 1), NULL);


-- =============================================
-- 4. NOVOS ITENS RETIRADOS
-- =============================================

-- ITEM 1

INSERT INTO item
(item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto, nome_retirante, email_retirante, data_retirada)
VALUES
('Relógio digital', 'Vestiário', '2026-04-06',
'Relógio digital preto com pulseira de silicone',
@cpf1, 'RETIRADO',
(SELECT id_categoria FROM categoria WHERE nome = 'acessórios' LIMIT 1),
'Já entreguei o objeto na coordenação.',
'Lucas Ferreira', 'lucas.ferreira@aluno.senai.br', '2026-04-20 09:20:00');

SET @id = LAST_INSERT_ID();

INSERT INTO retirada
(id_item, nome_retirante, telefone_retirante, curso_retirante, email_retirante, cpf_retirante, data_retirada)
VALUES
(@id, 'Lucas Ferreira', '16999998888',
'Desenvolvimento de Sistemas',
'lucas.ferreira@aluno.senai.br', '51234567890', '2026-04-20 09:20:00');


-- ITEM 2

INSERT INTO item
(item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto, nome_retirante, email_retirante, data_retirada)
VALUES
('Garrafa vermelha', 'Quadra', '2026-09-09',
'Garrafa plástica vermelha com tampa preta',
@cpf2, 'RETIRADO',
(SELECT id_categoria FROM categoria WHERE nome = 'Garrafas e utensílios' LIMIT 1),
'Já entreguei o objeto na coordenação.',
'Ana Beatriz Souza', 'ana.beatriz@aluno.senai.br', '2026-09-11 15:40:00');

SET @id = LAST_INSERT_ID();

INSERT INTO retirada
(id_item, nome_retirante, telefone_retirante, curso_retirante, email_retirante, cpf_retirante, data_retirada)
VALUES
(@id, 'Ana Beatriz Souza', '16988887777',
'Eletroeletrônica',
'ana.beatriz@aluno.senai.br', '62345678901', '2026-09-11 15:40:00');


-- ITEM 3

INSERT INTO item
(item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto, nome_retirante, email_retirante, data_retirada)
VALUES
('Estojo de ferramentas', 'Laboratório de Mecânica', '2026-11-17',
'Estojo pequeno com ferramentas e chave de fenda',
@cpf3, 'RETIRADO',
(SELECT id_categoria FROM categoria WHERE nome = 'Ferramentas' LIMIT 1),
'Já entreguei o objeto na coordenação.',
'Rafael Mendes', 'rafael.mendes@aluno.senai.br', '2026-11-26 08:50:00');

SET @id = LAST_INSERT_ID();

INSERT INTO retirada
(id_item, nome_retirante, telefone_retirante, curso_retirante, email_retirante, cpf_retirante, data_retirada)
VALUES
(@id, 'Rafael Mendes', '16977776666',
'Mecânica',
'rafael.mendes@aluno.senai.br', '73456789012', '2026-11-26 08:50:00');


-- =============================================
-- 5. NOVOS ITENS ARQUIVADOS
-- =============================================

INSERT INTO item
(item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto)
VALUES

('Mochila infantil', 'Pátio', '2025-11-10',
'Mochila pequena azul com estampa de estrelas',
@cpf1, 'Arquivado',
(SELECT id_categoria FROM categoria WHERE nome = 'Bolsas e mochilas' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Livro de português', 'Biblioteca', '2026-01-20',
'Livro didático de português com capa verde',
@cpf2, 'Arquivado',
(SELECT id_categoria FROM categoria WHERE nome = 'Livros e apostilas' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Chinelo preto', 'Vestiário', '2026-02-25',
'Chinelo preto com tiras simples',
@cpf3, 'Arquivado',
(SELECT id_categoria FROM categoria WHERE nome = 'Calçados' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Carregador de notebook', 'Laboratório de Informática', '2026-04-14',
'Carregador preto para notebook com cabo de alimentação',
@cpf1, 'Arquivado',
(SELECT id_categoria FROM categoria WHERE nome = 'Informática' LIMIT 1),
'Já entreguei o objeto na coordenação.');

-- =============================================
-- 6. MAIS ITENS DISPONÍVEIS
-- =============================================

INSERT INTO item
(item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto)
VALUES

('Jaqueta jeans', 'Sala 108', '2026-06-01', NULL,
'Jaqueta jeans azul clara tamanho M com botões prateados',
NULL, @cpf2, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Outros' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Carteira marrom', 'Pátio', '2026-11-14', NULL,
'Carteira de couro marrom com zíper, sem documentos dentro',
'camila.oliveira@aluno.senai.br', NULL, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Acessórios' LIMIT 1),
'Ainda estou com o objeto e vou levar à coordenação.'),

('Calculadora científica', 'Sala 201', '2026-10-20', NULL,
'Calculadora científica preta com tampa deslizante',
NULL, @cpf1, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Papelaria' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Bola de futsal', 'Quadra poliesportiva', '2026-08-27', NULL,
'Bola de futsal branca e laranja um pouco desgastada',
NULL, @cpf3, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Material esportivo' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Marmita retangular', 'Refeitório', '2026-11-20', NULL,
'Marmita de vidro retangular com tampa vermelha',
NULL, @cpf2, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Garrafas e utensílios' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Chave de fenda', 'Laboratório de Mecânica', '2026-07-15', NULL,
'Chave de fenda com cabo amarelo e ponta média',
'rafael.mendes@aluno.senai.br', NULL, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Ferramentas' LIMIT 1),
'Ainda estou com o objeto e vou levar à coordenação.'),

('Fone de ouvido preto', 'Biblioteca', '2026-11-26', NULL,
'Fone de ouvido preto com fio e entrada P2',
NULL, @cpf1, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Informática' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Cartão de transporte', 'Entrada principal', '2026-11-05', NULL,
'Cartão de transporte escolar sem identificação visível',
'ana.beatriz@aluno.senai.br', NULL, 'DISPONIVEL',
(SELECT id_categoria FROM categoria WHERE nome = 'Documentos' LIMIT 1),
'Ainda estou com o objeto e vou levar à coordenação.');


-- =============================================
-- 7. MAIS RELATÓRIOS DE PERDA
-- =============================================

INSERT INTO item
(item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto)
VALUES

('Garrafa verde', 'Quadra poliesportiva', '2026-11-24', NULL,
'Garrafa de alumínio verde com adesivo de estrela',
'gabriela.p.silva10@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'Garrafas e utensílios' LIMIT 1), NULL),

('Casaco cinza', 'Sala 305', '2026-09-30', NULL,
'Casaco de moletom cinza com capuz e logo do SENAI',
'lucas.ferreira@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'Outros' LIMIT 1), NULL),

('Chave de armário', 'Vestiário', '2026-11-12', NULL,
'Chave pequena de armário com etiqueta numerada 42',
'camila.oliveira@aluno.senai.br', NULL, 'Perdido',
(SELECT id_categoria FROM categoria WHERE nome = 'Acessórios' LIMIT 1), NULL);


-- =============================================
-- 8. MAIS ITENS RETIRADOS
-- =============================================

-- ITEM 1

INSERT INTO item
(item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto, nome_retirante, email_retirante, data_retirada)
VALUES
('Carteira preta', 'Corredor do bloco A', '2026-07-8',
'Carteira preta de couro sintético com porta-cartões',
@cpf1, 'RETIRADO',
(SELECT id_categoria FROM categoria WHERE nome = 'Acessórios' LIMIT 1),
'Já entreguei o objeto na coordenação.',
'Camila Oliveira', 'camila.oliveira@aluno.senai.br', '2026-08-13 10:10:00');

SET @id = LAST_INSERT_ID();

INSERT INTO retirada
(id_item, nome_retirante, telefone_retirante, curso_retirante, email_retirante, cpf_retirante, data_retirada)
VALUES
(@id, 'Camila Oliveira', '16966665555',
'Logística',
'camila.oliveira@aluno.senai.br', '84567890123', '2026-08-13 10:10:00');


-- ITEM 2

INSERT INTO item
(item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto, nome_retirante, email_retirante, data_retirada)
VALUES
('Guarda-chuva azul', 'Entrada principal', '2026-10-22',
'Guarda-chuva azul marinho com cabo curvo preto',
@cpf2, 'RETIRADO',
(SELECT id_categoria FROM categoria WHERE nome = 'Outros' LIMIT 1),
'Já entreguei o objeto na coordenação.',
'Gabriela Silva', 'gabriela.p.silva10@aluno.senai.br', '2026-11-03 16:30:00');

SET @id = LAST_INSERT_ID();

INSERT INTO retirada
(id_item, nome_retirante, telefone_retirante, curso_retirante, email_retirante, cpf_retirante, data_retirada)
VALUES
(@id, 'Gabriela Silva', '16955554444',
'Administração',
'gabriela.p.silva10@aluno.senai.br', '95678901234', '2026-11-03 16:30:00');


-- =============================================
-- 9. MAIS ITENS ARQUIVADOS
-- =============================================

INSERT INTO item
(item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto)
VALUES

('Agasalho cinza', 'Pátio', '2026-01-08',
'Agasalho cinza de zíper tamanho G',
@cpf3, 'Arquivado',
(SELECT id_categoria FROM categoria WHERE nome = 'Outros' LIMIT 1),
'Já entreguei o objeto na coordenação.'),

('Calculadora simples', 'Sala 102', '2026-03-30',
'Calculadora simples preta com teclas brancas',
@cpf1, 'Arquivado',
(SELECT id_categoria FROM categoria WHERE nome = 'Papelaria' LIMIT 1),
'Já entreguei o objeto na coordenação.');

-- =============================================
-- FIM
-- =============================================