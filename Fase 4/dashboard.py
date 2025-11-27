"""
Dashboard Streamlit - Interface Principal do Sistema

Este módulo implementa a interface web completa do sistema de manejo agrícola usando
Streamlit. O dashboard é dividido em 5 abas principais: Resumo (visão geral dos dados),
Análise (exploração interativa), Previsão (interface para previsões customizadas),
Recomendação (cronograma de irrigação) e ML (análise técnica dos modelos). O sistema
carrega automaticamente o arquivo CSV padrão e treina todos os modelos ao inicializar,
permitindo análises e previsões imediatas.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import io

warnings.filterwarnings('ignore')

# Importar módulos do projeto
import config
from data_loader import DataLoader
from phase1_regression import Phase1Regression
from phase2_classification import Phase2Classification
from weather_api import WeatherAPI
from recommendations import IrrigationRecommendations

# ============================================================================
# CONFIGURAÇÃO INICIAL DA PÁGINA STREAMLIT
# ============================================================================
# Define o título, ícone e layout da página
# layout="wide" permite usar mais espaço horizontal
# initial_sidebar_state="expanded" deixa o menu lateral aberto por padrão

st.set_page_config(
    page_title="FarmTech Solutions - Sistema Inteligente de Manejo Agrícola",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================
# Define estilos para melhorar a aparência visual do dashboard
# .main-header: estilo para o título principal
# .metric-card: estilo para cards de métricas (reservado para uso futuro)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO DO ESTADO DA SESSÃO
# ============================================================================
# Streamlit mantém estado entre interações através de session_state
# Inicializa variáveis que serão usadas em múltiplas partes do dashboard
# Isso evita recarregar dados e retreinar modelos a cada interação

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df = None
    st.session_state.regression = None
    st.session_state.classification = None
    st.session_state.weather_api = None
    st.session_state.recommendations = None

# ============================================================================
# TÍTULO PRINCIPAL DO DASHBOARD
# ============================================================================

st.markdown('<h1 class="main-header">FarmTech Solutions - Sistema Inteligente de Manejo Agrícola</h1>', unsafe_allow_html=True)

# ============================================================================
# MENU LATERAL - CONFIGURAÇÕES E CONTROLES
# ============================================================================
# O menu lateral contém os controles principais do sistema:
# seleção de município, cultura, upload de arquivo e botão de carregamento

st.sidebar.header("Configurações")

# Lista de municípios disponíveis para seleção
# O município selecionado é usado para consultar previsões meteorológicas
municipios = [
    "São Paulo", "Campinas", "Ribeirão Preto", 
    "Piracicaba", "Londrina", "Cascavel", "Maringá"
]
municipio_selecionado = st.sidebar.selectbox("Município", municipios)

# Lista de culturas disponíveis
# A cultura selecionada filtra os dados e influencia as recomendações
culturas = ["SOJA", "MILHO", "CAFÉ"]
cultura_selecionada = st.sidebar.selectbox("Cultura", culturas)

# Seção de upload de arquivo
# Permite ao usuário fazer upload de um CSV customizado
# Se nenhum arquivo for enviado, o sistema usa o arquivo padrão
st.sidebar.markdown("---")
st.sidebar.subheader("Carregar Dados")
uploaded_file = st.sidebar.file_uploader(
    "Escolha o arquivo CSV",
    type=['csv'],
    help="Faça upload do arquivo base_sintetica_pivo_2025.csv ou deixe vazio para usar o arquivo padrão"
)

# ============================================================================
# PROCESSAMENTO DE CARREGAMENTO DE DADOS
# ============================================================================
# Quando o botão é clicado, o sistema:
# 1. Carrega os dados (do upload ou arquivo padrão)
# 2. Filtra por cultura selecionada
# 3. Pré-processa os dados para regressão e classificação
# 4. Treina todos os modelos (regressão com/sem PCA, classificação)
# 5. Inicializa API meteorológica e sistema de recomendações
# 6. Armazena tudo no session_state para uso nas abas

if st.sidebar.button("Carregar Dados", type="primary", use_container_width=True):
    with st.spinner("Carregando dados e treinando modelos..."):
        try:
            # Cria instância do carregador de dados
            loader = DataLoader()
            
            # Verifica se há arquivo enviado pelo usuário
            if uploaded_file is not None:
                # Lê o arquivo enviado diretamente da memória
                df = pd.read_csv(io.BytesIO(uploaded_file.read()))
                loader.df = df
            else:
                # Carrega automaticamente do arquivo padrão definido em config.py
                # O arquivo padrão está em data/base_sintetica_pivo_2025.csv
                # Se o arquivo não existir, load_data retorna None
                if loader.load_data() is None:
                    st.sidebar.error(f"Arquivo não encontrado: {config.DATA_FILE}")
                    st.stop()
                df = loader.df
            
            # Verifica se os dados foram carregados com sucesso
            if df is not None and len(df) > 0:
                # Armazena dados originais no loader (sem filtro)
                # Isso garante que os modelos sejam treinados com todos os dados disponíveis
                # O filtro por cultura será aplicado apenas para visualização
                loader.df = df.copy()
                
                # Filtra dados pela cultura selecionada apenas para exibição no dashboard
                # Os modelos são treinados com todos os dados para garantir classes balanceadas
                df_filtered = df.copy()
                if "Cultura" in df.columns:
                    df_filtered = df[df["Cultura"] == cultura_selecionada].copy()
                    # Se o filtro resultar em muito poucos dados, mantém todos para visualização também
                    if len(df_filtered) < 50:
                        st.sidebar.info(
                            f"Poucos dados para '{cultura_selecionada}' ({len(df_filtered)} registros). "
                            f"Exibindo todos os dados."
                        )
                        df_filtered = df.copy()
                
                # Armazena dados filtrados para exibição e dados completos no loader
                st.session_state.df = df_filtered
                st.session_state.loader = loader
                
                # Pré-processa dados para modelos de regressão
                # Usa TODOS os dados (sem filtro) para garantir qualidade do modelo
                # Retorna features (X), variável alvo (y) e nomes das features
                X_reg, y_reg, features_reg = loader.preprocess_for_regression()
                
                # Inicializa e treina modelos de regressão
                regression = Phase1Regression()
                regression.initialize_models()
                
                # Treina modelos sem PCA (usa todas as features originais)
                regression.train_models(X_reg, y_reg, use_pca=False)
                
                # Treina modelos com PCA (reduz dimensionalidade)
                # Isso cria versões alternativas de cada modelo para comparação
                # n_components=None faz o código calcular automaticamente o número máximo possível
                regression.train_models(X_reg, y_reg, use_pca=True, n_components=None)
                
                # Seleciona o melhor modelo baseado em R²
                regression.get_best_model()
                st.session_state.regression = regression
                
                # Pré-processa dados para modelos de classificação
                # Similar à regressão, mas mantém Relay_On como variável alvo
                X_clf, y_clf, features_clf = loader.preprocess_for_classification()
                
                # Verifica se há pelo menos 2 classes antes de treinar modelos de classificação
                # Isso evita erros quando os dados filtrados têm apenas uma classe
                unique_classes = y_clf.nunique() if hasattr(y_clf, 'nunique') else len(pd.Series(y_clf).unique())
                if unique_classes < 2:
                    st.sidebar.warning(
                        f"⚠️ Os dados filtrados para '{cultura_selecionada}' contêm apenas uma classe "
                        f"(Relay_On = {y_clf.iloc[0] if len(y_clf) > 0 else 'N/A'}). "
                        f"Modelos de classificação não podem ser treinados. "
                        f"Tente selecionar outra cultura ou usar dados sem filtro."
                    )
                    # Cria instância vazia para evitar erros nas abas
                    classification = Phase2Classification()
                    st.session_state.classification = classification
                else:
                    # Inicializa e treina modelos de classificação
                    classification = Phase2Classification()
                    classification.initialize_models()
                    classification.train_models(X_clf, y_clf)
                    classification.get_best_model()
                    st.session_state.classification = classification
                
                # Inicializa API meteorológica
                # Pode usar API real (se configurada) ou dados simulados
                weather_api = WeatherAPI()
                st.session_state.weather_api = weather_api
                
                # Inicializa sistema de recomendações
                # Combina modelos de ML com dados meteorológicos
                recommendations = IrrigationRecommendations(
                    regression, classification, weather_api
                )
                st.session_state.recommendations = recommendations
                
                # Marca dados como carregados para habilitar abas
                st.session_state.data_loaded = True
                st.sidebar.success("Dados carregados com sucesso!")
                st.rerun()
            else:
                st.sidebar.error("Erro ao carregar dados")
        
        except Exception as e:
            st.sidebar.error(f"Erro: {str(e)}")
            st.exception(e)

# Texto informativo abaixo do botão (sempre visível)
st.sidebar.caption(
    "💡 Não tem dados próprios? O sistema possui dados de teste. "
    "Basta clicar em 'Carregar Dados' para usar os dados de exemplo."
)

# ============================================================================
# ABAS PRINCIPAIS DO DASHBOARD
# ============================================================================
# O dashboard é dividido em 5 abas que aparecem apenas após carregar os dados
# Cada aba tem um propósito específico e usa os dados/modelos carregados

if st.session_state.data_loaded:
    # Cria as 5 abas principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Resumo", 
        "Análise", 
        "Previsão", 
        "Recomendação",
        "ML"
    ])
    
    # Recupera dados e modelos do estado da sessão
    # Isso evita recarregar a cada interação
    df = st.session_state.df
    regression = st.session_state.regression
    classification = st.session_state.classification
    
    # ============================================================================
    # ABA 1: RESUMO GERAL
    # ============================================================================
    # Esta aba fornece uma visão geral rápida dos dados carregados
    # Inclui métricas principais, séries temporais e importância de variáveis
    
    with tab1:
        # Título removido - a aba já identifica o conteúdo
        
        # Exibe métricas principais em 4 colunas
        # Métricas dão uma visão rápida do estado dos dados
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Registros", len(df))
        
        with col2:
            if "Umidade do Solo" in df.columns:
                umidade_media = df["Umidade do Solo"].mean()
                st.metric("Umidade Média", f"{umidade_media:.1f}%")
        
        with col3:
            if "Temperatura" in df.columns:
                temp_media = df["Temperatura"].mean()
                st.metric("Temperatura Média", f"{temp_media:.1f}°C")
        
        with col4:
            if "PH" in df.columns:
                ph_medio = df["PH"].mean()
                st.metric("PH Médio", f"{ph_medio:.2f}")
        
        st.markdown("---")
        
        # Gráficos de séries temporais
        # Mostram a evolução das variáveis ao longo do tempo
        st.subheader("Evolução Temporal")
        
        if "Data" in df.columns and "Hora" in df.columns:
            # Converte colunas de data e hora para formato datetime
            df["Data"] = pd.to_datetime(df["Data"])
            df["DataHora"] = pd.to_datetime(df["Data"].astype(str) + " " + df["Hora"].astype(str))
            df_sorted = df.sort_values("DataHora").copy()
            
            # Agrupa por dia (média diária) para os últimos 30 dias
            # Filtra últimos 30 dias
            if len(df_sorted) > 0:
                data_limite = df_sorted["Data"].max() - pd.Timedelta(days=30)
                df_30_dias = df_sorted[df_sorted["Data"] >= data_limite].copy()
            else:
                df_30_dias = df_sorted.copy()
            
            # Agrupa por dia (média diária)
            df_diario = df_30_dias.groupby("Data").agg({
                "Temperatura": "mean",
                "Umidade do Solo": "mean" if "Umidade do Solo" in df_30_dias.columns else "first",
                "PH": "mean" if "PH" in df_30_dias.columns else "first"
            }).reset_index()
            df_diario = df_diario.sort_values("Data")  # Garante ordem cronológica
            
            # Gráfico de temperatura ao longo do tempo (últimos 30 dias, média diária)
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=df_diario["Data"],
                y=df_diario["Temperatura"],
                mode='lines',
                name="Temperatura Média",
                line=dict(shape='spline', smoothing=1.0, width=2, color='blue')
            ))
            fig_temp.update_layout(
                title="Temperatura",
                xaxis_title="Data",
                yaxis_title="Temperatura (°C)",
                xaxis=dict(rangeslider=dict(visible=True), type="date"),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Gráfico de umidade do solo ao longo do tempo
            if "Umidade do Solo" in df.columns:
                fig_umidade = go.Figure()
                fig_umidade.add_trace(go.Scatter(
                    x=df_diario["Data"],
                    y=df_diario["Umidade do Solo"],
                    mode='lines',
                    name="Umidade Média",
                    line=dict(shape='spline', smoothing=1.0, width=2, color='green')
                ))
                fig_umidade.update_layout(
                    title="Umidade do Solo",
                    xaxis_title="Data",
                    yaxis_title="Umidade (%)",
                    xaxis=dict(rangeslider=dict(visible=True), type="date"),
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_umidade, use_container_width=True)
            
            # Gráfico de PH ao longo do tempo
            if "PH" in df.columns:
                fig_ph = go.Figure()
                fig_ph.add_trace(go.Scatter(
                    x=df_diario["Data"],
                    y=df_diario["PH"],
                    mode='lines',
                    name="PH Médio",
                    line=dict(shape='spline', smoothing=1.0, width=2, color='orange')
                ))
                fig_ph.update_layout(
                    title="PH",
                    xaxis_title="Data",
                    yaxis_title="PH",
                    xaxis=dict(rangeslider=dict(visible=True), type="date"),
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_ph, use_container_width=True)
        
        st.markdown("---")
        
        # Análise de importância das variáveis
        # Mostra quais features são mais importantes para prever umidade
        st.subheader("Importância das Variáveis")
        
        if regression:
            # Obtém importância calculada pelo Random Forest
            importance_df = regression.get_feature_importance()
            
            if importance_df is not None:
                # Gráfico de barras com as 10 variáveis mais importantes
                fig_importance = px.bar(
                    importance_df.head(10),
                    x="Feature",
                    y="Importance_%",
                    title="Top 10 Variáveis Mais Importantes (Random Forest)",
                    labels={"Importance_%": "Importância (%)", "Feature": "Variável"},
                    color="Importance_%",
                    color_continuous_scale="Greens"
                )
                fig_importance.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_importance, use_container_width=True)
                
                # Texto interpretativo explicando as principais variáveis
                st.markdown("### Interpretação")
                top_3 = importance_df.head(3)
                st.write(f"""
                As variáveis que mais explicam a **Umidade do Solo** são:
                
                1. **{top_3.iloc[0]['Feature']}**: {top_3.iloc[0]['Importance_%']:.1f}%
                2. **{top_3.iloc[1]['Feature']}**: {top_3.iloc[1]['Importance_%']:.1f}%
                3. **{top_3.iloc[2]['Feature']}**: {top_3.iloc[2]['Importance_%']:.1f}%
                
                Essas três variáveis juntas explicam aproximadamente 
                **{top_3['Importance_%'].sum():.1f}%** da variação na umidade do solo.
                """)
    
    # ============================================================================
    # ABA 2: ANÁLISE EXPLORATÓRIA
    # ============================================================================
    # Esta aba permite análise interativa dos dados
    # Usuário pode selecionar métricas e ajustar parâmetros de visualização
    
    with tab2:
        # Título removido - a aba já identifica o conteúdo
        
        # Lista de métricas disponíveis para análise
        # Construída dinamicamente baseada nas colunas presentes no dataset
        metricas_disponiveis = []
        if "Temperatura" in df.columns:
            metricas_disponiveis.append("Temperatura")
        if "Umidade do Solo" in df.columns:
            metricas_disponiveis.append("Umidade do Solo")
        if "PH" in df.columns:
            metricas_disponiveis.append("PH")
        
        if metricas_disponiveis:
            # Layout com métrica e slider lado a lado
            col_sel, col_slider = st.columns([2, 2])
            
            with col_sel:
                # Dropdown para seleção da métrica a analisar
                metrica_selecionada = st.selectbox("Selecione a métrica para análise", metricas_disponiveis)
            
            with col_slider:
                # Slider para ajustar tamanho da janela de média móvel
                # Média móvel suaviza a série temporal, facilitando visualização de tendências
                window_size = st.slider("Tamanho da Média Móvel", 1, 50, 7)
            
            # Prepara dados para visualização
            if "Data" in df.columns:
                df["Data"] = pd.to_datetime(df["Data"])
                df_sorted = df.sort_values("Data")  # Garante ordem cronológica
                
                # Agrupa por dia (média diária) para últimos 30 dias
                if len(df_sorted) > 0:
                    data_limite = df_sorted["Data"].max() - pd.Timedelta(days=30)
                    df_30_dias = df_sorted[df_sorted["Data"] >= data_limite].copy()
                else:
                    df_30_dias = df_sorted.copy()
                
                # Agrupa por dia
                df_diario = df_30_dias.groupby("Data")[metrica_selecionada].mean().reset_index()
                df_diario = df_diario.sort_values("Data")  # Garante ordem cronológica
                
                # Calcula média móvel usando rolling window
                df_diario[f"{metrica_selecionada}_MA"] = df_diario[metrica_selecionada].rolling(window=window_size).mean()
                
                # Cria gráfico de série temporal com Plotly
                fig = go.Figure()
                
                # Adiciona linha com valores originais (suavizada)
                fig.add_trace(go.Scatter(
                    x=df_diario["Data"],
                    y=df_diario[metrica_selecionada],
                    mode='lines',
                    name=metrica_selecionada,
                    line=dict(shape='spline', smoothing=1.0, color='blue', width=1)
                ))
                
                # Adiciona linha com média móvel (suavizada)
                fig.add_trace(go.Scatter(
                    x=df_diario["Data"],
                    y=df_diario[f"{metrica_selecionada}_MA"],
                    mode='lines',
                    name=f"Média Móvel ({window_size})",
                    line=dict(shape='spline', smoothing=1.0, color='red', width=2)
                ))
                
                fig.update_layout(
                    title=metrica_selecionada,
                    xaxis_title="Data",
                    yaxis_title=metrica_selecionada,
                    hovermode='x unified',
                    xaxis=dict(rangeslider=dict(visible=True), type="date"),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Estatísticas descritivas da métrica selecionada (depois da série temporal)
                st.markdown("---")
                st.subheader("Estatísticas")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Média", f"{df[metrica_selecionada].mean():.2f}")
                with col2:
                    st.metric("Mediana", f"{df[metrica_selecionada].median():.2f}")
                with col3:
                    st.metric("Desvio Padrão", f"{df[metrica_selecionada].std():.2f}")
                with col4:
                    st.metric("Mínimo", f"{df[metrica_selecionada].min():.2f}")
                with col5:
                    st.metric("Máximo", f"{df[metrica_selecionada].max():.2f}")
                
                # Histograma mostrando distribuição da métrica
                st.markdown("---")
                st.subheader("Distribuição")
                fig_hist = px.histogram(
                    df,
                    x=metrica_selecionada,
                    nbins=30,
                    title=None,
                    labels={metrica_selecionada: metrica_selecionada}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
    
    # ============================================================================
    # ABA 3: PREVISÃO DE UMIDADE
    # ============================================================================
    # Esta aba permite ao usuário fazer previsões customizadas de umidade
    # Usuário insere valores de features e recebe previsão do modelo
    
    with tab3:
        # Título removido - a aba já identifica o conteúdo
        
        # Campos simplificados para previsão
        col1, col2 = st.columns(2)
        
        with col1:
            cultura_input = st.selectbox("Cultura", culturas, index=culturas.index(cultura_selecionada))
            temperatura_input = st.number_input("Temperatura (°C)", value=25.0, min_value=0.0, max_value=50.0, step=0.1)
            chuva_real_input = st.number_input("Chuva Real (mm)", value=0.0, min_value=0.0, max_value=100.0, step=0.1)
        
        with col2:
            umidade_ar_input = st.number_input("Umidade do Ar (%)", value=60.0, min_value=0.0, max_value=100.0, step=0.1)
            hora_input = st.number_input("Hora do Dia", value=12, min_value=0, max_value=23, step=1)
        
        # Botão para executar a previsão
        st.markdown("---")
        if st.button("Prever Umidade", type="primary", use_container_width=True):
            
            # Verifica se o modelo está disponível no session_state
            if st.session_state.regression and st.session_state.regression.best_model is not None:
                regression = st.session_state.regression
                
                try:
                    # Obtém os nomes das features do modelo treinado
                    # Isso garante que criamos o DataFrame com as mesmas colunas usadas no treinamento
                    if regression.feature_names is None and hasattr(st.session_state, 'loader'):
                        # Se não temos feature_names, precisamos recriar o pré-processamento
                        X_temp, _, _ = st.session_state.loader.preprocess_for_regression()
                        feature_names = X_temp.columns.tolist()
                    else:
                        feature_names = regression.feature_names
                    
                    if feature_names is None:
                        raise ValueError("Não foi possível determinar as features do modelo. Carregue os dados novamente.")
                    
                    # Obtém valores médios do dataset para features não fornecidas
                    # Isso permite fazer previsões mesmo sem todos os parâmetros
                    df_temp = st.session_state.df.copy() if st.session_state.df is not None else None
                    
                    # Cria dicionário inicial vazio com todas as features do modelo
                    # Todas começam com 0 (padrão)
                    features_dict = {feat: 0 for feat in feature_names}
                    
                    # Preenche features fornecidas pelo usuário
                    if "Temperatura" in feature_names:
                        features_dict["Temperatura"] = temperatura_input
                    if "Chuva Real (mm)" in feature_names:
                        features_dict["Chuva Real (mm)"] = chuva_real_input
                    if "Umidade do Ar" in feature_names:
                        features_dict["Umidade do Ar"] = umidade_ar_input
                    if "Hora" in feature_names:
                        features_dict["Hora"] = hora_input
                    
                    # Preenche features não fornecidas com valores médios do dataset
                    if df_temp is not None:
                        if "PH" in feature_names and "PH" in df_temp.columns:
                            features_dict["PH"] = df_temp["PH"].mean()
                        if "Nível de Nitrogênio" in feature_names and "Nível de Nitrogênio" in df_temp.columns:
                            features_dict["Nível de Nitrogênio"] = df_temp["Nível de Nitrogênio"].mean()
                        if "Nível de Fósforo" in feature_names and "Nível de Fósforo" in df_temp.columns:
                            features_dict["Nível de Fósforo"] = df_temp["Nível de Fósforo"].mean()
                        if "Nível de Potássio" in feature_names and "Nível de Potássio" in df_temp.columns:
                            features_dict["Nível de Potássio"] = df_temp["Nível de Potássio"].mean()
                        if "Probabilidade de Chuva" in feature_names and "Probabilidade de Chuva" in df_temp.columns:
                            features_dict["Probabilidade de Chuva"] = df_temp["Probabilidade de Chuva"].mean()
                    
                    # Adiciona one-hot encoding para Cultura
                    # Procura por colunas que começam com "Cultura_"
                    for feat in feature_names:
                        if feat.startswith("Cultura_"):
                            cultura_feat = feat.replace("Cultura_", "")
                            features_dict[feat] = 1 if cultura_feat == cultura_input else 0
                    
                    # Adiciona one-hot encoding para Estágio Fenológico
                    # Usa o estágio mais comum da cultura selecionada como padrão
                    estagios = config.ESTAGIOS_POR_CULTURA.get(cultura_input, ["Vegetativo"])
                    estagio_padrao = estagios[len(estagios) // 2]  # Estágio do meio como padrão
                    for feat in feature_names:
                        if feat.startswith("Estagio_"):
                            estagio_feat = feat.replace("Estagio_", "")
                            features_dict[feat] = 1 if estagio_feat == estagio_padrao else 0
                    
                    # Cria DataFrame na ordem exata das features do modelo
                    features_ordered = {feat: features_dict[feat] for feat in feature_names}
                    X_input = pd.DataFrame([features_ordered])
                    
                    # Faz previsão usando o melhor modelo treinado
                    umidade_prevista = regression.predict(X_input)[0]
                    
                    # Exibe resultado da previsão
                    col_result1, col_result2 = st.columns(2)
                    with col_result1:
                        st.metric("Umidade do Solo Prevista", f"{umidade_prevista:.2f}%")
                    
                    # Lógica para determinar se precisa irrigar
                    # Baseado na umidade prevista, temperatura, chuva e umidade do ar
                    precisa_irrigar = False
                    motivo_irrigacao = ""
                    
                    # Regras de decisão para irrigação
                    if umidade_prevista < 20:
                        precisa_irrigar = True
                        motivo_irrigacao = "Umidade crítica (< 20%). Risco de estresse hídrico."
                    elif umidade_prevista < 30:
                        # Se umidade está baixa e não há chuva prevista, deve irrigar
                        if chuva_real_input == 0 and umidade_ar_input < 50:
                            precisa_irrigar = True
                            motivo_irrigacao = "Umidade abaixo do ideal (< 30%) e condições secas."
                        else:
                            precisa_irrigar = False
                            motivo_irrigacao = "Umidade abaixo do ideal, mas condições ambientais podem compensar."
                    else:
                        precisa_irrigar = False
                        motivo_irrigacao = "Umidade adequada. Irrigação não necessária no momento."
                    
                    # Considerações adicionais baseadas em temperatura e umidade do ar
                    if temperatura_input > 35 and umidade_ar_input < 40:
                        # Temperatura muito alta e ar seco aumenta necessidade de irrigação
                        if not precisa_irrigar and umidade_prevista < 35:
                            precisa_irrigar = True
                            motivo_irrigacao = "Condições de alta temperatura e baixa umidade do ar aumentam a demanda hídrica."
                    
                    # Exibe recomendação de irrigação
                    with col_result2:
                        if precisa_irrigar:
                            st.metric("Recomendação", "IRRIGAR", delta="Necessário")
                        else:
                            st.metric("Recomendação", "NÃO IRRIGAR", delta="Adequado")
                    
                    # Exibe motivo da recomendação
                    st.markdown("---")
                    st.markdown("### Análise da Recomendação")
                    if precisa_irrigar:
                        st.warning(f"**Irrigação Recomendada:** {motivo_irrigacao}")
                        st.info(
                            f"**Condições atuais:**\n"
                            f"- Umidade do Solo: {umidade_prevista:.1f}%\n"
                            f"- Temperatura: {temperatura_input:.1f}°C\n"
                            f"- Chuva: {chuva_real_input:.1f}mm\n"
                            f"- Umidade do Ar: {umidade_ar_input:.1f}%"
                        )
                    else:
                        st.success(f"**Irrigação Não Necessária:** {motivo_irrigacao}")
                        st.info(
                            f"**Condições atuais:**\n"
                            f"- Umidade do Solo: {umidade_prevista:.1f}%\n"
                            f"- Temperatura: {temperatura_input:.1f}°C\n"
                            f"- Chuva: {chuva_real_input:.1f}mm\n"
                            f"- Umidade do Ar: {umidade_ar_input:.1f}%"
                        )
                
                except Exception as e:
                    st.error(f"Erro ao fazer previsão: {str(e)}")
                    st.exception(e)
            else:
                st.error("Modelo não disponível. Carregue os dados primeiro.")
    
    # ============================================================================
    # ABA 4: RECOMENDAÇÕES DE IRRIGAÇÃO
    # ============================================================================
    # Esta aba gera cronograma automático de irrigação para os próximos 7 dias
    # Combina previsões meteorológicas com modelos de ML e regras de negócio
    
    with tab4:
        # Título removido - a aba já identifica o conteúdo
        
        # Explicação sobre a base das recomendações
        st.info(
            f"Recomendações baseadas na previsão meteorológica de **{municipio_selecionado}** "
            f"para a cultura **{cultura_selecionada}**. O sistema combina dados meteorológicos "
            f"com modelos de machine learning para gerar um cronograma de irrigação para os próximos 7 dias."
        )
        
        # Mapa do município (usando coordenadas)
        # Obtém previsão do tempo para exibir % de chuva no mapa
        if st.session_state.weather_api:
            coords = st.session_state.weather_api.get_city_coordinates(municipio_selecionado)
            if coords:
                # Obtém previsão do tempo para os próximos 7 dias
                weather_df = st.session_state.weather_api.get_weather_forecast(municipio_selecionado, days=7)
                
                # Título discreto e pequeno
                st.markdown(f"<p style='font-size: 0.75em; color: #888; margin-bottom: 0.3rem; margin-top: 0;'>Localização: {municipio_selecionado}</p>", unsafe_allow_html=True)
                
                # Mapa do município
                map_data = pd.DataFrame({
                    "lat": [coords[0]],
                    "lon": [coords[1]]
                })
                st.map(map_data, zoom=10)
                
                # Informações de chuva para os próximos 7 dias (abaixo do mapa)
                if weather_df is not None and len(weather_df) > 0:
                    st.markdown("**Previsão de Chuva (Próximos 7 dias):**")
                    
                    # Cria grid de 7 colunas para os dias
                    cols_chuva = st.columns(7)
                    for idx, (col, (_, row)) in enumerate(zip(cols_chuva, weather_df.iterrows())):
                        with col:
                            prob_chuva = row.get("probabilidade_chuva", 0)
                            # Ícone baseado na probabilidade
                            if prob_chuva > 70:
                                icon = "🌧️"
                            elif prob_chuva > 50:
                                icon = "🌦️"
                            elif prob_chuva > 30:
                                icon = "⛅"
                            else:
                                icon = "☀️"
                            
                            # Formata data
                            try:
                                data_formatada = pd.to_datetime(row["data"]).strftime("%d/%m")
                            except:
                                data_formatada = row["data"]
                            
                            # Exibe de forma compacta com fundo
                            st.markdown(f"<div style='text-align: center; padding: 0.4rem; background-color: #f8f9fa; border-radius: 0.4rem; margin-bottom: 0.3rem;'>", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-size: 1.8em; line-height: 1;'>{icon}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-size: 0.75em; font-weight: bold; margin-top: 0.2rem;'>{data_formatada}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-size: 0.85em; color: #2c3e50;'>{prob_chuva:.0f}%</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Botão para gerar recomendações
        if st.button("Gerar Recomendações para 7 Dias", type="primary"):
            if st.session_state.recommendations:
                with st.spinner(f"Consultando previsão do tempo para {municipio_selecionado} e gerando recomendações..."):
                    # Gera recomendações usando o sistema integrado
                    rec_df = st.session_state.recommendations.generate_recommendations(
                        municipio_selecionado, cultura_selecionada, days=7
                    )
                    
                    if rec_df is not None and len(rec_df) > 0:
                        st.markdown("---")
                        st.subheader("Cronograma (7 dias)")
                        
                        # Remove coluna justificativa da tabela
                        rec_df_display = rec_df.drop(columns=["justificativa"], errors="ignore")
                        
                        # Exibe tabela com todas as recomendações
                        st.dataframe(rec_df_display, use_container_width=True, hide_index=True)
                        
                        # Gráfico de umidade prevista para os próximos 7 dias (linha suavizada)
                        # Converte data para datetime para garantir ordem cronológica
                        rec_df_plot = rec_df.copy()
                        
                        # Garante que a coluna 'data' seja convertida para datetime
                        # Se já for datetime, mantém; se for string, converte
                        if rec_df_plot["data"].dtype == 'object':
                            rec_df_plot["data_dt"] = pd.to_datetime(rec_df_plot["data"], errors='coerce')
                        else:
                            rec_df_plot["data_dt"] = pd.to_datetime(rec_df_plot["data"], errors='coerce')
                        
                        # Remove linhas com datas inválidas
                        rec_df_plot = rec_df_plot.dropna(subset=['data_dt'])
                        rec_df_plot = rec_df_plot.sort_values("data_dt")  # Garante ordem cronológica
                        
                        # Garante que umidade_prevista seja numérico
                        rec_df_plot["umidade_prevista"] = pd.to_numeric(rec_df_plot["umidade_prevista"], errors='coerce')
                        rec_df_plot = rec_df_plot.dropna(subset=['umidade_prevista'])
                        
                        if len(rec_df_plot) > 0:
                            fig_umidade = go.Figure()
                            fig_umidade.add_trace(go.Scatter(
                                x=rec_df_plot["data_dt"],
                                y=rec_df_plot["umidade_prevista"],
                                mode='lines+markers',
                                name="Umidade Prevista",
                                line=dict(shape='spline', smoothing=1.0, width=2, color='green')
                            ))
                            # Adiciona linhas de referência (níveis ideal e crítico)
                            fig_umidade.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Ideal (30%)")
                            fig_umidade.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Crítico (20%)")
                            fig_umidade.update_layout(
                                title="Umidade Prevista",
                                xaxis_title="Data",
                                yaxis_title="Umidade (%)",
                                xaxis=dict(type="date"),
                                showlegend=False
                            )
                            st.plotly_chart(fig_umidade, use_container_width=True)
                        else:
                            st.warning("Não foi possível gerar o gráfico de umidade prevista. Verifique os dados.")
                        
                        # Detalhes expandíveis para cada dia
                        st.markdown("---")
                        st.subheader("Análise Detalhada")
                        
                        for idx, row in rec_df.iterrows():
                            # Define cor e ícone baseado na recomendação
                            if row['deve_irrigar']:
                                status_icon = "✅"
                                status_color = "green"
                                status_text = "IRRIGAR"
                            else:
                                status_icon = "⏸️"
                                status_color = "orange"
                                status_text = "NÃO IRRIGAR"
                            
                            with st.expander(f"{status_icon} {row['dia_semana']} - {row['data']} | {status_text}"):
                                # Explicação didática da recomendação
                                st.markdown("### Análise da Recomendação")
                                
                                # Análise da umidade
                                if row['umidade_prevista'] < 20:
                                    st.warning(
                                        f"**Umidade Crítica:** A umidade prevista é de {row['umidade_prevista']:.1f}%, "
                                        f"que está abaixo do nível crítico (20%). Isso indica risco de estresse hídrico "
                                        f"para a cultura {cultura_selecionada}."
                                    )
                                elif row['umidade_prevista'] < 30:
                                    st.info(
                                        f"**Umidade Abaixo do Ideal:** A umidade prevista é de {row['umidade_prevista']:.1f}%, "
                                        f"que está abaixo do ideal (30%). A cultura pode se beneficiar de irrigação suplementar."
                                    )
                                else:
                                    st.success(
                                        f"**Umidade Adequada:** A umidade prevista é de {row['umidade_prevista']:.1f}%, "
                                        f"que está dentro do nível adequado para a cultura {cultura_selecionada}."
                                    )
                                
                                # Análise da chuva
                                if row['probabilidade_chuva'] > 70:
                                    st.info(
                                        f"**Alta Probabilidade de Chuva:** A previsão indica {row['probabilidade_chuva']:.1f}% "
                                        f"de chance de chuva, com volume previsto de {row['chuva_prevista_mm']:.1f}mm. "
                                        f"Esta chuva deve suprir a necessidade hídrica da cultura."
                                    )
                                elif row['probabilidade_chuva'] > 50:
                                    st.warning(
                                        f"**Probabilidade Moderada de Chuva:** A previsão indica {row['probabilidade_chuva']:.1f}% "
                                        f"de chance de chuva. Monitore as condições e ajuste conforme necessário."
                                    )
                                else:
                                    st.info(
                                        f"**Baixa Probabilidade de Chuva:** A previsão indica apenas {row['probabilidade_chuva']:.1f}% "
                                        f"de chance de chuva. A irrigação pode ser necessária se a umidade estiver baixa."
                                    )
                                
                                # Horário recomendado (se aplicável)
                                if row['deve_irrigar'] and row.get('horario_recomendado'):
                                    st.info(
                                        f"**Horário Recomendado:** {row['horario_recomendado']} - "
                                        f"Este horário oferece melhor eficiência de irrigação, com menor evaporação "
                                        f"e melhor aproveitamento da água."
                                    )
            else:
                st.error("Sistema de recomendações não disponível.")
    
    # ============================================================================
    # ABA 5: ANÁLISE TÉCNICA DE MACHINE LEARNING
    # ============================================================================
    # Esta aba mostra análise detalhada dos modelos treinados
    # Inclui comparação de métricas, gráficos de desempenho e análise PCA
    
    with tab5:
        # Título removido - a aba já identifica o conteúdo
        
        # Seção de modelos de regressão
        st.subheader("Regressão")
        
        if regression and regression.results:
            # Cria tabela comparativa com métricas de todos os modelos
            results_df = pd.DataFrame(regression.results).T
            results_df = results_df[["MAE_test", "MSE_test", "RMSE_test", "R2_test"]]
            results_df.columns = ["MAE", "MSE", "RMSE", "R²"]
            results_df = results_df.round(4)
            
            st.markdown("### Comparação")
            st.dataframe(results_df, use_container_width=True)
            
            # Gráfico de barras comparando R² de todos os modelos
            fig_r2 = px.bar(
                x=results_df.index,
                y=results_df["R²"],
                title=None,
                labels={"x": "Modelo", "y": "R² Score"},
                color=results_df["R²"],
                color_continuous_scale="Greens"
            )
            fig_r2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_r2, use_container_width=True)
            
            # Identifica e exibe o melhor modelo
            best_name, _ = regression.get_best_model()
            st.success(f"Melhor Modelo: **{best_name}** (R² = {results_df.loc[best_name, 'R²']:.4f})")
            
            # Gráfico de dispersão: valores reais vs valores previstos
            # Pontos próximos à linha diagonal indicam boas previsões
            if best_name in regression.trained_models or best_name in regression.trained_models_pca:
                model_data = regression.trained_models.get(best_name) or regression.trained_models_pca.get(best_name)
                if model_data and "y_test" in model_data and "y_pred" in model_data:
                    fig_scatter = px.scatter(
                        x=model_data["y_test"],
                        y=model_data["y_pred"],
                        title=None,
                        labels={"x": "Valor Real", "y": "Valor Previsto"}
                    )
                    # Adiciona linha ideal (y = x)
                    fig_scatter.add_trace(go.Scatter(
                        x=[model_data["y_test"].min(), model_data["y_test"].max()],
                        y=[model_data["y_test"].min(), model_data["y_test"].max()],
                        mode='lines',
                        name='Linha Ideal',
                        line=dict(dash='dash', color='red')
                    ))
                    st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Análise PCA (se foi aplicado)
            st.markdown("---")
            st.subheader("Análise de Componentes Principais (PCA)")
            
            pca_info = regression.get_pca_info()
            if pca_info:
                # Scree plot: mostra variância explicada por cada componente (linha suavizada)
                explained_var = pca_info["explained_variance_ratio"]
                fig_scree = go.Figure()
                fig_scree.add_trace(go.Scatter(
                    x=list(range(1, len(explained_var) + 1)),
                    y=explained_var * 100,
                    mode='lines+markers',
                    name="Variância Explicada",
                    line=dict(shape='spline', smoothing=1.0, width=2, color='blue')
                ))
                fig_scree.update_layout(
                    title=None,
                    xaxis_title="Componente Principal",
                    yaxis_title="Variância Explicada (%)"
                )
                st.plotly_chart(fig_scree, use_container_width=True)
                
                # Loadings plot: mostra correlação entre features originais e componentes
                # Filtra apenas features relacionadas à cultura selecionada
                if len(pca_info["components"]) >= 2:
                    feature_names = pca_info["feature_names"]
                    if feature_names:
                        # Filtra features relacionadas à cultura selecionada
                        # Mantém apenas features da cultura selecionada e features numéricas gerais
                        cultura_prefix = f"Cultura_{cultura_selecionada}"
                        features_filtradas = []
                        indices_filtrados = []
                        
                        for i, feat in enumerate(feature_names):
                            # Inclui se:
                            # 1. É da cultura selecionada (Cultura_SOJA, Cultura_MILHO, etc)
                            # 2. Não é feature de cultura (features numéricas gerais)
                            # 3. Não é feature de estágio (para simplificar)
                            if (feat == cultura_prefix or 
                                (not feat.startswith("Cultura_") and not feat.startswith("Estagio_"))):
                                features_filtradas.append(feat)
                                indices_filtrados.append(i)
                        
                        # Se não encontrou features, usa todas (fallback)
                        if not indices_filtrados:
                            indices_filtrados = list(range(min(len(feature_names), len(pca_info["components"][0]))))
                            features_filtradas = feature_names[:len(indices_filtrados)]
                        
                        # Filtra loadings baseado nos índices
                        if len(indices_filtrados) > 0:
                            try:
                                # Extrai apenas os componentes das features filtradas
                                loadings_filtrados = pca_info["components"][:2][:, indices_filtrados].T
                                
                                loadings_df = pd.DataFrame(
                                    loadings_filtrados,
                                    columns=["PC1", "PC2"],
                                    index=features_filtradas[:len(loadings_filtrados)]
                                )
                            except:
                                # Fallback: usa todas as features
                                loadings_df = pd.DataFrame(
                                    pca_info["components"][:2].T,
                                    columns=["PC1", "PC2"],
                                    index=feature_names[:len(pca_info["components"][0])]
                                )
                        else:
                            # Fallback: usa todas as features
                            loadings_df = pd.DataFrame(
                                pca_info["components"][:2].T,
                                columns=["PC1", "PC2"],
                                index=feature_names[:len(pca_info["components"][0])]
                            )
                    else:
                        loadings_df = pd.DataFrame(
                            pca_info["components"][:2].T,
                            columns=["PC1", "PC2"]
                        )
                    
                    fig_loadings = px.scatter(
                        loadings_df,
                        x="PC1",
                        y="PC2",
                        text=loadings_df.index if loadings_df.index is not None else None,
                        title=None,
                        labels={"PC1": "PC1", "PC2": "PC2"}
                    )
                    fig_loadings.update_traces(textposition="top center")
                    st.plotly_chart(fig_loadings, use_container_width=True)
        
        # Seção de modelos de classificação
        st.markdown("---")
        st.subheader("Modelos de Classificação")
        
        if classification and classification.results:
            # Tabela comparativa com métricas de classificação
            clf_results_df = pd.DataFrame(classification.results).T
            clf_results_df = clf_results_df[["Accuracy_test", "Precision_test", "Recall_test", "F1_test"]]
            clf_results_df.columns = ["Acurácia", "Precisão", "Recall", "F1-Score"]
            clf_results_df = clf_results_df.round(4)
            
            st.markdown("### Comparação de Modelos")
            st.dataframe(clf_results_df, use_container_width=True)
            
            # Gráfico de barras comparando F1-Score
            fig_f1 = px.bar(
                x=clf_results_df.index,
                y=clf_results_df["F1-Score"],
                title="F1-Score por Modelo",
                labels={"x": "Modelo", "y": "F1-Score"},
                color=clf_results_df["F1-Score"],
                color_continuous_scale="Blues"
            )
            fig_f1.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_f1, use_container_width=True)
            
            # Identifica e exibe o melhor modelo
            best_clf_name, _ = classification.get_best_model()
            st.success(f"Melhor Modelo: **{best_clf_name}** (F1 = {clf_results_df.loc[best_clf_name, 'F1-Score']:.4f})")
            
            # Matriz de confusão do melhor modelo
            # Mostra quantas previsões foram corretas/incorretas
            if best_clf_name in classification.models:
                model_data = classification.models[best_clf_name]
                if "Confusion_Matrix" in model_data["metrics"]:
                    cm = model_data["metrics"]["Confusion_Matrix"]
                    fig_cm = px.imshow(
                        cm,
                        labels=dict(x="Previsto", y="Real", color="Quantidade"),
                        x=["Não Irrigar", "Irrigar"],
                        y=["Não Irrigar", "Irrigar"],
                        title=f"Matriz de Confusão - {best_clf_name}",
                        color_continuous_scale="Blues"
                    )
                    st.plotly_chart(fig_cm, use_container_width=True)

else:
    # Mensagem exibida quando os dados ainda não foram carregados
    st.info("Por favor, configure as opções no menu lateral e clique em 'Carregar Dados' para começar.")

# ============================================================================
# RODAPÉ DO DASHBOARD
# ============================================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Sistema Inteligente de Manejo Agrícola - Desenvolvido com Streamlit e Scikit-Learn"
    "</div>",
    unsafe_allow_html=True
)
