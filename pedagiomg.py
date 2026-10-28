import requests
from bs4 import BeautifulSoup
import pandas as pd

### função para fazer a raspagem de dados do site ###
def raspar_dados_pedagios():
    url = 'https://www.emsampa.com.br/pedmg.htm'  ### URL da página a ser raspada ###
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    ### realiza o request à URL ###
    resposta = requests.get(url, headers=headers)
    print(f"codigo do status: {resposta.status_code}")
    
    ### verifica se o request foi bem-sucedido ###
    if resposta.status_code != 200:
        print(f"deu um erro doido aqui: {resposta.status_code}")
        return []  ### retorna uma lista vazia em caso de erro ###

    ### parseia o conteúdo HTML da página ###
    sopa = BeautifulSoup(resposta.content, 'html.parser')

    dados_pedagio = []
    tabelas = sopa.find_all('table', {'width': '90%'})  ### encontra todas as tabelas de pedágio na página ###

    ### percorre cada tabela de pedágios ###
    for tabela in tabelas:
        legenda = tabela.find('caption')  ### captura a legenda da tabela ###
        
        ### se houver legenda, captura o nome da rodovia ###
        if legenda:
            span = legenda.find('span', style=lambda value: value and 'font-size: 16px' in value)
            rodovia = span.get_text(strip=True).split(' - ')[0].strip() if span else 'Desconhecida'
        else:
            rodovia = 'Desconhecida'

        linhas = tabela.find_all('tr')[2:]  ### ignora as duas primeiras linhas (cabeçalho) e percorre as linhas de dados ###
        
        ### percorre cada linha da tabela ###
        for linha in linhas:
            colunas = linha.find_all('td')
            
            ### verifica se há pelo menos 8 colunas na linha ###
            if len(colunas) < 8:
                continue  ### ignora a linha se não tiver todas as colunas necessárias ###
            
            km = colunas[0].get_text(strip=True)  ### captura o valor do KM ###
            localidade = colunas[1].get_text(strip=True)  ### captura a localidade ###
            eixo = colunas[4].get_text(strip=True)  ### captura o número de eixos ###
            desde = colunas[6].get_text(strip=True)  ### captura o valor da tarifa desde ###
            
            ### adiciona os dados extraídos à lista ###
            dados_pedagio.append({'Rodovia': rodovia, 'KM': km, 'Localidade': localidade, 'Eixo': eixo, 'Desde': desde})

    return dados_pedagio  ### retorna a lista de dados de pedágio ###

### função para salvar os dados em um arquivo Excel ###
def salvar_para_excel(dados, nome_arquivo):
    if not dados:
        print("não tem dados.")
        return
    df = pd.DataFrame(dados)  ### converte os dados para DataFrame do pandas ###
    df.to_excel(nome_arquivo, index=False)  ### salva o DataFrame no arquivo Excel ###

### executa a raspagem de dados ###
dados_pedagio = raspar_dados_pedagios()

### salva os dados raspados no arquivo Excel ###
salvar_para_excel(dados_pedagio, 'PracasMG.xlsx')
