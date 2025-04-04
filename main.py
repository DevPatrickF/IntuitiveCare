from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
from zipfile import ZipFile 
from selenium.webdriver.chrome.options import Options
import os
import pdfplumber  
import csv 
import sys
import database.connection as db_connection


sys.stdout.reconfigure(encoding='utf-8') #garantir que o terminal consiga exibir os caracteres especiais.

arquivos_dentro_files_pdf = os.listdir("files_pdf") #Lista de arquivos dentro da pasta files

#Garantir que não há nenhum arquivo dentro da pasta de pdfs (files_pdf)
for file in arquivos_dentro_files_pdf: #percorre a pasta arquivo por arquivo.
     os.remove(os.path.join("files_pdf", file)) #deleta o arquivo encontrado em file
 
download_dir = os.path.abspath("files_pdf") #caminho até a pasta file_pdf

#Passando prefs personalizadas para o chrome com intuito de não abrir a pagina de visualização de pdf.
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir, #onde vai ser salvo o arquivo pdf.
    "plugins.always_open_pdf_externally": True, #opção de baixar o arquivo direto : true.
    "download.prompt_for_download": False,  #Não abrir a janela de salvar como, salva direto sem perguntar.
    "download.directory_upgrade": True  #forçar o chrome a baixar dentro da pasta definida na variável, mesmo que nao tenha a pasta definida como padrão no chrome.
})
#navegar ate o site
navegador = webdriver.Chrome(options=options)

#Url do site e baixar os anexos 1 e 2
navegador.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
elemento = navegador.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/button[2]').click()
elemento = navegador.find_element(By.XPATH, '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li[1]/a[1]').click()
elemento = navegador.find_element(By.XPATH, '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li[2]/a').click()

print("Downloads dos anexos 1 e 2 feito com sucesso!")

#Outra opçao de download sem precisar usar o selenium (utilizando urllib.requests.urlretrieve)

# url_pdf1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
# url_pdf2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"

# caminho_pdf1 ="files_pdf/anexo_1.pdf"
# caminho_pdf2 = "files_pdf/anexo_2.pdf"


# urllib.request.urlretrieve(url_pdf1, caminho_pdf1)
# print('PDF do anexo1 baixado com sucesso!')

# urllib.request.urlretrieve(url_pdf2, caminho_pdf2)
# print('PDF do anexo2 baixado com sucesso!')

#Espera os downloads concluirem 100% dos dois arquivos
while True:
    arquivos = os.listdir("files_pdf")
    pdfs = []

    for arquivo in arquivos:
        if arquivo.endswith(".pdf"):
            pdfs.append(arquivo)

    if len(pdfs) == 2:
        break

    time.sleep(0.7)

#Compactar os anexos 1 e 2 em um unico arquivo zip
with ZipFile("anexos_compactados.zip", "w") as zip:
    for file in arquivos_dentro_files_pdf: #percorre a pasta file com os arquivos pdfs
        if file.endswith(".pdf"): #se o arquivo terminar com pdf (endswith)
            zip.write(os.path.join("files_pdf", file), arcname=file) #aqui ele cria o zip, sem subpasta.

print("Arquivos compactados com sucesso!")

#Funcao para substituir as abreviacoes 
def substituir_abreviacoes(texto):
    legenda_abreviacoes = {
        "OD" : "Seg. Odontologica",
       "AMB" : "Seg. Ambulatorial"
    }

    if isinstance(texto, str):  # Garante que só mexe em strings
        texto = texto.strip() #remove espaços ao redor
        return legenda_abreviacoes.get(texto, texto) #substitui apenas se a sigla for exatamente como escrita
    return texto

#Extraindo os dados da tabela
for arquivo in pdfs: #percorrer somente o anexo1
    if "Anexo_I_" in arquivo: #percorrer somente o anexo1 
        arquivo_anexo1 = os.path.join(download_dir, arquivo) 
        break #intorromper assim o anexo1 for encontrado

