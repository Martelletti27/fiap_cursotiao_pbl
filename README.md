# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# PROJETO FARMTECH SOLUTIONS

## 👥 Integrantes: 
- <a href="https://github.com/Emarinhos">Everton</a>
- <a href="https://github.com/Juliagutierres29">Julia</a>
- <a href="https://github.com/rm567718">Nayara</a> 
- <a href="https://github.com/Xaramandas">Felipe Lourenco</a> 
- <a href="https://github.com/Martelletti27">Matheus</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoy, PhD</a>

## 📜 Descrição:

Projeto acadêmico desenvolvido no curso de Inteligência Artificial (FIAP), com foco em soluções para Agricultura Digital.
O grupo FarmTech Solutions propõe o desenvolvimento de sistemas inteligentes para monitoramento, automação e análise de dados agrícolas, integrando Python, R e IoT (ESP32).

## 🗂 ESTRUTURA GERAL

```
fiap_cursotiao_pbl/
│
├── Fase 1/                          # Manejo e cálculo de insumos
│   ├── apps/
│   │   ├── python_app/              # CLI para cálculo de manejo
│   │   └── r_app/                   # Análise de aplicação e API Meteorológica
│   └── docs/                        # Link YouTube do funcionamento
│
├── Fase 2/                          # Sistema de irrigação inteligente (IoT + API)
│   └── apps/
│       ├── esp32_app/               # Automação de irrigação com ESP32 (Wokwi)
│       ├── python_integration/      # Integração com API Meteorológica (Open-Meteo)
│       └── r_integration/           # Análise para decisão inteligente de irrigação
│
├── Fase 3/                          # Banco de dados e sensores
│   ├── scripts/                    # Consultas SQL
│   ├── assets/                     # Dados e assets
│   └── README.md                   # Manual de importação Oracle
│
├── Fase 4/                          # ML - Previsão de umidade do solo
│   ├── dashboard.py                # Interface Streamlit
│   ├── phase1_regression.py        # Modelos de regressão
│   ├── weather_api.py              # API meteorológica (Open-Meteo)
│   ├── recommendations.py          # Recomendações de irrigação
│   └── requirements.txt
│
├── Fase 5/                          # ML - Previsão de rendimento + Cloud
│   ├── Parte 1/                     # Notebook - Previsão de rendimento de safra
│   │   ├── everton_marinhos_rm566767_pbl_fase5.ipynb
│   │   └── data/crop_yield.csv
│   ├── Parte 2/                     # Comparativo de custos AWS
│   │   └── comparacao_aws.md
│   └── README.md
│
└── README.md                        # Este arquivo
```

## 🔧 Como executar o código

📘 FASE 1 - MANEJO E CALCULO DE INSUMOS

Nesta primeira fase, foi desenvolvido um sistema em Python e R para o planejamento de manejo agrícola, permitindo o cálculo de áreas, doses de produtos e análise de tratamentos.

🔹 Funcionalidades principais

      Cálculo de área plantada (retangular ou pivô circular)

      Estimativa de insumos e aplicações por hectare

      Registro de manejos e produtos utilizados

      Exportação de dados em CSV para análise no R

🔗 Código: `Fase 1/apps/python_app/`


___________________________________________________________________________
📘 FASE 2 - SISTEMA DE IRRIGAÇÃO INTELIGENTE (IoT + API)

Evolução do projeto para um sistema automatizado de irrigação, utilizando o ESP32 no Wokwi e integração com dados meteorológicos via API pública (Open-Meteo).

🎯 Objetivo

    Acionar automaticamente a bomba d’água (relé) com base em:

    Níveis de nutrientes simulados (NPK)

    Faixa de pH ideal (via LDR)

    Umidade mínima (via DHT22)

    Previsão de chuva e probabilidade de precipitação (POP) fornecidas pela integração Python

🔧 Sensores simulados no Wokwi

    Parâmetro	      Sensor/Ferramenta      Pino ESP32
    Nitrogênio (N)	  Botão verde          12
    Fósforo (P)	      Botão verde          13
    Potássio (K)      Botão verde          14
    pH                LDR                  34
    Umidade	          DHT22                15
    Bomba             Relé                 26

🔬 Lógica de decisão da irrigação

O ESP32 avalia continuamente as leituras dos sensores e o token meteorológico.

    Condição                                  Ação
    Umidade < 40%                             Irrigação permitida
    pH entre 5.5 e 7.5	                      pH ok
    Pelo menos 1 botão NPK ativo	            Nutrientes ok
    Chuva prevista (rainBlock = true)	        Irrigação bloqueada
    Todas as condições válidas	              Relé (bomba) ligado

🔗 Guia detalhado de execução: `Fase 2/apps/esp32_app/README.md`

___________________________________________________________________________
📘 FASE 3 - BANCO DE DADOS E SENSORES

Importação da base de sensores (fase2_sensor_readings.csv) para Oracle SQL Developer e consultas.

🔗 Manual de importação: `Fase 3/README.md`

___________________________________________________________________________
📘 FASE 4 - ML - PREVISÃO DE UMIDADE DO SOLO

Sistema de Machine Learning para previsão de umidade do solo e recomendações inteligentes de irrigação, com integração à API Open-Meteo.

🔹 Funcionalidades principais
- Modelos de regressão (Linear, Ridge, Lasso, Random Forest, Gradient Boosting)
- Dashboard Streamlit interativo
- Cronograma automático de irrigação para 7 dias
- Integração com API meteorológica (sem cadastro)

🔗 Para executar:
```bash
cd Fase 4
pip install -r requirements.txt
streamlit run dashboard.py
```
Consulte `Fase 4/README.md` para detalhes.

___________________________________________________________________________
📘 FASE 5 - ML - PREVISÃO DE RENDIMENTO DE SAFRA + CLOUD

**Parte 1** — Notebook de Machine Learning para previsão de rendimento (ton/ha) por cultura (cacau, palma, arroz, borracha): PCA, K-Means, clustering, múltiplos modelos de regressão e simulador de produtividade.

**Parte 2** — Documentação de comparativo de custos e região AWS.

🔗 Para executar o notebook (Parte 1):
```bash
cd "Fase 5/Parte 1"
pip install pandas numpy matplotlib seaborn scikit-learn xgboost
# Abra everton_marinhos_rm566767_pbl_fase5.ipynb no Jupyter
```
Consulte `Fase 5/README.md` para detalhes.

___________________________________________________________________________
## 🗃 Histórico de lançamentos
* 0.1.0 - 15/09/2025
* 0.2.0 - 15/10/2025

___________________________________________________________________________
🧾 Licença

 <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
