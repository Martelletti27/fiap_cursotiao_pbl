# 🌾 Sistema Inteligente de Manejo Agrícola

Sistema completo de Machine Learning para previsão de umidade do solo, classificação de irrigação e recomendações inteligentes para gestão agrícola.

## 📋 Características

- **FASE 1 - Regressão**: 5 modelos para prever Umidade do Solo (com e sem PCA)
- **FASE 2 - Classificação**: 5 modelos para prever acionamento de irrigação
- **API Meteorológica**: Integração com previsão do tempo
- **Recomendações Inteligentes**: Cronograma automático de irrigação para 7 dias
- **Dashboard Interativo**: Interface Streamlit com 5 abas completas

## 🚀 Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Coloque o arquivo `base_sintetica_pivo_2025.csv` na pasta `data/` ou faça upload via interface.

## 🎯 Uso

Execute o dashboard:

```bash
streamlit run dashboard.py
```

Ou use o script de execução:

```bash
python run.py
```

## 📁 Estrutura do Projeto

```
Fase 4/
├── config.py                 # Configurações globais
├── data_loader.py            # Carregamento e pré-processamento
├── phase1_regression.py      # Modelos de regressão (FASE 1)
├── phase2_classification.py  # Modelos de classificação (FASE 2)
├── weather_api.py            # Integração com API meteorológica
├── recommendations.py        # Sistema de recomendações
├── dashboard.py              # Interface Streamlit principal
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

## 🔧 Funcionalidades

### Aba Resumo
- Métricas gerais do dataset
- Séries temporais interativas
- Importância das variáveis

### Aba Análise
- Análise exploratória com gráficos
- Séries temporais com média móvel
- Histogramas de distribuição

### Aba Previsão
- Interface para prever umidade do solo
- Inputs personalizados
- Explicação baseada em importância

### Aba Recomendação
- Previsão do tempo para 7 dias
- Cronograma de irrigação automático
- Justificativas técnicas

### Aba ML
- Comparação de todos os modelos
- Métricas detalhadas
- Análise PCA
- Matrizes de confusão

## 📊 Modelos Implementados

### Regressão (FASE 1)
1. Linear Regression
2. Ridge Regression
3. Lasso Regression
4. Random Forest Regressor
5. Gradient Boosting Regressor

Todos com versões **com e sem PCA**.

### Classificação (FASE 2)
1. Logistic Regression
2. Random Forest Classifier
3. Gradient Boosting Classifier
4. SVM
5. KNN

## 🌦 API Meteorológica

O sistema suporta:
- OpenWeatherMap (com API key)
- Dados simulados (fallback automático)

Configure a variável de ambiente `WEATHER_API_KEY` para usar API real.

## 📝 Notas

- Os modelos são treinados automaticamente ao carregar os dados
- O melhor modelo é selecionado automaticamente
- Todas as previsões incluem explicações baseadas em importância de features

## 🔍 Requisitos

- Python 3.8+
- Streamlit 1.28+
- Scikit-learn 1.3+
- Pandas 2.0+
- Plotly 5.17+

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.
