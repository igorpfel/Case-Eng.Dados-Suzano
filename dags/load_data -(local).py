
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime


def convert_to_float(x):
    try:
        return float(str(x).replace('.', '').replace(',', '.'))
    except:
        return None


engine = create_engine("postgresql://postgres:1234@db:5432/investing")

# 1. USD/CNY
df_usd = pd.read_csv("/opt/airflow/fonte/usd_cny_data.csv")

df_usd = df_usd.rename(columns={
    "Data": "date",
    "Último": "close",
    "Abertura": "open",
    "Máxima": "high",
    "Mínima": "low",
    "Vol.": "volume"
})

df_usd["date"] = pd.to_datetime(df_usd["date"], format="%d.%m.%Y")
for col in ["close", "open", "high", "low"]:
    df_usd[col] = df_usd[col].apply(convert_to_float)


with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS usd_cny_exchange (
        date DATE PRIMARY KEY,
        close FLOAT,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        volume TEXT
    )
    """))


df_usd.to_sql("usd_cny_exchange", engine, if_exists="append", index=False, method="multi")

# 2. Chinese PMI
df_pmi = pd.read_csv("/opt/airflow/fonte/chinese_pmi_data.csv")

df_pmi = df_pmi.rename(columns={
    "data": "date",
    "Atual": "actual_state",
    "Projeção": "forecast",
    "Anterior": "close"
})

df_pmi["date"] = pd.to_datetime(df_pmi["date"], format="%d.%m.%Y", errors="coerce")
for col in ["actual_state", "forecast", "close"]:
    df_pmi[col] = df_pmi[col].apply(convert_to_float)

with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS chinese_pmi_index (
        date DATE PRIMARY KEY,
        actual_state FLOAT,
        forecast FLOAT,
        close FLOAT
    )
    """))

df_pmi.to_sql("chinese_pmi_index", engine, if_exists="append", index=False, method="multi")
print("Dados inseridos com sucesso!")
