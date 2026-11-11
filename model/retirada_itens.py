from database.conexao import conectar

def registrar_retirada_bd(id_item, nome_retirante, email_retirante):
    conexao, cursor = conectar()
    # Exemplo de UPDATE atualizando o status e os dados do retirante
    sql = """
        UPDATE item 
        SET status = 'RETIRADO', 
            nome_retirante = %s, 
            email_retirante = %s,
            data_retirada = NOW()
        WHERE id_item = %s
    """
    cursor.execute(sql, (nome_retirante, email_retirante, id_item))
    conexao.commit()
    cursor.close()
    conexao.close()