from database.conexao import conectar

def cadastrar_item(produto, local, data, descricao):
 
    conexao, cursor = conectar()
    cursor = conexao.cursor()

  
    comando_sql = """
        INSERT INTO itens (produto, local, data, descricao)
        VALUES (?, ?, ?, ?)
    """


    cursor.execute(comando_sql, (produto, local, data, descricao))

  
    conexao.commit()
    conexao.close()