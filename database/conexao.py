import mysql.connector

# importando biblioteca p/ acessar .env
import os 
from dotenv import load_dotenv

load_dotenv()

def conectar():
    BD_AMBIENTE = os.getenv("BD_AMBIENTE", "local")

    if BD_AMBIENTE == "local":
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="DB_LOCALIZA"
        )

    elif BD_AMBIENTE == "online":
        conexao = mysql.connector.connect(
            host= os.getenv("BD_HOST"),
            user= os.getenv("BD_USER"),
            password= os.getenv("BD_PASSWORD"),
            database= os.getenv("DB_LOCALIZA")
        )

    cursor = conexao.cursor(dictionary=True)

    return conexao, cursor