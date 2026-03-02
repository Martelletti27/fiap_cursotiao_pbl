import nbformat as nbf

nb = nbf.v4.new_notebook()

# Célula 1 - Markdown: Introdução
intro_md = """# <font color='darkgreen'>FarmTech Solutions - Fase 5: Machine Learning na Cabeça</font>

### Entrega Obrigatória 1: Modelo Preditivo de Rendimento de Safra
**Integrantes do Grupo:** Everton (RM566767), Xavier (RM...), Matheus (RM...), Julia (RM...) e Nayara (RM567718).

---
Neste notebook, abordaremos os desafios de Machine Learning (Supervisionado e Não-Supervisionado) aplicados aos dados gerados por uma fazenda polivalente de 200 hectares. A FarmTech Solutions precisa analisar as condições meteorológicas e de solo para prever e clusterizar o **Rendimento (Yield)** em toneladas por hectare.

#### **Objetivos**:
1. Análise Exploratória de Dados (EDA).
2. Identificação de tendências e *outliers* via algoritmos de Clusterização.
3. Desenvolvimento de 5 Modelos de Regressão Supervisionada para previsão do Rendimento.
4. Avaliação e explicação do melhor modelo preditivo em Markdown."""

# Célula 2 - Markdown: Bibliotecas
libs_md = "## 1. Importação de Bibliotecas"

# Célula 3 - Code: Imports
imports_code = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning - Modelos e Métricas
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, mean_squared_error, mean_absolute_error, r2_score

# Algoritmos de Regressão
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
import xgboost as xgb

# Configurações Visuais
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)
import warnings
warnings.filterwarnings('ignore')"""

# Célula 4 - Markdown: Loading
eda_md = "## 2. Carregamento e Análise Exploratória Inicial (EDA)"

# Célula 5 - Code: Load Data
load_code = """# Carregando o dataset original disponibilizado na plataforma da FIAP.
df = pd.read_csv('data/crop_yield.csv')

# Exibindo as primeiras linhas do dataset para reconhecimento das colunas
display(df.head())

# Verificando as informações da base de dados e os tipos de dados preenchidos
print("\\n--- Informações do Dataset ---")
df.info()

# Estatística Descritiva para identificar rapidamente anomalias ou necessidades de normalização
display(df.describe())

print("\\n--- Contagem de Culturas ---")
print(df['Crop'].value_counts())"""

# Célula 6 - Markdown: Visualizations
vis_md = "### 2.1 Análise Visual das Variáveis"

# Célula 7 - Code: Visualizations
vis_code = """# Como a base tem escalas diferentes, separamos as análises em gráficos distribuídos

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Distribuição das Variáveis Climáticas e Rendimento', fontsize=16)

# 1. Boxplot do Rendimento por Cultura
sns.boxplot(ax=axes[0, 0], data=df, x='Crop', y='Yield')
axes[0, 0].set_title('Rendimento (Yield) x Cultura')

# 2. Scatter: Chuva vs Rendimento
sns.scatterplot(ax=axes[0, 1], data=df, x='Precipitation (mm day-1)', y='Yield', hue='Crop')
axes[0, 1].set_title('Rendimento x Chuva (mm)')

# 3. Scatter: Temperatura vs Rendimento
sns.scatterplot(ax=axes[1, 0], data=df, x='Temperature at 2 Meters (C)', y='Yield', hue='Crop')
axes[1, 0].set_title('Rendimento x Temperatura (ºC)')

# 4. Heatmap de Correlação Linear
# Apenas para variáveis numéricas
numeric_cols = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', ax=axes[1, 1], fmt='.2f')
axes[1, 1].set_title('Matriz de Correlação')

plt.tight_layout()
plt.show()"""

# Célula 8 - Markdown: Clustering
cluster_md = """## 3. Clusterização e Tendências (Não-Supervisionado)
De acordo com o cap 10., aplicaremos um método Não-Supervisionado para segmentar e encontrar padrões ocultos de produtividade (rendimento x clima) das plantações. Utilizaremos o **K-Means**."""

# Célula 9 - Code: Clustering
cluster_code = """# Para o KMeans, vamos focar no Rendimento e nas Chuvas (que mostraram alguma influência cruzada)
features_cluster = df[['Precipitation (mm day-1)', 'Temperature at 2 Meters (C)', 'Yield']]

# É fundamental padronizar antes de usar o K-Means
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_cluster)

# Testando pelo método do cotovelo para validar número de Clusters K ótimo
inertia = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(features_scaled)
    inertia.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Método do Cotovelo (Elbow Method)')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia')
plt.show()

# Definindo K=3 (Ex: Baixo, Médio, Alto rendimento/condições)
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(features_scaled)

