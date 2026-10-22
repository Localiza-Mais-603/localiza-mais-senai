from database.conexao import conectar


from database.conexao import conectar

def atualizar_usuario(email_original, novo_nome, novo_email, novo_curso):
    conexao, cursor = conectar()
    sql = """
        UPDATE usuarios 
        SET nome = %s, email = %s, curso = %s 
        WHERE email = %s
    """
    
    cursor.execute(sql, (novo_nome, novo_email, novo_curso, email_original))

    conexao.commit()
    
    cursor.close()
    conexao.close()