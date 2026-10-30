from database.conexao import conectar

def listar_todos():
    conexao, cursor = conectar()
    
    query = """
        SELECT item.*, usuarios.nome AS nome_usuario 
        FROM item 
        LEFT JOIN usuarios ON item.email = usuarios.email
    """
    cursor.execute(query)
    itens = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    return itens