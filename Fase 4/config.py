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

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
INMET_API_URL = "https://apitempo.inmet.gov.br/estacao"

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
# CONFIGURAÇÕES PARA FASE 2 - CLASSIFICAÇÃO
# ============================================================================
# Define a variável alvo e features para prever se o sistema de irrigação
# será acionado (Relay_On = 1) ou não (Relay_On = 0)
# Inclui a umidade do solo como feature, pois ela influencia a decisão de irrigar

CLASSIFICATION_TARGET = "Relay_On"

CLASSIFICATION_FEATURES = [
    "Umidade do Solo",
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
