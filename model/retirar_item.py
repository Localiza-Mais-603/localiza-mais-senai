from database.conexao import conectar


def retirar_item(id_item, nome, telefone, curso, email, cpf):
    conexao, cursor = conectar()
    sql_retirada = """
        INSERT INTO retirada(id_item, nome_retirante, telefone_retirante, curso_retirante, email_retirante, cpf_retirante)
        VALUES(%s, %s, %s, %s, %s, %s)

    """

    cursor.execute(sql_retirada, (id_item, nome, telefone, curso, email, cpf))