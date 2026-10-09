from database.conexao import conectar


def cadastrar_item( item, descricao, data_encontrado, status, id_categoria,  local:str = None, foto: str = None, email: str = None, cpf_coordenador: str = None ):

    conexao, cursor = conectar()

    sql = """
        INSERT INTO item
        ( item, descricao, data_encontrado, local, status, foto, email, cpf_coordenador, id_categoria)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        item,
        descricao,
        data_encontrado,
        local,
        status,
        foto,
        email,
        cpf_coordenador,
        id_categoria
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

# Função para os alunos cadastrarem itens
def registrar_item_perdido (item, descricao, data_encontrado, status, id_categoria,  local:str = None, foto: str = None, email: str = None, cpf_coordenador: str = None ):
    conexao, cursor = conectar()
    cursor.execute("""
             INSERT INTO item
        ( item, descricao, data_encontrado, local, status, foto, email, cpf_coordenador, id_categoria)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [item, descricao, data_encontrado, local, status, foto, email, cpf_coordenador, id_categoria])  
    conexao.commit()
    conexao.close()
    return True