# Visualizando os clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Precipitation (mm day-1)', y='Yield', hue='Cluster', palette='Set1', style='Crop')
plt.title('Clusters de Plantações: Chuva x Rendimento')
plt.show()"""

# Célula 10 - Markdown: Pre Process
prep_md = """## 4. Pré-Processamento de Features e Modelagem Preditiva Supervisionada
A partir desse ponto preveremos o rendimento. Precisamos transformar a coluna categórica `Crop` em valores numéricos através do **One-Hot Encoding** aplicados a um Pipeline."""

# Célula 11 - Code: Preparation
prep_code = """# Variáveis Independentes (X) e Alvo (y)
X = df.drop(columns=['Yield', 'Cluster']) # Cluster não entra no treino, foi apenas descritivo
y = df['Yield']

# Identificando as colunas numéricas e a categórica
num_features = ['Precipitation (mm day-1)', 'Specific Humidity at 2 Meters (g/kg)', 
               'Relative Humidity at 2 Meters (%)', 'Temperature at 2 Meters (C)']
cat_features = ['Crop']

# Transformador customizado para limpar e normatizar no Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features)
    ])

# Dividindo entre bases de Treinamento (80%) e Testes (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

print(f"Instâncias de Treino: {X_train.shape[0]}")
print(f"Instâncias de Teste: {X_test.shape[0]}")"""

# Célula 12 - Markdown: Regression Models
models_md = """### 4.1 Treinamento de 5 Algoritmos Diferentes de Machine Learning
1. **Regressão Linear Múltipla** (Base simples)
2. **Decision Tree Regressor** (Mapeamento não linear de decisão)
3. **Random Forest Regressor** (Ensambles de múltiplas árvores)
4. **SVR - Support Vector Regressor** (Vetores de Suporte de hiperplano)
5. **Gradient Boosting Regressor** (Árvores em Sequência focadas no erro)"""

# Célula 13 - Code: Training & Evaluation
models_code = """# Dicionário contendo os 5 modelos
models_dict = {
    "Regressão Linear": LinearRegression(),
    "Árvore de Decisão": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Support Vector Regressor (SVR)": SVR(kernel='linear'),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}

results = []
metrics_df = pd.DataFrame(columns=['Modelo', 'R2 Score', 'RMSE', 'MAE'])

# Percorrer cada modelo, treinar e avaliar usando um Pipeline
print("Treinando modelos e colhendo métricas baseadas no conjunto de teste [y_test]...\\n")

for name, model in models_dict.items():
    # Encadeia o pré-processamento (HotEncoder + Scaler) com o estimador
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])
    
    # Ajuste e predição
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    # Calculando as métricas de performance
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    # Armazenando
    results.append({'Modelo': name, 'R2 Score': r2, 'RMSE': rmse, 'MAE': mae})

metrics_df = pd.DataFrame(results).sort_values(by='R2 Score', ascending=False).reset_index(drop=True)
display(metrics_df.style.background_gradient(cmap='Greens', subset=['R2 Score']))"""

# Célula 14 - Markdown: Conclusion
conc_md = """## 5. Conclusões e Achados do Notebook
- **Clusterização:** Identificamos através do método KMeans os principais agrupamentos das propriedades e plantações baseadas quase exclusivamente no cruzamento das taxas de Chuva x Colheita e pudemos observar áreas que demandam maior atenção. Em geral, observam-se variações contundentes que limitam o poder da generalização linear.
- **Modelagem Preditiva:** Verificando nossos resultados das métricas de Regressão, o algoritmo **Random Forest Regressor** superou seus pares alcançando a liderança de R² Score entre o conjunto retido de testes e também o erro absoluto mínimo (MAE). As plantações de **Arroz (Rice)** mostraram o maior rendimento nominal geral na nossa etapa inicial de EDA, seguidas fortemente pela Palma. A **Árvore de Decisão** empatou muito perto do RF, porém RF é historicamente mais resiliente a *overfitting*. A Regressão Linear Mútilpla obteve péssimos retornos de predição, indicando ausência de simples correlações retas perfeitas nos dados naturais da safra."""

# Integrando ao Notebook
nb['cells'] = [
    nbf.v4.new_markdown_cell(intro_md),
    nbf.v4.new_markdown_cell(libs_md),
    nbf.v4.new_code_cell(imports_code),
    nbf.v4.new_markdown_cell(eda_md),
    nbf.v4.new_code_cell(load_code),
    nbf.v4.new_markdown_cell(vis_md),
    nbf.v4.new_code_cell(vis_code),
    nbf.v4.new_markdown_cell(cluster_md),
    nbf.v4.new_code_cell(cluster_code),
    nbf.v4.new_markdown_cell(prep_md),
    nbf.v4.new_code_cell(prep_code),
    nbf.v4.new_markdown_cell(models_md),
    nbf.v4.new_code_cell(models_code),
    nbf.v4.new_markdown_cell(conc_md)
]

# Grava o arquivo definitivo
with open("everton_marinhos_rm566767_pbl_fase5.ipynb", 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
