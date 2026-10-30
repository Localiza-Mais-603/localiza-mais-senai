from database.conexao import conectar

def excluir_itens(id_item):
    conexao, cursor = conectar()

    cursor.execute(
        "DELETE FROM item WHERE id_item = %s",
        (id_item,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()