with pdfplumber.open(arquivo_anexo1) as pdf: #Abrir o arquivo e extrair a tabela
    todas_tabelas = [] #Lista para armazenar as tabelas extraidas

    for pagina in pdf.pages: #percorrer cada pagina do pdf
        tabela = pagina.extract_table() #extrair as tabelas da pagina
        if tabela:
            todas_tabelas.append(tabela) #adicionando tabela extraida a lista 



    #Abrir o arquivo para a leitura da tabela
    with open('tabelas_extraidas_anexo1.csv', mode='w', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv)
      
        for i, tabela in enumerate(todas_tabelas): # usei enumerate para obter os valores de cada item
            print(f"Linha {i+1}")  #Imprimir o numero no console de qual tabela está sendo processada
            for linha in tabela: #percorre linha por linha da tabela
            
                try: #inicia um bloco de codigo que pode gerar erros
                    linha[3] = "Seg. Odontológica" if linha[3] != "" else ""
                    linha[4] = "Seg. Ambulatorial" if linha[3] != "" else ""
                    # Imprimir cada célula da linha, lidando com erros de codificação
                    linha_impressa = [item.encode('utf-8', errors='ignore').decode('utf-8') if isinstance(item, str) else item for item in linha]
                    print(linha_impressa)  # Imprimir a linha, corrigida para codificação UTF-8
                except UnicodeEncodeError:
                    print("Erro ao tentar imprimir linha com caracteres especiais")
                    linha_impressa = [item.encode('utf-8', errors='ignore').decode('utf-8') if isinstance(item, str) else item for item in linha]
                    print(linha_impressa)
                writer.writerow(linha)  # Escrever a linha no arquivo CSV
            print("Dados extraídos para pasta CSV com sucesso!")

    
            

#Compactando o csv em um arquivo zip
csv_filename = 'tabelas_extraidas_anexo1.csv' #caminho do arquivo a ser compactado em zip
zip_filename = 'Teste_{tabela_em_zip}.zip' #Nome do novo arquivo zip

#Compactar em zip
with ZipFile(zip_filename, "w") as zip:
    zip.write(csv_filename, arcname=os.path.basename(csv_filename)) #adicionando o arquivo csv em arquivo zip
    print("Arquivo csv compactado em zip com sucesso!")
    


def criar_tabela_cadop(conexao):
    try:
        cursor_create_table = conexao.cursor()
        
        cursor_create_table.execute("""
            CREATE TABLE IF NOT EXISTS ans (
            registro_ans INT PRIMARY KEY,
            cnpj VARCHAR(18) NOT NULL,
            razao_social VARCHAR(255) NOT NULL,
            nome_fantasia VARCHAR(255),
            modalidade VARCHAR(100),
            logradouro VARCHAR(255),
            numero VARCHAR(20),
            complemento VARCHAR(255),
            bairro VARCHAR(100),
            cidade VARCHAR(100),
            uf CHAR(2),
            cep VARCHAR(10),
            ddd CHAR(2),
            telefone VARCHAR(20),
            fax VARCHAR(20),
            endereco_eletronico VARCHAR(255),
            representante VARCHAR(255),
            cargo_representante VARCHAR(255),
            regiao_comercializacao VARCHAR(255),
            data_registro_ans DATE
        );
            )
        """)
        print("Tabela criada com sucesso!")
        
        cursor_create_table.close()


    except Exception as e:
        print(f"Erro ao criar tabela ou inserir dados: {e}")


