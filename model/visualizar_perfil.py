from database.conexao import conectar

def visualizar_perfil():
    conexao, cursor = conectar()

    cursor.execute("""SELECT nome, email, curso FROM usuarios WHERE usuario""")