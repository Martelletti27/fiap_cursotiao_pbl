# Entrega 2: Computação em Nuvem - Estimativa AWS

A FarmTech Solutions precisa hospedar a API de Machine Learning e os receptores de dados dos sensores (ESP32) na nuvem. Foi solicitada uma estimativa de custos para instâncias **On-Demand (100% de uso mensal)** comparando as regiões **São Paulo (sa-east-1)** e **Norte da Virgínia (us-east-1)** utilizando a Calculadora de Preços da AWS, com a seguinte infraestrutura base:

- **Sistema Operacional:** Linux
- **VCPUs:** 2
- **Memória:** 1 GiB
- **Banda de Rede:** Até 5 Gigabit
- **Armazenamento de Bloco:** 50 GB (Amazon EBS - gp3)

---

## 1. Estimativa de Custos (Calculadora AWS)

Para atender a capacidade solicitada (*2 vCPUs e 1 GiB RAM*), a instância mais barata e eficiente encontrada na AWS foi a **t4g.micro** (instância com processador ARM graviton, que oferece melhor custo-benefício).

### 🇺🇸 Região: US East (N. Virginia - us-east-1)
- **Custo Computacional (EC2 t4g.micro):** ~ $1.53 USD / mês
- **Custo de Armazenamento (EBS gp3 50GB):** ~ $4.00 USD / mês
- **Total Mensal Estimado:** **~$5.53 USD**

### 🇧🇷 Região: South America (São Paulo - sa-east-1)
- **Custo Computacional (EC2 t4g.micro):** ~ $4.31 USD / mês
- **Custo de Armazenamento (EBS gp3 50GB):** ~ $5.70 USD / mês
- **Total Mensal Estimado:** **~$10.01 USD**

> *Nota: Os valores são aproximados baseados na tabela oficial da AWS Calculator no regime On-Demand (sem fidelidade/Reserved Instances).*

---

## 2. Análise Técnica e Escolha da Região

### Desafio Proposto
*Você precisa acessar rapidamente os dados dos sensores e há restrições legais para armazenamento no exterior.*

### Escolha e Justificativa

A opção escolhida deve ser obrigatoriamente a região de **São Paulo (sa-east-1)**, apesar de ter um custo On-Demand aproximadamente **81% mais caro** ($10.01 vs $5.53). A justificativa técnica e legal sustenta-se em dois pilares principais exigidos pelo cenário:

1. **Baixa Latência (Acesso Rápido):** A API estará recebendo dados dos sensores IoT do campo continuamente. Hospedar os recursos em São Paulo (sa-east-1) garante um tempo de resposta (ping/latência) extremamente menor para os dispositivos localizados no Brasil em comparação à Virgínia (us-east-1). Isso previne *timeouts* no ESP32, agiliza a inferência de Machine Learning e fornece dados de produtividade agrícola em tempo real para os painéis de forma fluida.

2. **Compliance e Restrições Legais:** O cenário indica que existem *restrições legais protetivas* para armazenamento de dados da fazenda fora do país de origem. No Brasil, regulações como a LGPD (Lei Geral de Proteção de Dados) e normas corporativas do segmento agropecuário muitas vezes exigem que bases de dados críticas (como os históricos de 200 hectares, cruzamentos meteorológicos, e segredos industriais de fertilização relatados nas features) sejam processadas e repousem sob **jurisdição territorial originária**. Ao hospedar o volume EBS de 50GB em `sa-east-1`, a FarmTech Solutions atende 100% aos requisitos de *data sovereignty* (soberania dos dados).
