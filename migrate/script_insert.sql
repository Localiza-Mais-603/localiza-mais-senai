-- INSERÇÃO DE CATEGORIAS
INSERT INTO db_localiza.categoria (nome) VALUES ('acessórios');
INSERT INTO db_localiza.categoria (nome) VALUES ('EPI');


-- INSERÇÃO DE COORDENADOR
INSERT INTO db_localiza.coordenador (cpf, nome, email, senha) 
VALUES ('23465478921', 'Godofredo Alex', 'godoalex@gmail.com', 'godo12');


-- INSERÇÃO DE USUARIOS
INSERT INTO db_localiza.usuarios (email, cpf, nome, curso, senha) 
VALUES ('felizsnts@gmail.com', '12367898765', 'felizberta santos', 'desenvolvimento de sistemas', 'feliz09');
INSERT INTO db_localiza.usuarios (email, cpf, nome, curso, senha) 
VALUES ('gabriela.p.silva10@aluno.senai.br', '48693273841', 'Gabriela Peratello', 'Desenvolvimento de Sistemas', '1');


-- INSERÇÃO DE ITENS (Corrigido para incluir o destino_objeto correspondente ou NULL)
INSERT INTO db_localiza.item (item, local, data_encontrado, descricao, cpf_coordenador, status, id_categoria, destino_objeto) 
VALUES ('óculos', 'biblioteca', '2026-10-09', 'óculos rosa', '23465478921', 'perdido', 1, NULL);
INSERT INTO db_localiza.item (item, local, data_encontrado, descricao, email, status, id_categoria, destino_objeto) 
VALUES ('garrafinha', 'refeitório', '2026-10-09', 'Garrafinha azul', 'felizsnts@gmail.com', 'perdido', 1, 'Ainda estou com o objeto e vou levar à coordenação.');

-- 1. NOVAS CATEGORIAS (caso ainda não existam)
INSERT INTO categoria (nome) VALUES ('eletrônicos');
INSERT INTO categoria (nome) VALUES ('vestuário');

-- 2. NOVOS COORDENADORES (Setor de Apoio)
INSERT INTO coordenador (cpf, nome, email, senha) VALUES
('34567890122', 'Marina Almeida', 'marina.apoio@escola.edu.br', 'coord123'),
('45678901233', 'Carlos Eduardo Rocha', 'carlos.apoio@escola.edu.br', 'coord456');

-- 3. NOVOS USUÁRIOS (Alunos)
INSERT INTO usuarios (email, cpf, nome, curso, senha) VALUES
('lucas.ferreira@aluno.senai.br', '51234567890', 'Lucas Ferreira', 'Desenvolvimento de Sistemas', 'aluno123'),
('ana.beatriz@aluno.senai.br', '62345678901', 'Ana Beatriz Souza', 'Eletroeletrônica', 'aluno123'),
('rafael.mendes@aluno.senai.br', '73456789012', 'Rafael Mendes', 'Mecânica', 'aluno123'),
('camila.oliveira@aluno.senai.br', '84567890123', 'Camila Oliveira', 'Administração', 'aluno123');

-- 4. ITENS DISPONÍVEIS (aparecem na tela principal /visualizar-itens)
-- Cadastrados pela coordenação (status = 'DISPONIVEL', cpf_coordenador preenchido)
INSERT INTO item (item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto) VALUES
('Fone Bluetooth', 'Biblioteca', '2026-11-10', NULL, 'Fone intra-auricular preto com estojo de carregamento', NULL, '23465478921', 'DISPONIVEL', 3, 'Já entreguei o objeto na coordenação.'),
('Óculos de proteção', 'Laboratório de Mecânica', '2026-11-12', NULL, 'Óculos de segurança lente incolor com haste lateral', NULL, '34567890122', 'DISPONIVEL', 2, 'Já entreguei o objeto na coordenação.'),
('Moleton cinza', 'Quadra Poliesportiva', '2026-11-15', NULL, 'Blusa de moletom cinza tamanho M, sem estampa', NULL, '45678901233', 'DISPONIVEL', 4, 'Já entreguei o objeto na coordenação.');

-- Encontrados por alunos e publicados (status = 'DISPONIVEL', email do aluno + destino_objeto)
INSERT INTO item (item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto) VALUES
('Chaveiro com chave', 'Bloco A - Sala 102', '2026-11-18', NULL, 'Chaveiro emborrachado verde com uma chave simples', 'lucas.ferreira@aluno.senai.br', NULL, 'DISPONIVEL', 1, 'Ainda estou com o objeto e vou levar à coordenação.'),
('Carregador USB-C', 'Cantina', '2026-11-20', NULL, 'Cabo e fonte branca padrão USB-C', 'ana.beatriz@aluno.senai.br', NULL, 'DISPONIVEL', 3, 'Deixado no local (ex: em cima da mesa do professor).');

-- 5. RELATÓRIOS DE PERDA ("Perdi algo" -> status = 'Perdido', aparecem em /relatorios-perda e no histórico do aluno)
INSERT INTO item (item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto) VALUES
('Carteira marrom', 'Pátio', '2026-11-19', NULL, 'Carteira de couro marrom com documentos e cartão estudantil', 'rafael.mendes@aluno.senai.br', NULL, 'Perdido', 1, NULL),
('Calculadora científica', 'Sala 205', '2026-11-21', NULL, 'Calculadora científica preta com tampa deslizante', 'camila.oliveira@aluno.senai.br', NULL, 'Perdido', 3, NULL),
('Avental técnico', 'Laboratório de Química', '2026-11-22', NULL, 'Avental branco manga longa com nome bordado', 'gabriela.p.silva10@aluno.senai.br', NULL, 'Perdido', 2, NULL);

-- 6. ITEM ARQUIVADO (status = 'Arquivado', aparece em /itens-arquivados)
INSERT INTO item (item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto) VALUES
('Estojo escolar', 'Secretaria', '2026-04-10', NULL, 'Estojo azul marinho com zíper duplo', NULL, '23465478921', 'Arquivado', 1, 'Já entreguei o objeto na coordenação.');

-- 7. ITEM RETIRADO + REGISTRO NA TABELA retirada (aparece em /itens_retirados)
INSERT INTO item (item, local, data_encontrado, foto, descricao, email, cpf_coordenador, status, id_categoria, destino_objeto, nome_retirante, email_retirante, data_retirada) VALUES
('Guarda-chuva preto', 'Portaria', '2026-11-05', NULL, 'Guarda-chuva dobrável preto com cabo curvo', NULL, '34567890122', 'RETIRADO', 1, 'Já entreguei o objeto na coordenação.', 'Lucas Ferreira', 'lucas.ferreira@aluno.senai.br', '2026-11-06 14:30:00');

-- Vincula a retirada ao id_item recém-inserido
SET @id_item_retirado = LAST_INSERT_ID();

INSERT INTO retirada (id_item, nome_retirante, telefone_retirante, curso_retirante, email_retirante, cpf_retirante) VALUES
(@id_item_retirado, 'Lucas Ferreira', '16999998888', 'Desenvolvimento de Sistemas', 'lucas.ferreira@aluno.senai.br', '51234567890');