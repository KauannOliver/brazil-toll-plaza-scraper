import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_toll_data():
    url = 'https://www.emsampa.com.br/pedes.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    toll_data = []
    tables = soup.find_all('table', {'width': '90%'})

    for table in tables:
        caption = table.find('caption')
        if caption:
            span = caption.find('span', style=lambda value: value and 'font-size: 16px' in value)
            rodovia = span.get_text(strip=True).split(' - ')[0].strip() if span else 'Desconhecida'
        else:
            rodovia = 'Desconhecida'

        rows = table.find_all('tr')[2:]
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 8:
                continue
            km = cells[0].get_text(strip=True)
            localidade = cells[1].get_text(strip=True)
            eixo = cells[4].get_text(strip=True)
            desde = cells[6].get_text(strip=True)
            toll_data.append({'Rodovia': rodovia, 'KM': km, 'Localidade': localidade, 'Eixo': eixo, 'Desde': desde})

    return toll_data

def save_to_excel(data, filename):
    if not data:
        print("No data to save.")
        return
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

toll_data = scrape_toll_data()
save_to_excel(toll_data, 'PraçasES.xlsx')
