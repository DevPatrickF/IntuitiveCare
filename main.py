from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
from zipfile import ZipFile 
import pdfplumber


#Navegar até o site
navegador = webdriver.Chrome()


#Url do site e baixar os anexos 1 e 2
navegador.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
elemento = navegador.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/button[2]').click()
elemento = navegador.find_element(By.XPATH, '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li[1]/a[1]').click()
elemento = navegador.find_element(By.XPATH, '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li[2]/a').click()


url_pdf1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
url_pdf2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"

caminho_pdf1 ="C:\\Users\\COMPUTADOR\\OneDrive\\Documentos\\IntuitiveCare\\download.pdf1"
caminho_pdf2 = "C:\\Users\\COMPUTADOR\\OneDrive\\Documentos\\IntuitiveCare\\download.pdf2"


urllib.request.urlretrieve(url_pdf1, caminho_pdf1)
print('PDF do anexo1 baixado com sucesso!')

urllib.request.urlretrieve(url_pdf2, caminho_pdf2)
print('PDF do anexo2 baixado com sucesso!')


#Compactar os anexos 1 e 2 em um unico arquivo zip

with ZipFile("C:\\Users\\COMPUTADOR\\OneDrive\\Documentos\\IntuitiveCare\\anexos_compactados.zip", "w") as zip:
    zip.write(caminho_pdf1, "download.pdf1")
    zip.write(caminho_pdf2, "download.pdf2")

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