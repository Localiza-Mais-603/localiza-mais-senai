from database.conexao import conectar

def atualizar_item_no_banco(id_item, item, descricao, local, data):
    conexao, cursor = conectar()
    
    sql = """UPDATE item SET item = %s, descricao = %s, local = %s, data_encontrado = %s WHERE id_item = %s"""
    cursor.execute(sql, (item, descricao, local, data, id_item))

    conexao.commit()
    cursor.close()
    conexao.close()

def atualizar_status_item(id_item, novo_status):
    conexao, cursor = conectar()

    sql = "UPDATE item SET status = %s WHERE id_item = %s"
    cursor.execute(sql, (novo_status, id_item))

    conexao.commit()
    cursor.close()
    conexao.close()