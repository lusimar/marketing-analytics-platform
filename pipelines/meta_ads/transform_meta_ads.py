import pandas as pd
import glob
import os
import logging
from datetime import datetime
import ast

# Config logs
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:

    logging.info("Iniciando transformação Silver")

    # Busca arquivo mais recente da Bronze
    files = glob.glob("data/raw/*.csv")
    last_file = max(files, key=os.path.getmtime)
     
    logging.info(f"Arquivo encontrado: {last_file}")

    #lendo CSV
    df = pd.read_csv(last_file)

    #mostrar todas as colunas
    if "actions" in df.columns:
        
        df["actions"] = df["actions"].fillna("[]")

        #Convertendo string para lista
        df["actions"] = df["actions"].apply(ast.literal_eval)
        print(df["actions"].head())

except Exception as e:

    logging.error(f"Erro na camada Silver: {str(e)}")

    print(f"Erro: {e}")