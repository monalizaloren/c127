import requests
from bs4 import BeautifulSoup
import csv

# URL da página da BBC que queremos extrair
url = "https://www.bbc.com"

# Faz uma solicitação GET para obter o conteúdo da página
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida (status code 200)
if response.status_code == 200:
    # Analisa o conteúdo da página com o Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontra os elementos que contêm as notícias
    news_elements = soup.find_all('div', class_='media__content')
    
    # Abrir um arquivo CSV para escrita
    with open('bbc_news.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Criar um objeto de escrita CSV
        csv_writer = csv.writer(csvfile)
        
        # Escrever o cabeçalho do CSV
        csv_writer.writerow(['Título', 'Link'])
        
        # Itera sobre os elementos das notícias e extrai os títulos e links
        for news_element in news_elements:
            headline = news_element.find('h3', class_='media__title')
            link = news_element.find('a', class_='media__link')
            
            if headline and link:
                title = headline.get_text(strip=True)
                news_link = link['href']
                
                # Escrever os dados no arquivo CSV
                csv_writer.writerow([title, news_link])
    
    print("Dados exportados para bbc_news.csv.")
else:
    print("Não foi possível acessar a página.")
