import mysql.connector
from mysql.connector import Error

def conectar_mysql():
    try:
        conexao = mysql.connector.connect(
            host='database-ans-dados.cyf00sugy40z.us-east-1.rds.amazonaws.com',  # Substitua pelo endereço do seu servidor MySQL
            user='admin',
            password='02041996',
            database= 'ans_dados'
        )
        if conexao.is_connected():
            print("Conexão com o MySQL foi estabelecida com sucesso!")
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None