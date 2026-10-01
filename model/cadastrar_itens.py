from database.conexao import conectar


def cadastrar_item(id_item, id_coord, item, descricao, data, local, status):

    conexao, cursor = conectar()

    sql = """
        INSERT INTO cadastro_item
        (id_item, id_coord, item, descricao, data, local, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        id_item,
        id_coord,
        item,
        descricao,
        data,
        local,
        status
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()