import json
import mysql.connector
from mysql.connector import Error

def conectar_mysql():
    try:
        conexao = mysql.connector.connect(
            host='database-ans-dados.cyf00sugy40z.us-east-1.rds.amazonaws.com',
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


def executar_consulta(conexao, operadora):
    try:
        consulta = f"select * from ans where razao_social like {operadora}"
        cursor = conexao.cursor()
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]

        # Transforma tuplas em dicionários + trata campo de data
        resultado_formatado = []
        for row in resultados:
            registro = dict(zip(colunas, row))
            if 'data_registro_ans' in registro:
                registro['data_registro_ans'] = str(registro['data_registro_ans'])
            resultado_formatado.append(registro)

        return resultado_formatado
    except Error as e:
        print(f"Erro ao executar a consulta: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def lambda_handler(event, context):
    print(event)
    conexao = conectar_mysql()
    if conexao:
        resultados = executar_consulta(conexao, "'%"+event['operadora']+"%'")
        if resultados:
            print("Resultados da consulta:")
            for resultado in resultados:
                print(resultado)
        else:
            print("Nenhum resultado encontrado.")
        conexao.close()
    return {
        'statusCode': 200,
        'body': resultados
    }
