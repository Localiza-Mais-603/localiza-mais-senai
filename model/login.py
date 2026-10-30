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
    """Verifica se o e-mail existe e salva o token no banco."""
    conexao, cursor = conectar()

    sql_check = "SELECT email FROM usuarios WHERE email = %s"
    cursor.execute(sql_check, (email,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conexao.close()
        raise ValueError("Este e-mail não está cadastrado no sistema!")


    sql = "UPDATE usuarios SET token_recuperacao = %s WHERE email = %s"
    cursor.execute(sql, (token, email))
    
    conexao.commit()
    cursor.close()
    conexao.close()

def verificar_token_valido(token):
    """Busca o usuário que possui o token enviado pelo link do e-mail."""
    if not token:
        return None
    conexao, cursor = conectar()
    
    sql = "SELECT * FROM usuarios WHERE token_recuperacao = %s"
    cursor.execute(sql, (token,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    return usuario  

def atualizar_senha_por_token(token, nova_senha):
    """Atualiza a senha do usuário e apaga o token."""
    conexao, cursor = conectar()
    
    sql = "UPDATE usuarios SET senha = %s, token_recuperacao = NULL WHERE token_recuperacao = %s"
    cursor.execute(sql, (nova_senha, token))
    
    conexao.commit()  
    cursor.close()
    conexao.close()
