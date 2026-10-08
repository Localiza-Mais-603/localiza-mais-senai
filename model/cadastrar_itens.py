from database.conexao import conectar

def cadastrar_item(item, descricao, local, data):
    conexao, cursor = conectar()

    sql = """
        INSERT INTO cadastro_item (item, descricao, local, data, status)
        VALUES (%s, %s, %s, %s, %s)
    """

    data_valor = data if data else None

    # Passa 'Pendente' para preencher a coluna status que é obrigatória
    cursor.execute(sql, (item, descricao, local, data_valor, 'Pendente'))
    conexao.commit()

    cursor.close()
    conexao.close()