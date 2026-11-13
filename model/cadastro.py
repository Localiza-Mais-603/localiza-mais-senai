from database.conexao import conectar

def cadastrar_usuario(cpf, nome, curso, email, senha):
    conexao, cursor = conectar()

    sql = """ INSERT INTO 
    usuarios (cpf, nome, curso, email, senha) 
    VALUES (%s, %s, %s, %s, %s) """ 
    valores = (cpf, nome, curso, email, senha) 
    cursor.execute(sql, valores) 
    conexao.commit() 
    cursor.close() 
    conexao.close()


def cadastrar_coor(nome, cpf, email, senha):
    conexao, cursor = conectar()

    sql = """
        INSERT INTO coordenador (cpf, nome, email, senha)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (cpf, nome, email, senha))
    conexao.commit()

    cursor.close()
    conexao.close()

def existe_coordenador():
    conexao, cursor = conectar()
    cursor.execute("SELECT COUNT(*) FROM coordenador")
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    total = resultado[0] if isinstance(resultado, tuple) else list(resultado.values())[0]
    return total > 0