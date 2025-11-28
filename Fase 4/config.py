"""
Arquivo de Configuração Global do Sistema

Este módulo centraliza todas as configurações do sistema de manejo agrícola,
incluindo caminhos de arquivos, parâmetros de modelos, variáveis de features
e configurações de APIs externas. Centralizar essas configurações facilita
a manutenção e permite ajustes rápidos sem modificar o código principal.
"""
import os

# ============================================================================
# CONFIGURAÇÃO DE CAMINHOS E DIRETÓRIOS
# ============================================================================
# Define os caminhos base do projeto e cria os diretórios necessários
# para armazenar dados e modelos treinados

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Cria os diretórios automaticamente se não existirem
# Isso garante que o sistema funcione mesmo sem estrutura pré-existente
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Caminho completo para o arquivo de dados padrão
# O sistema tentará carregar este arquivo automaticamente na inicialização
DATA_FILE = os.path.join(DATA_DIR, "base_sintetica_pivo_2025.csv")

# ============================================================================
# CONFIGURAÇÕES DE API METEOROLÓGICA
# ============================================================================
# Configurações para integração com serviços de previsão do tempo
# O sistema usa OpenWeatherMap por padrão, mas pode ser configurado
# para outras APIs através das variáveis de ambiente

# API Open-Meteo (gratuita, sem necessidade de cadastro ou chave)
# Não é necessário configurar chave de API - a API é totalmente gratuita
# Documentação: https://open-meteo.com/en/docs
WEATHER_API_KEY = ""  # Não utilizado - mantido para compatibilidade

# URL da API Open-Meteo para previsão meteorológica
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Lista de municípios cadastrados no sistema
MUNICIPIOS_CADASTRADOS = [
    "São Paulo",
    "Campinas",
    "Ribeirão Preto",
    "Piracicaba",
    "Londrina",
    "Cascavel",
    "Maringá"
]

# ============================================================================
# CONFIGURAÇÕES DE MODELOS DE MACHINE LEARNING
# ============================================================================
# Parâmetros globais que garantem reprodutibilidade dos experimentos
# RANDOM_STATE: semente para geradores aleatórios (garante resultados consistentes)
# TEST_SIZE: proporção dos dados reservada para teste (20% = 0.2)

RANDOM_STATE = 42
TEST_SIZE = 0.2

# ============================================================================
# CONFIGURAÇÕES PARA FASE 1 - REGRESSÃO
# ============================================================================
# Define a variável alvo e as features utilizadas para prever a umidade do solo
# O modelo de regressão usará essas features para aprender padrões e fazer previsões

REGRESSION_TARGET = "Umidade do Solo"

REGRESSION_FEATURES = [
    "PH",
    "Temperatura",
    "Nível de Nitrogênio",
    "Nível de Fósforo",
    "Nível de Potássio",
    "Probabilidade de Chuva",
    "Chuva Real (mm)",
]

# ============================================================================
# ESTÁGIOS FENOLÓGICOS POR CULTURA
# ============================================================================
# Define os estágios de desenvolvimento de cada cultura agrícola
# Esses estágios são importantes pois diferentes fases da planta têm
# necessidades hídricas distintas, influenciando as recomendações de irrigação

ESTAGIOS_SOJA = [
    "Germinação",
    "Vegetativo",
    "Florescimento",
    "Enchimento de Grãos",
    "Maturação"
]

ESTAGIOS_MILHO = [
    "Germinação",
    "Vegetativo",
    "Pendoamento",
    "Grãos Leitosos",
    "Maturação"
]

ESTAGIOS_CAFE = [
    "Vegetativo",
    "Floração",
    "Chumbinho",
    "Granação",
    "Maturação"
]

# Dicionário que mapeia cada cultura aos seus estágios
# Facilita o acesso programático aos estágios durante o processamento
ESTAGIOS_POR_CULTURA = {
    "SOJA": ESTAGIOS_SOJA,
    "MILHO": ESTAGIOS_MILHO,
    "CAFÉ": ESTAGIOS_CAFE,
}
