from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
from zipfile import ZipFile 
from selenium.webdriver.chrome.options import Options
import os
import pdfplumber  
import csv 

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
def substituir_abreviacoes(linha):
    legenda_abreviacoes = {
        "OD" : "Odontologica",
       "AMB" : "Ambulatorial"
    }
    linha_atualizada = [legenda_abreviacoes.get(item, item) for item in linha]
    return linha_atualizada

#Extraindo os dados da tabela
for arquivo in pdfs: #percorrer somente o anexo1
    if "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf" in arquivo: #percorrer somente o anexo1 
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
            print(f"Tabela {i+1}")  #Imprimir o numero no console de qual tabela está sendo processada
            for linha in tabela: #percorre linha por linha da tabela
                try:
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


