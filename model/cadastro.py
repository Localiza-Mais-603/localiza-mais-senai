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

