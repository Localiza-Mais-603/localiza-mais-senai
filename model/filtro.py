from database.conexao import conectar  

def buscar_itens_filtrados(categorias_ids, apenas_disponiveis=None):
    res = conectar()
    
    # Se conectar() retornar uma tupla (ex: conexao, cursor ou conexao, erro), pega apenas o primeiro item
    if isinstance(res, tuple):
        conexao = res[0]
    else:
        conexao = res

    # Se mesmo assim der erro ou vier None, interrompe antes de chamar cursor
    if not conexao:
        return []

    try:
        # Tenta criar cursor com dictionary=True (ou fallback para cursor padrão)
        try:
            cursor = conexao.cursor(dictionary=True)
        except (TypeError, AttributeError):
            cursor = conexao.cursor()

        # Monta a query dinamicamente apenas se houver categorias selecionadas
        if categorias_ids:
            placeholders = ', '.join(['%s'] * len(categorias_ids))
            query = f"SELECT * FROM item WHERE id_categoria IN ({placeholders})"
            params = list(categorias_ids)
            
            if apenas_disponiveis:
                query += " AND status = 'Disponível'"
        else:
            query = "SELECT * FROM item"
            params = []
            if apenas_disponiveis:
                query += " WHERE status = 'Disponível'"

        cursor.execute(query, params)
        itens = cursor.fetchall()
        return itens

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexao:
            conexao.close()