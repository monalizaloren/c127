from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

# Configuração do WebDriver
driver = webdriver.Chrome()
driver.get("https://www.amazon.com.br/")
time.sleep(5)

# Aguarda o carregamento da página (você pode ajustar o tempo de espera conforme necessário)
driver.implicitly_wait(10)

# Crie uma lista para armazenar os dados coletados
dados_livros = []

# Função para coletar informações de um livro
def coletar_info_livro(livro_element):
    titulo = livro_element.find("h2").text
    autor = livro_element.find("p", class_="autor").text
    preco = livro_element.find("span", class_="preco").text
    return {"Título": titulo, "Autor": autor, "Preço": preco}

# Loop para percorrer várias páginas de livros (se houver paginação)
while True:
    # Obtenha o código-fonte da página atual
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Encontre os elementos que representam livros na página
    livros = soup.find_all("div", class_="livro")

    # Coleta informações de cada livro e adiciona à lista de dados
    for livro_element in livros:
        info_livro = coletar_info_livro(livro_element)
        dados_livros.append(info_livro)

    # Verifique se há próxima página e clique no botão "Próxima" (ajuste o seletor conforme necessário)
    next_button = driver.find_element_by_xpath("//button[@class='proxima-pagina']")
    if next_button.get_attribute("disabled"):
        break
    else:
        next_button.click()

# Feche o navegador
driver.quit()

# Converta a lista de dicionários em um DataFrame do pandas
df = pd.DataFrame(dados_livros)

# Salve o DataFrame em um arquivo CSV
df.to_csv("livros_amazon.csv", index=False)

# Exiba os dados coletados
for livro in dados_livros:
    print("Título:", livro["Título"])
    print("Autor:", livro["Autor"])
    print("Preço:", livro["Preço"])
    print()

# Os dados também foram salvos em um arquivo CSV chamado "livros_amazon.csv" no diretório atual.
