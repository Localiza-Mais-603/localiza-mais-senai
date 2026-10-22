from database.conexao import conectar  

def buscar_usuario_por_email(email):
    conexao, cursor = conectar()
    cursor = conexao.cursor(dictionary=True) 
    
    query = "SELECT * FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return usuario