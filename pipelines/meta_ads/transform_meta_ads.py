import pandas as pd
import glob
import os
import logging
from datetime import datetime

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

    latest_file = max(files, key=os.path.getctime)

    logging.info(f"Arquivo Bronze encontrado: {latest_file}")

    # Ler CSV
    df = pd.read_csv(latest_file)

    # Remove duplicados
    df = df.drop_duplicates()

    # Tratar nulos
    df = df.fillna(0)

    # Conversões
    numeric_columns = [
        "impressions",
        "clicks",
        "spend",
        "cpc",
        "ctr"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Datas
    if "date_start" in df.columns:
        df["date_start"] = pd.to_datetime(df["date_start"])

    if "date_stop" in df.columns:
        df["date_stop"] = pd.to_datetime(df["date_stop"])

    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Output
    output_path = f"data/processed/meta_ads_silver_{timestamp}.csv"

    # Salvar
    df.to_csv(output_path, index=False)

    logging.info(f"Arquivo Silver salvo: {output_path}")
    logging.info(f"Quantidade de linhas Silver: {len(df)}")

    print(df.head())

except Exception as e:

    logging.error(f"Erro na camada Silver: {str(e)}")

    print(f"Erro: {e}")