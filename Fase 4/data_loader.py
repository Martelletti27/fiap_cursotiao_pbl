"""
Módulo de Carregamento e Pré-processamento de Dados

Este módulo é responsável por carregar o dataset CSV e prepará-lo para os modelos
de machine learning. Realiza transformações como one-hot encoding de variáveis
categóricas, normalização de datas e remoção de valores ausentes. O pré-processamento
é específico para cada tipo de modelo (regressão ou classificação) devido às
diferenças nas variáveis alvo e features necessárias.
"""
import pandas as pd
import numpy as np
import os
import config

class DataLoader:
    """
    Classe responsável pelo carregamento e pré-processamento de dados.
    
    Esta classe encapsula toda a lógica de leitura de arquivos CSV e transformação
    dos dados brutos em formatos adequados para treinamento de modelos. Mantém
    o estado dos dados carregados para evitar recarregamentos desnecessários.
    """
    
    def __init__(self):
        """
        Inicializa o carregador de dados.
        
        Atributos:
        - df: DataFrame pandas com os dados carregados (None até o carregamento)
        - preprocessor: Pipeline de pré-processamento (reservado para uso futuro)
        - label_encoders: Dicionário de encoders para variáveis categóricas
        """
        self.df = None
        self.preprocessor = None
        self.label_encoders = {}
    
    def load_data(self, file_path=None):
        """
        Carrega o dataset CSV do arquivo especificado ou do caminho padrão.
        
        O método primeiro tenta carregar do caminho fornecido. Se nenhum caminho
        for especificado, usa o arquivo padrão definido em config.DATA_FILE.
        Trata erros de arquivo não encontrado e outros erros de leitura.
        
        Args:
            file_path: Caminho opcional para o arquivo CSV. Se None, usa config.DATA_FILE.
        
        Returns:
            DataFrame pandas com os dados carregados ou None em caso de erro.
        """
        if file_path is None:
            file_path = config.DATA_FILE
        
        try:
            # Carrega o CSV usando pandas, que detecta automaticamente separadores e encoding
            self.df = pd.read_csv(file_path)
            print(f"Dados carregados: {len(self.df)} registros")
            return self.df
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {file_path}")
            return None
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None
    
    def preprocess_for_regression(self):
        """
        Pré-processa dados para modelos de regressão (FASE 1).
        
        Este método prepara os dados para prever a umidade do solo. As transformações
        incluem: conversão de datas, one-hot encoding de variáveis categóricas (Cultura
        e Estágio Fenológico), remoção de colunas não utilizadas e separação entre
        features (X) e variável alvo (y). Remove também registros com valores ausentes.
        
        O one-hot encoding cria colunas binárias para cada categoria, permitindo que
        modelos lineares capturem efeitos diferentes para cada cultura e estágio.
        
        Returns:
            Tupla (X, y, feature_cols):
            - X: DataFrame com features numéricas e codificadas
            - y: Series com a variável alvo (Umidade do Solo)
            - feature_cols: Lista com nomes das colunas de features
        
        Raises:
            ValueError: Se os dados não foram carregados ou se a coluna alvo não existe.
        """
        if self.df is None:
            raise ValueError("Dados não carregados. Execute load_data() primeiro.")
        
        # Cria cópia para não modificar o DataFrame original
        df = self.df.copy()
        
        # Remove colunas de data e hora ANTES do one-hot encoding
        # Isso evita conflitos de tipo de dados (datetime não pode ser misturado com numéricos)
        # Essas colunas não são usadas diretamente como features, apenas para ordenação
        cols_to_remove_early = ["ID", "Data", "Hora", "Status de Irrigação", "Relay_On"]
        cols_to_remove_early = [c for c in cols_to_remove_early if c in df.columns]
        df = df.drop(columns=cols_to_remove_early, errors="ignore")
        
        # One-hot encoding para Cultura
        # Transforma uma coluna categórica em múltiplas colunas binárias
        # Exemplo: Cultura "SOJA" vira coluna "Cultura_SOJA" com valor 1
        # IMPORTANTE: Fazer isso ANTES de converter outras colunas para evitar conflitos de tipo
        if "Cultura" in df.columns:
            df = pd.get_dummies(df, columns=["Cultura"], prefix="Cultura")
        
        # One-hot encoding para Estágio Fenológico
        # Cada estágio vira uma coluna binária separada
        if "Estágio Fenológico" in df.columns:
            df = pd.get_dummies(df, columns=["Estágio Fenológico"], prefix="Estagio")
        
        # Separa features (X) e variável alvo (y)
        target = config.REGRESSION_TARGET
        if target not in df.columns:
            raise ValueError(f"Coluna alvo '{target}' não encontrada")
        
        # Todas as colunas exceto a variável alvo são features
        feature_cols = [c for c in df.columns if c != target]
        X = df[feature_cols].copy()
        y = df[target].copy()
        
        # Remove qualquer coluna que ainda seja do tipo datetime ou object (strings de data)
        # Isso garante que apenas colunas numéricas e one-hot encoded sejam mantidas
        cols_to_drop = []
        for col in X.columns:
            # Verifica se é datetime
            if pd.api.types.is_datetime64_any_dtype(X[col]):
                cols_to_drop.append(col)
            # Verifica se é object (string) e parece ser data
            elif X[col].dtype == 'object':
                # Tenta converter para datetime - se conseguir, é uma data
                try:
                    pd.to_datetime(X[col].iloc[0], errors='raise')
                    cols_to_drop.append(col)
                except:
                    pass  # Não é data, mantém a coluna
        
        if cols_to_drop:
            X = X.drop(columns=cols_to_drop, errors="ignore")
            feature_cols = [c for c in feature_cols if c not in cols_to_drop]
        
        # Converte todas as colunas restantes para numérico (garante que one-hot encoding seja numérico)
        # Isso é crítico porque o StandardScaler precisa de dados numéricos
        for col in X.columns:
            if X[col].dtype == 'object':
                # Se ainda for object, tenta converter para numérico
                X[col] = pd.to_numeric(X[col], errors='coerce')
            elif pd.api.types.is_datetime64_any_dtype(X[col]):
                # Se for datetime, remove (não deve chegar aqui, mas por segurança)
                X = X.drop(columns=[col], errors="ignore")
                feature_cols = [c for c in feature_cols if c != col]
        
        # Verificação final: garante que todas as colunas são numéricas
        # Remove qualquer coluna que não seja numérica
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < len(X.columns):
            non_numeric = [c for c in X.columns if c not in numeric_cols]
            X = X[numeric_cols]
            feature_cols = [c for c in feature_cols if c in numeric_cols]
        
        # Remove registros com valores ausentes (NaN)
        # Cria máscara booleana: True para linhas sem NaN, False para linhas com NaN
        mask = ~(X.isna().any(axis=1) | y.isna())
        X = X[mask]
        y = y[mask]
        
        return X, y, feature_cols
    
    def preprocess_for_classification(self):
        """
        Pré-processa dados para modelos de classificação (FASE 2).
        
        Similar ao método de regressão, mas mantém a coluna Relay_On como variável
        alvo ao invés de removê-la. O pré-processamento é quase idêntico, mas as
        colunas removidas são diferentes pois Relay_On é necessário para classificação.
        
        Returns:
            Tupla (X, y, feature_cols):
            - X: DataFrame com features
            - y: Series com a variável alvo (Relay_On: 0 ou 1)
            - feature_cols: Lista com nomes das colunas de features
        
        Raises:
            ValueError: Se os dados não foram carregados ou se a coluna alvo não existe.
        """
        if self.df is None:
            raise ValueError("Dados não carregados. Execute load_data() primeiro.")
        
        df = self.df.copy()
        
        # Remove colunas de data, hora e outras não utilizadas ANTES do one-hot encoding
        # Isso evita conflitos de tipo de dados (datetime não pode ser misturado com numéricos)
        # Mantém Relay_On pois é a variável alvo da classificação
        cols_to_remove_early = ["ID", "Data", "Hora", "Status de Irrigação"]
        cols_to_remove_early = [c for c in cols_to_remove_early if c in df.columns]
        df = df.drop(columns=cols_to_remove_early, errors="ignore")
        
        # One-hot encoding para Cultura
        # IMPORTANTE: Fazer isso ANTES de converter outras colunas para evitar conflitos de tipo
        if "Cultura" in df.columns:
            df = pd.get_dummies(df, columns=["Cultura"], prefix="Cultura")
        
        # One-hot encoding para Estágio Fenológico
        if "Estágio Fenológico" in df.columns:
            df = pd.get_dummies(df, columns=["Estágio Fenológico"], prefix="Estagio")
        
        # Separa features e variável alvo
        target = config.CLASSIFICATION_TARGET
        if target not in df.columns:
            raise ValueError(f"Coluna alvo '{target}' não encontrada")
        
        feature_cols = [c for c in df.columns if c != target]
        X = df[feature_cols].copy()
        y = df[target].copy()
        
        # Remove qualquer coluna que ainda seja do tipo datetime ou object (strings de data)
        # Isso garante que apenas colunas numéricas e one-hot encoded sejam mantidas
        cols_to_drop = []
        for col in X.columns:
            # Verifica se é datetime
            if pd.api.types.is_datetime64_any_dtype(X[col]):
                cols_to_drop.append(col)
            # Verifica se é object (string) e parece ser data
            elif X[col].dtype == 'object':
                # Tenta converter para datetime - se conseguir, é uma data
                try:
                    pd.to_datetime(X[col].iloc[0], errors='raise')
                    cols_to_drop.append(col)
                except:
                    pass  # Não é data, mantém a coluna
        
        if cols_to_drop:
            X = X.drop(columns=cols_to_drop, errors="ignore")
            feature_cols = [c for c in feature_cols if c not in cols_to_drop]
        
        # Converte todas as colunas restantes para numérico (garante que one-hot encoding seja numérico)
        # Isso é crítico porque o StandardScaler precisa de dados numéricos
        for col in X.columns:
            if X[col].dtype == 'object':
                # Se ainda for object, tenta converter para numérico
                X[col] = pd.to_numeric(X[col], errors='coerce')
            elif pd.api.types.is_datetime64_any_dtype(X[col]):
                # Se for datetime, remove (não deve chegar aqui, mas por segurança)
                X = X.drop(columns=[col], errors="ignore")
                feature_cols = [c for c in feature_cols if c != col]
        
        # Verificação final: garante que todas as colunas são numéricas
        # Remove qualquer coluna que não seja numérica
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < len(X.columns):
            non_numeric = [c for c in X.columns if c not in numeric_cols]
            X = X[numeric_cols]
            feature_cols = [c for c in feature_cols if c in numeric_cols]
        
        # Remove valores ausentes
        mask = ~(X.isna().any(axis=1) | y.isna())
        X = X[mask]
        y = y[mask]
        
        return X, y, feature_cols
    
    def filter_by_culture(self, cultura):
        """
        Filtra o dataset por uma cultura específica.
        
        Útil para análises focadas em uma única cultura, reduzindo o tamanho
        do dataset e permitindo modelos específicos por cultura.
        
        Args:
            cultura: String com o nome da cultura (ex: "SOJA", "MILHO", "CAFÉ")
        
        Returns:
            DataFrame filtrado ou None se os dados não foram carregados.
        """
        if self.df is None:
            return None
        
        if "Cultura" not in self.df.columns:
            return self.df
        
        # Filtra linhas onde a coluna Cultura corresponde ao valor fornecido
        df_filtered = self.df[self.df["Cultura"] == cultura].copy()
        return df_filtered
    
    def get_summary_stats(self):
        """
        Retorna estatísticas resumidas do dataset carregado.
        
        Útil para verificação rápida dos dados e para exibição no dashboard.
        Inclui informações sobre quantidade de registros, culturas presentes,
        período temporal coberto e lista de colunas disponíveis.
        
        Returns:
            Dicionário com estatísticas ou None se os dados não foram carregados.
        """
        if self.df is None:
            return None
        
        return {
            "total_registros": len(self.df),
            "culturas": self.df["Cultura"].unique().tolist() if "Cultura" in self.df.columns else [],
            "periodo": {
                "inicio": str(self.df["Data"].min()) if "Data" in self.df.columns else None,
                "fim": str(self.df["Data"].max()) if "Data" in self.df.columns else None,
            },
            "colunas": self.df.columns.tolist(),
        }