def insert_relatorio_cadop(conexao):
        cursor = conexao.cursor()
        # Apagar os dados da tabela antes de inserir novos
        cursor.execute("DELETE FROM ans")
        conexao.commit()  # Confirmar a exclusão dos dados
        print("Dados antigos apagados com sucesso!")

        # Inserir dados
        query_inserir = """
            INSERT INTO ans (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_comercializacao, data_registro_ans)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with open('Relatorio_cadop.csv', mode='r', encoding='utf-8') as file_csv:
            reader = csv.reader(file_csv, delimiter=";", quotechar='"')
            next(reader)  # Pular o cabeçalho
            valores = [tuple(row) for row in reader]  # Certifique-se de que os dados correspondem às colunas da tabela
        cursor.executemany(query_inserir, valores)
        
        conexao.commit()
        print(f"{cursor.rowcount} registros inseridos com sucesso!")


def criar_tabela_demonstrativo_contabil(conexao):
    cursor_create_table = conexao.cursor()

    cursor_create_table.execute("""
    CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    DATA DATE,
    REG_ANS INT,
    CD_CONTA_CONTABIL VARCHAR(50),
    DESCRICAO VARCHAR(255),
    VL_SALDO_INICIAL DECIMAL(15, 2),
    VL_SALDO_FINAL DECIMAL(15, 2)
        );
    """
    )

    cursor_create_table.close()

    print("Tabela de demostrações contábeis criada com sucesso!")


def insert_demonstracoes_contabeis(conexao):
    
    cursor = conexao.cursor()
    cursor.execute("TRUNCATE TABLE demonstracoes_contabeis")
    print("Dados antigos apagados com sucesso!")

    query_inserir = """
        INSERT INTO demonstracoes_contabeis (DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    for demonstrativo in os.listdir("demonstracoes_contabeis"):
        
        full_path = os.path.join("demonstracoes_contabeis", demonstrativo)

        with open(full_path, mode='r', encoding='utf-8') as file_csv:
            reader = csv.reader(file_csv, delimiter=";", quotechar='"')
            next(reader)  # Pular o cabeçalho

            batch_size = 50000

            valores = []  # Certifique-se de que os dados correspondem às colunas da tabela

            for row in reader:
                valores.append(tuple(row if row else None for row in row))  # Substituir "" por None
                if len(valores) >= batch_size:
                    cursor.executemany(query_inserir, valores)
                    conexao.commit()
                    valores = []
            if valores:
                cursor.executemany(query_inserir, valores)
                conexao.commit()

        
        print("Todos os dados foram inseridos com sucesso.")


def exibir_top10_despesas_3_meses(conexao):
    query = """
        SELECT 
            dc.reg_ans,
            a.nome_fantasia,
            SUM(CAST(REPLACE(dc.vl_saldo_final, ',', '.') AS DECIMAL(18,2))) AS total_despesa
        FROM demonstracoes_contabeis dc
        JOIN ans a ON a.registro_ans = dc.reg_ans
        WHERE dc.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
            AND dc.data BETWEEN '2024-10-01' AND '2024-12-31'
        GROUP BY dc.reg_ans, a.nome_fantasia
        ORDER BY total_despesa DESC
        LIMIT 10;
        """
    try:
        cursor = conexao.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        print("Top 10 Despesas:")
        for reg_ans, nome_fantasia, total_despesa in resultados:
            print(f"Registro ANS: {reg_ans}, Nome Fantasia: {nome_fantasia}, Total Despesa: {total_despesa}")
        cursor.close()
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def exibir_top10_despesas_1_ano(conexao):
    query = """
        SELECT 
            dc.reg_ans,
            a.nome_fantasia,
            SUM(CAST(REPLACE(dc.vl_saldo_final, ',', '.') AS DECIMAL(18,2))) AS total_despesa
        FROM demonstracoes_contabeis dc
        JOIN ans a ON a.registro_ans = dc.reg_ans
        WHERE dc.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
            AND dc.data BETWEEN '2024-01-01' AND '2024-12-31'
        GROUP BY dc.reg_ans, a.nome_fantasia
        ORDER BY total_despesa DESC
        LIMIT 10;
        """
    try:
        cursor = conexao.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        print("Top 10 Despesas:")
        for reg_ans, nome_fantasia, total_despesa in resultados:
            print(f"Registro ANS: {reg_ans}, Nome Fantasia: {nome_fantasia}, Total Despesa: {total_despesa}")
        cursor.close()
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


# Exemplo de uso
conexao = db_connection.conectar_mysql()
if conexao:
    criar_tabela_cadop(db_connection.conectar_mysql())
    insert_relatorio_cadop(db_connection.conectar_mysql())
    criar_tabela_demonstrativo_contabil(db_connection.conectar_mysql())
    insert_demonstracoes_contabeis(db_connection.conectar_mysql())
    exibir_top10_despesas_3_meses(db_connection.conectar_mysql())
    exibir_top10_despesas_1_ano(db_connection.conectar_mysql())
    print("Conexão com o MySQL foi encerrada.")


    