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