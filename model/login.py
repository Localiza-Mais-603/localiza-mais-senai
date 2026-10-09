from database.conexao import conectar

def verificar_login_coor(cpf, senha):
    conexao, cursor = conectar()
    
    query = "SELECT * FROM cadastro_coor WHERE cpf_coor = %s AND senha = %s"
    cursor.execute(query, (cpf, senha))
    coordenador = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return coordenador