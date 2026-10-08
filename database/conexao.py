import mysql.connector


def conectar():

    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="DB_LOCALIZA"
    )

    cursor = conexao.cursor(dictionary=True)

    return conexao, cursor