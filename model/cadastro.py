from database.conexao import conectar

def cadastrar_usuario(nome, cpf, email, curso, senha):
    conexao, cursor = conectar()
    cursor = conexao.cursor()
    

    sql = """ INSERT INTO 
    cadastro_usuario (cpf_usuario, nome, curso, email, senha) 
    VALUES (%s, %s, %s, %s, %s) """ 
    valores = (cpf, nome, curso, email, senha) 
    cursor.execute(sql, valores) 
    conexao.commit() 
    cursor.close() 
    conexao.close()





def cadastrar_coor(nome, cpf, email, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO cadastro_coor (cpf_coor, nome, email, senha)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (cpf, nome, email, senha))
    conexao.commit()

    cursor.close()
    conexao.close()
