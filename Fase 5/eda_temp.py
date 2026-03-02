import pandas as pd
import numpy as np

# Carregar o dataset
df = pd.read_csv('data/crop_yield.csv')

# Exibir informações básicas
print("=== Informações do Dataset ===")
print(df.info())
print("\n=== Primeiras 5 linhas ===")
print(df.head())
print("\n=== Estatísticas Descritivas ===")
print(df.describe())
print("\n=== Valores Nulos ===")
print(df.isnull().sum())
print("\n=== Contagem de Culturas (Crop) ===")
if 'Crop' in df.columns:
    print(df['Crop'].value_counts())
elif 'Cultura' in df.columns:
    print(df['Cultura'].value_counts())
