import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging

# Configuração do logging
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carregar variáveis de ambiente
load_dotenv()

ACESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')


try:
    logging.info("Iniciando extração de dados de Meta Ads")
    #endpoint para obter os dados de anúncios
    url = f"https://graph.facebook.com/v25.0/{AD_ACCOUNT_ID}/insights"


    #parâmetros para a requisição
    params = {
        "access_token": ACESS_TOKEN,
        "fields": """
            account_id,
            campaign_name,
            impressions,
            clicks,
            spend,
            ctr,
            cpc,
            reach,
            frequency,
            actions,
            action_values,
            date_start,
            date_stop
            """.replace("\n", ""),
        "date_preset": "last_30d"
    }

    #realizar a requisição
    response = requests.get(url, params=params)

    #convertendo para json
    data = response.json()

    #validação
    if 'data' not in data:
        logging.error(f"Erro ao obter dados: {data}")
        raise Exception("Erro ao obter dados de Meta Ads")
    
    #dataframe
    df = pd.DataFrame(data['data'])

    #verifica se veio vazio
    if df.empty:
        logging.warning("Nenhum dado encontrado para o período especificado")
    else:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        #cominho para salvar o arquivo
        output_path = f"data/raw/meta_ads_insights_{timestamp}.csv"
        #salvar o arquivo
        df.to_csv(output_path, index=False)
        logging.info(f"Dados de Meta Ads salvos com sucesso em {output_path}")
        logging.info(f'Total de registros extraídos: {len(df)}')
        print(f"Dados de Meta Ads salvos com sucesso em {output_path}")
except Exception as e:
    logging.error(f"Erro na extração de dados de Meta Ads: {str(e)}")
    print(f"Erro na extração de dados de Meta Ads: {str(e)}")