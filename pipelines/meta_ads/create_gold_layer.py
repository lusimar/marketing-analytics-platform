import pandas as pd
import glob
import os
import logging
from datetime import datetime

# Configuração de logs
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:

    logging.info("Iniciando camada Gold")

    # Buscar arquivo mais recente da Silver
    files = glob.glob("data/processed/*.csv")

    latest_file = max(files, key=os.path.getctime)

    logging.info(f"Arquivo Silver encontrado: {latest_file}")

    # Ler CSV
    df = pd.read_csv(latest_file)

    # Validar colunas numéricas existentes
    numeric_columns = []

    possible_columns = [
        "impressions",
        "clicks",
        "spend",
        "cpc",
        "ctr"
    ]

    for col in possible_columns:
        if col in df.columns:
            numeric_columns.append(col)

    # Converter tipos
    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors='coerce'
        ).fillna(0)

    # Criar CPM somente se existir spend e impressions
    if "spend" in df.columns and "impressions" in df.columns:
        df["cpm"] = (
            df["spend"] / df["impressions"]
        ) * 1000

    # Criar dicionário dinâmico de agregações
    agg_dict = {}

    if "impressions" in df.columns:
        agg_dict["impressions"] = "sum"

    if "clicks" in df.columns:
        agg_dict["clicks"] = "sum"

    if "spend" in df.columns:
        agg_dict["spend"] = "sum"

    if "ctr" in df.columns:
        agg_dict["ctr"] = "mean"

    if "cpc" in df.columns:
        agg_dict["cpc"] = "mean"

    if "cpm" in df.columns:
        agg_dict["cpm"] = "mean"

    # Agrupamento Gold
    gold_df = df.groupby(
        ["account_id", "date_start", "date_stop"],
        as_index=False
    ).agg(agg_dict)

    # Arredondamentos
    for col in ["ctr", "cpc", "cpm"]:
        if col in gold_df.columns:
            gold_df[col] = gold_df[col].round(2)

    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Caminho saída
    output_path = f"data/gold/meta_ads_gold_{timestamp}.csv"

    # Salvar arquivo
    gold_df.to_csv(output_path, index=False)

    logging.info(f"Gold criada com sucesso: {output_path}")
    logging.info(f"Quantidade linhas Gold: {len(gold_df)}")

    print(gold_df.head())

except Exception as e:

    logging.error(f"Erro camada Gold: {str(e)}")

    print(f"Erro: {e}")