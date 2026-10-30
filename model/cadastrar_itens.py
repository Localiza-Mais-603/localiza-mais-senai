from database.conexao import conectar


def cadastrar_item(item, descricao, data_encontrado, status, id_categoria, local=None, foto=None, email=None, cpf_coordenador=None):
    conexao, cursor = conectar()

    sql = """
        INSERT INTO item
        (item, descricao, data_encontrado, local, status, foto, email, cpf_coordenador, id_categoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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

def listar_categorias():
    conexao, cursor = conectar()
    cursor.execute("SELECT id_categoria, nome FROM categoria ORDER BY nome ASC")
    categorias = cursor.fetchall()
    conexao.close()
    return categorias

def cadastrar_categoria(nome):
    conexao, cursor = conectar()
    cursor.execute("INSERT INTO categoria (nome) VALUES (%s)", [nome])
    conexao.commit()
    id_criado = cursor.lastrowid  
    conexao.close()
    return id_criado