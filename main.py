from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
from zipfile import ZipFile 
import pdfplumber
from selenium.webdriver.chrome.options import Options
import os

arquivos_dentro_files_pdf = os.listdir("files_pdf") #Lista de arquivos dentro da pasta files

#Garantir que não há nenhum arquivo dentro da pasta de pdfs (files_pdf)
for file in arquivos_dentro_files_pdf: #percorre a pasta arquivo por arquivo.
     os.remove(os.path.join("files_pdf", file)) #deleta o arquivo encontrado em file

#Navegar até o site
download_dir = os.path.abspath("files_pdf") #caminho até a pasta file_pdf

#Passando prefs personalizadas para o chrome com intuito de não abrir a pagina de visualização de pdf.
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir, #onde vai ser salvo o arquivo pdf.
    "plugins.always_open_pdf_externally": True, #opção de baixar o arquivo direto : true.
    "download.prompt_for_download": False,  #Não abrir a janela de salvar como, salva direto sem perguntar.
    "download.directory_upgrade": True  #forçar o chrome a baixar dentro da pasta definida na variável, mesmo que nao tenha a pasta definida como padrão no chrome.
})
navegador = webdriver.Chrome(options=options)

#Url do site e baixar os anexos 1 e 2
navegador.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
elemento = navegador.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/button[2]').click()
elemento = navegador.find_element(By.XPATH, '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li[1]/a[1]').click()
elemento = navegador.find_element(By.XPATH, '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li[2]/a').click()

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

#2 - Extraindo dados da tabela ROL (anexo1)
caminho_extraçaoTabela1 = "C:\\Users\\COMPUTADOR\\OneDrive\\Documentos\\IntuitiveCare\\download.pdf1"

with pdfplumber.open(caminho_extraçaoTabela1) as pdf:
    todas_tabelas = []

    for pagina in pdf.pages:
        tabela = pagina.extract_table()
        if tabela:
            todas_tabelas.append(tabela)

    for i, tabela in enumerate(todas_tabelas): 
            print(f"Tabela {i+1}") 
    for linha in tabela: 
            print(linha)