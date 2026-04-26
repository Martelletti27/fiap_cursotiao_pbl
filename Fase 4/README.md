# 🌾 Sistema Inteligente de Manejo Agrícola

Sistema completo de Machine Learning para previsão de umidade do solo e recomendações inteligentes para gestão agrícola, com integração de dados meteorológicos em tempo real.

## 📋 Características

- **Modelos de Regressão**: 5 algoritmos para prever Umidade do Solo
- **API Meteorológica**: Integração automática com Open-Meteo (gratuita, sem cadastro)
- **Recomendações Inteligentes**: Cronograma automático de irrigação para 7 dias
- **Dashboard Interativo**: Interface Streamlit com 5 abas completas
- **Carregamento Automático**: Dados meteorológicos carregados automaticamente por município

## Como executar o código

Na pasta do projeto (ex.: `Fase 4/` na raiz do repositório):

```bash
pip install -r requirements.txt
```

Coloque `base_sintetica_pivo_2025.csv` em `data/` ou faça upload pela interface, depois suba o dashboard:

```bash
streamlit run dashboard.py
```

Alternativa: `python run.py`. (Detalhes e troubleshooting em [QUICKSTART.md](QUICKSTART.md).)

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
├── phase1_regression.py      # Modelos de regressão
├── weather_api.py            # Integração com API meteorológica (Open-Meteo)
├── recommendations.py        # Sistema de recomendações
├── dashboard.py              # Interface Streamlit principal
├── run.py                    # Script de execução
├── test_api.py              # Script de teste da API
├── requirements.txt          # Dependências Python
├── README.md                 # Este arquivo
├── CONFIGURACAO_API.md       # Documentação da API
└── QUICKSTART.md             # Guia rápido de início
```

## 🔧 Funcionalidades

### Aba Resumo
- Métricas gerais do dataset
- Séries temporais interativas (últimos 120 dias)
- Importância das variáveis (Random Forest)

### Aba Análise
- Análise exploratória com gráficos
- Séries temporais com média móvel configurável
- Histogramas de distribuição
- Estatísticas descritivas

### Aba Previsão
- Interface para prever umidade do solo
- Inputs personalizados (temperatura, chuva, umidade do ar, etc.)
- Recomendação automática de irrigação
- Análise detalhada da recomendação

### Aba Recomendação
- Previsão do tempo para 7 dias (dados reais da API)
- Mapa interativo do município
- Cronograma de irrigação automático
- Justificativas técnicas para cada dia
- Gráficos de umidade prevista

### Aba ML
- Comparação de todos os modelos de regressão
- Métricas detalhadas (MAE, MSE, RMSE, R²)
- Gráfico de dispersão (valores reais vs previstos)
- Seleção automática do melhor modelo

## 📊 Modelos Implementados

### Regressão
1. **Linear Regression** - Modelo linear simples
2. **Ridge Regression** - Regularização L2
3. **Lasso Regression** - Regularização L1
4. **Random Forest Regressor** - Ensemble de árvores
5. **Gradient Boosting Regressor** - Boosting sequencial

O sistema compara todos os modelos e seleciona automaticamente o melhor baseado no R² no conjunto de teste.

## 🌦 API Meteorológica

O sistema utiliza a **API Open-Meteo**, que oferece:

- ✅ **Totalmente gratuita** - Sem custos ou limites rígidos
- ✅ **Sem cadastro necessário** - Funciona imediatamente
- ✅ **Sem chave de API** - Não precisa configurar nada
- ✅ **Dados confiáveis** - Baseados em modelos meteorológicos profissionais
- ✅ **Carregamento automático** - Dados carregados ao selecionar município

### Municípios Suportados

- São Paulo
- Campinas
- Ribeirão Preto
- Piracicaba
- Londrina
- Cascavel
- Maringá

Para mais informações, consulte [CONFIGURACAO_API.md](CONFIGURACAO_API.md).

## 🧪 Testando a API

Para testar se a API está funcionando:

```bash
cd "Fase 4"
python test_api.py
```

O script testa todos os municípios cadastrados e exibe um relatório completo.

## 📝 Notas

- Os modelos são treinados automaticamente ao carregar os dados
- O melhor modelo é selecionado automaticamente baseado em R²
- Dados meteorológicos são carregados automaticamente ao selecionar município
- Cache inteligente evita requisições desnecessárias à API
- Sistema exibe status da API no menu lateral

## 🔍 Requisitos

- Python 3.8+
- Streamlit 1.28+
- Scikit-learn 1.3+
- Pandas 2.0+
- Plotly 5.17+
- Requests 2.31+

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique o arquivo [QUICKSTART.md](QUICKSTART.md) para guia rápido
2. Consulte [CONFIGURACAO_API.md](CONFIGURACAO_API.md) para questões sobre a API
3. Execute `python test_api.py` para diagnosticar problemas com a API
