from database.conexao import conectar

def listar_todos():
        conexao, cursor = conectar()
        cursor.execute("""
            SELECT id_item, item, descricao, local, data_encontrado, foto, status, email, id_categoria
            FROM item
            ORDER BY id_item DESC
        """)
        resultado = cursor.fetchall()
        conexao.close()
        return resultado