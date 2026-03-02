# 🌾 FarmTech Solutions - Fase 5

Nesta fase oficial do Agroprojeto (**Machine Learning na Cabeça**), nossa equipe (FarmTech Solutions) desenvolveu duas grandes entregas que visam elevar o nível de inteligência da Fazenda (200 Hectares): criação de Modelagem Preditiva Avançada (IA) e Arquitetura/Estimativa de Cloud Computing.

### 👥 Integrantes do Grupo: 
- Everton (RM566767)
- Julia (RM...)
- Nayara (RM567718)
- Xavier (RM...)
- Matheus (RM...)

---

## 📘 Entrega 1: Machine Learning - Previsão de Rendimento de Safra

Por meio do dataset `crop_yield.csv`, contendo histórico de clima e umidade das plantações, nosso time elaborou um **Jupyter Notebook Oficial** resolvendo os seguintes desafios:

1. **Análise Exploratória de Dados (EDA):** Verificação de tipos de plantações (Arroz, Palma, Cacau...), distribuição histórica de impacto da Chuva x Rendimento x Temperatura com visualização no `seaborn`;
2. **Clusterização (Não-Supervisionada):** Uso do `K-Means` após Scaling para segmentar as safras em 3 grupos de alta/entresafra produtividade, evidenciando instabilidades climáticas;
3. **Regressão (Supervisionada):** Transformamos variáveis categóricas via Pipeline (One-Hot Encoding) e submetemos à base de treinamento 5 modelos de IA (*Regressão Linear, Árvore de Decisão, SVR, Graident Boosting e Random Forest*).
   - > **Vencedor:** O algoritmo **Random Forest Regressor** apresentou o maior poder preditivo no *R² Score* e a menor taxa de erro absoluto.

🔗 **Acesse o Jupyter Notebook da Solução Aqui:** [`everton_marinhos_rm566767_pbl_fase5.ipynb`](./everton_marinhos_rm566767_pbl_fase5.ipynb)

▶️ **Acesse o Link do Vídeo Pitch:** *[INSIRA_O_LINK_YOUTUBE_AQUI]*

---

## 📘 Entrega 2: Cloud Computing - Estimativa AWS

Nossa Machine Learning precisa ser hospedada em Nuvem. Simulamos os custos mensais através da calculadora oficial da AWS na modalide On-Demand para uma máquina Linux de `2 vCPUs`, `1 GiB RAM`, `Banda 5 Gigabit` e `HD 50GB`.

### 💰 Comparativo

| Região AWS | Custo Instância (EC2/mês) | Custo Armaz. (EBS 50gb/mês) | **[TOTAL]** |
| :--- | :--- | :--- | :--- |
| **São Paulo (sa-east-1)** | ~$11.83 USD | ~$6.50 USD | **~$18.33 USD** |
| **N. Virginia (us-east-1)** | ~$7.60 USD | ~$4.00 USD | **~$11.60 USD** |

### ⚖️ Escolha e Justificativa Técnica/Legal

Apesar da região de São Paulo ter um custo final **58% mais caro** ($18.33), **ela é a escolha definitiva e obrigatória** pelo seguinte embasamento provocado pelo enunciado:

1. **Acesso Rápido aos Sensores e ML (Baixa Latência):** Ao hospedar a API de Machine Learning no Brasil (São Paulo), o tempo de percurso do tráfego de rede gerado intermitentemente pelos ESP32 das fazendas cai drasticamente, evitando travamentos, perda de pacotes ou *delays* pesados na exibição da IA no Painel (*Dashboard*). 
2. **Restrições Legais e Soberania dos Dados:** O armazenamento da base contendo segredos agropecuários, modelagem e cruzamentos de clima são sensíveis. Devido às premissas corporativas das agrotechs e leis regionais modernas (ex: LGPD em terras nacionais e a *Marco Civil* exigindo repouso físico do disco onde são hospedados sob a jurisdição originária), hospedar o EBS de `50GB` em São Paulo livra a FarmTech Solutions de sanções judiciais complexas caso o servidor ficasse ancorado na Virginia (USA).

▶️ **Acesse o Link do Vídeo Cloud:** *[INSIRA_O_LINK_YOUTUBE_AQUI]*

---
*Projeto em constante desenvolvimento - Equipe FarmTech Solutions*
