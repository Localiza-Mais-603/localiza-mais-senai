from database.conexao import conectar

def verificar_login_coor(cpf, senha):
    conexao, cursor = conectar()
    
    query = "SELECT * FROM coordenador WHERE cpf = %s AND senha = %s"
    cursor.execute(query, (cpf, senha))
    coordenador = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return coordenador

def verificar_login_usuario(email, senha):
    conexao, cursor = conectar()
    
    sql = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
    cursor.execute(sql, (email, senha))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    return usuario


def salvar_token_recuperacao(email, token):
    """Salva o token gerado no usuário correspondente no banco."""
    conexao, cursor = conectar()

    sql = "UPDATE usuarios SET token_recuperacao = %s WHERE email = %s"
    cursor.execute(sql, (token, email))
    
    conexao.commit()
    cursor.close()
    conexao.close()

def verificar_token_valido(token):
    """Busca o usuário que possui o token enviado pelo link do e-mail."""
    conexao, cursor = conectar()
    
    sql = "SELECT * FROM usuarios WHERE token_recuperacao = %s"
    cursor.execute(sql, (token,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    return usuario  

def atualizar_senha_por_token(token, nova_senha):
    """Atualiza a senha do usuário e apaga o token para ele não ser usado de novo."""
    conexao, cursor = conectar()
    
    sql = "UPDATE usuarios SET senha = %s, token_recuperacao = NULL WHERE token_recuperacao = %s"
    cursor.execute(sql, (nova_senha, token))
    
    conexao.commit()  
    cursor.close()
    conexao.close()