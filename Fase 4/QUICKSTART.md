# 🚀 Guia Rápido de Início

## Instalação Rápida

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Colocar o arquivo de dados na pasta data/
# Ou fazer upload via interface do Streamlit

# 3. Executar o dashboard
streamlit run dashboard.py
```

## 📋 Checklist de Uso

1. ✅ Instalar dependências (`pip install -r requirements.txt`)
2. ✅ Ter o arquivo `base_sintetica_pivo_2025.csv` disponível
3. ✅ Executar `streamlit run dashboard.py`
4. ✅ No menu lateral:
   - Selecionar Município
   - Selecionar Cultura (SOJA, MILHO ou CAFÉ)
   - Fazer upload do CSV ou usar arquivo padrão
   - Clicar em "Carregar Dados"
5. ✅ Aguardar treinamento dos modelos (pode levar alguns minutos)
6. ✅ Explorar as 5 abas do dashboard

## 🔧 Configuração Opcional

### API Meteorológica Real

Para usar API real ao invés de dados simulados:

1. Obter API key do OpenWeatherMap: https://openweathermap.org/api
2. Configurar variável de ambiente:
   ```bash
   # Windows PowerShell
   $env:WEATHER_API_KEY="sua_chave_aqui"
   
   # Linux/Mac
   export WEATHER_API_KEY="sua_chave_aqui"
   ```

## 📊 Estrutura de Dados Esperada

O arquivo CSV deve conter as seguintes colunas:

- `ID`: Identificador numérico
- `Data`: Data (YYYY-MM-DD)
- `Hora`: Horário (HH:MM)
- `Cultura`: SOJA, MILHO ou CAFÉ
- `Estágio Fenológico`: Estágio da planta
- `Umidade do Solo`: Variável alvo de regressão (%)
- `PH`: Acidez do solo
- `Temperatura`: Temperatura ambiente (°C)
- `Nível de Nitrogênio`: Índice (30-95)
- `Nível de Fósforo`: Índice (30-95)
- `Nível de Potássio`: Índice (30-95)
- `Probabilidade de Chuva`: Previsão (%)
- `Chuva Real (mm)`: Volume real
- `Status de Irrigação`: HOLD, WAIT_RAIN ou IRRIGATE
- `Relay_On`: Variável alvo de classificação (0 ou 1)

## ⚠️ Solução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique se o arquivo CSV está na pasta `data/`
- Ou faça upload via interface do Streamlit

### Erro: "Modelo não disponível"
- Certifique-se de clicar em "Carregar Dados" primeiro
- Aguarde o treinamento dos modelos completar

### Performance lenta
- Reduza o tamanho do dataset para testes
- Os modelos são treinados a cada carregamento (pode levar tempo)

## 📞 Suporte

Para mais informações, consulte o `README.md` principal.
