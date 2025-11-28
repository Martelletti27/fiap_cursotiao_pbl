# 🌤️ API Meteorológica - Open-Meteo

O sistema utiliza a **API Open-Meteo**, uma API meteorológica gratuita, de código aberto e **sem necessidade de cadastro ou chave de API**.

## ✅ Vantagens da Open-Meteo

- ✅ **Totalmente gratuita** - Sem custos ou limites rígidos
- ✅ **Sem cadastro necessário** - Funciona imediatamente
- ✅ **Sem chave de API** - Não precisa configurar nada
- ✅ **Dados confiáveis** - Baseados em modelos meteorológicos profissionais
- ✅ **Cobertura global** - Funciona para qualquer localização
- ✅ **Atualizações frequentes** - Dados atualizados regularmente

## 🚀 Como Funciona

O sistema funciona **automaticamente** sem necessidade de configuração:

1. **Ao iniciar o sistema:** A API é testada automaticamente
2. **Ao selecionar município:** Os dados são carregados automaticamente
3. **Ao mudar município:** Os dados são recarregados automaticamente

## 📍 Municípios Cadastrados

O sistema está configurado para os seguintes municípios:

- ✅ São Paulo
- ✅ Campinas
- ✅ Ribeirão Preto
- ✅ Piracicaba
- ✅ Londrina
- ✅ Cascavel
- ✅ Maringá

Todos os municípios têm coordenadas geográficas mapeadas e estão prontos para uso.

## ✅ Testando a API

Para testar se a API está funcionando, execute:

```bash
cd "Fase 4"
python test_api.py
```

O script irá:
- Testar a conexão com a API
- Testar todos os municípios cadastrados
- Exibir um relatório completo com dados reais

## 📊 Dados Disponíveis

A API fornece os seguintes dados para cada dia:

- **Temperatura:** Média, máxima e mínima (°C)
- **Precipitação:** Volume de chuva previsto (mm)
- **Probabilidade de Chuva:** Percentual de chance de chuva (%)
- **Umidade Relativa:** Umidade do ar (%)

## 🔄 Funcionamento Automático

Uma vez que o sistema está rodando:

1. **Status da API:** Exibido no menu lateral
   - ✅ "API meteorológica conectada" se estiver funcionando
   - ⚠️ "API meteorológica não disponível" se houver problemas

2. **Carregamento de Dados:**
   - Dados são carregados automaticamente ao selecionar um município
   - Cache inteligente evita requisições desnecessárias
   - Dados são atualizados ao mudar de município

## 🐛 Solução de Problemas

### Erro: "API meteorológica não disponível"

**Possíveis causas:**
- Problemas de conexão com a internet
- API temporariamente fora do ar
- Firewall bloqueando requisições

**Soluções:**
- Verifique sua conexão com a internet
- Aguarde alguns minutos e tente novamente
- Verifique se o firewall não está bloqueando requisições HTTPS

### Erro: "Nenhum dado retornado"

**Possíveis causas:**
- Coordenadas do município não encontradas
- Problema temporário na API

**Soluções:**
- Verifique se o município está na lista cadastrada
- Tente com outro município
- Execute o script de teste para diagnóstico

## 📚 Documentação da API

- **Site oficial:** https://open-meteo.com/
- **Documentação:** https://open-meteo.com/en/docs
- **Status da API:** Geralmente 99.9% de disponibilidade

## 🎯 Limites e Política de Uso

A API Open-Meteo é gratuita e não possui limites rígidos, mas recomenda-se:
- Não fazer mais de 10.000 requisições por dia
- Respeitar um intervalo mínimo de 1 segundo entre requisições
- Usar cache quando possível (já implementado no sistema)

## ✨ Resumo

**Não é necessário fazer nada!** A API funciona automaticamente assim que o sistema é iniciado. Apenas selecione o município e os dados serão carregados automaticamente.
