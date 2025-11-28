"""
Módulo de Modelos de Regressão - FASE 1

Este módulo implementa e gerencia os modelos de regressão para prever a umidade
do solo. Inclui 5 algoritmos diferentes (Linear, Ridge, Lasso, Random Forest e
Gradient Boosting). O módulo compara todos os modelos e seleciona
automaticamente o melhor baseado na métrica R² no conjunto de teste.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.base import clone
import joblib
import os
import config

class Phase1Regression:
    """
    Classe para treinar, avaliar e gerenciar modelos de regressão.
    
    Esta classe encapsula toda a lógica de treinamento de múltiplos modelos,
    avaliação de métricas e seleção do melhor modelo. Mantém
    os modelos treinados em memória para uso em previsões e permite salvar/carregar
    modelos para evitar retreinamento.
    """
    
    def __init__(self):
        """
        Inicializa a classe de regressão.
        
        Atributos:
        - model_definitions: Dicionário com definições dos modelos (não treinados)
        - trained_models: Dicionário com modelos treinados
        - results: Dicionário com métricas de todos os modelos
        - best_model: Melhor modelo selecionado automaticamente
        - best_model_name: Nome do melhor modelo
        - scaler: Normalizador StandardScaler treinado
        - feature_names: Lista com nomes das features (para interpretação)
        """
        self.model_definitions = {}
        self.trained_models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def initialize_models(self):
        """
        Inicializa os 5 modelos de regressão com seus hiperparâmetros.
        
        Define os modelos que serão treinados. Cada modelo tem características
        diferentes: modelos lineares são rápidos mas podem ter limitações,
        enquanto ensemble methods (Random Forest, Gradient Boosting) são mais
        complexos mas podem capturar padrões não-lineares.
        """
        self.model_definitions = {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(alpha=1.0, random_state=config.RANDOM_STATE),
            "Lasso Regression": Lasso(alpha=0.1, random_state=config.RANDOM_STATE),
            "Random Forest": RandomForestRegressor(
                n_estimators=100,
                random_state=config.RANDOM_STATE,
                max_depth=10
            ),
            "Gradient Boosting": GradientBoostingRegressor(
                n_estimators=100,
                random_state=config.RANDOM_STATE,
                max_depth=5
            ),
        }
    
    def train_models(self, X, y):
        """
        Treina todos os modelos de regressão com os dados fornecidos.
        
        O processo de treinamento segue estas etapas:
        1. Divide os dados em treino e teste (80/20)
        2. Normaliza as features usando StandardScaler
        3. Treina cada modelo no conjunto de treino
        4. Avalia cada modelo no conjunto de teste
        5. Armazena métricas e modelos treinados
        
        Args:
            X: DataFrame ou array com features
            y: Series ou array com variável alvo
        
        Returns:
            Dicionário com métricas de todos os modelos treinados
        """
        # Armazena nomes das features para uso posterior (interpretação, gráficos)
        self.feature_names = X.columns.tolist() if hasattr(X, 'columns') else None
        
        # Divide os dados em conjuntos de treino e teste
        # test_size=0.2 significa 20% para teste, 80% para treino
        # random_state garante que a divisão seja sempre a mesma (reprodutibilidade)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
        )
        
        # Normalização das features
        # StandardScaler transforma cada feature para ter média 0 e desvio padrão 1
        # Isso é importante porque features em escalas diferentes podem prejudicar
        # o desempenho de alguns algoritmos (especialmente modelos lineares e SVM)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treina cada modelo definido
        for name, model in self.model_definitions.items():
            # Clona o modelo para evitar modificar a definição original
            # Isso permite treinar o mesmo tipo de modelo múltiplas vezes
            model_clone = clone(model)
            
            # Treina o modelo no conjunto de treino
            # O modelo aprende a relação entre features (X) e variável alvo (y)
            model_clone.fit(X_train_scaled, y_train)
            
            # Faz previsões nos conjuntos de treino e teste
            # Previsões no treino mostram se o modelo está aprendendo
            # Previsões no teste mostram a capacidade de generalização
            y_pred_train = model_clone.predict(X_train_scaled)
            y_pred_test = model_clone.predict(X_test_scaled)
            
            # Calcula métricas de avaliação
            # MAE: Erro médio absoluto (quanto menor, melhor)
            # MSE: Erro quadrático médio (penaliza erros grandes mais)
            # RMSE: Raiz do MSE (mesma unidade da variável alvo)
            # R²: Coeficiente de determinação (quanto da variância é explicada, 1.0 = perfeito)
            metrics = {
                "MAE_train": mean_absolute_error(y_train, y_pred_train),
                "MAE_test": mean_absolute_error(y_test, y_pred_test),
                "MSE_train": mean_squared_error(y_train, y_pred_train),
                "MSE_test": mean_squared_error(y_test, y_pred_test),
                "RMSE_train": np.sqrt(mean_squared_error(y_train, y_pred_train)),
                "RMSE_test": np.sqrt(mean_squared_error(y_test, y_pred_test)),
                "R2_train": r2_score(y_train, y_pred_train),
                "R2_test": r2_score(y_test, y_pred_test),
            }
            
            # Armazena o modelo treinado e suas métricas
            # Também guarda y_test e y_pred para análise posterior (gráficos, etc)
            self.trained_models[name] = {
                "model": model_clone,
                "metrics": metrics,
                "y_test": y_test,
                "y_pred": y_pred_test,
            }
            
            # Armazena métricas no dicionário de resultados para comparação
            self.results[name] = metrics
        
        return self.results
    
    def get_best_model(self):
        """
        Seleciona o melhor modelo baseado na métrica R² no conjunto de teste.
        
        R² (coeficiente de determinação) mede quanto da variância da variável
        alvo é explicada pelo modelo. Valores próximos de 1.0 indicam bom ajuste.
        O modelo com maior R² no teste é considerado o melhor, pois indica melhor
        capacidade de generalização para dados não vistos.
        
        Returns:
            Tupla (nome_do_melhor_modelo, modelo_treinado) ou None se nenhum modelo foi treinado
        """
        if not self.results:
            return None
        
        # Inicializa com valor muito baixo para garantir que qualquer modelo seja melhor
        best_r2 = -np.inf
        best_name = None
        
        # Itera sobre todos os modelos treinados
        for name, metrics in self.results.items():
            # Compara R² de teste (métrica de generalização)
            if metrics["R2_test"] > best_r2:
                best_r2 = metrics["R2_test"]
                best_name = name
        
        # Armazena o melhor modelo e seu nome
        self.best_model_name = best_name
        
        # Recupera o modelo treinado
        self.best_model = self.trained_models[best_name]["model"]
        
        return best_name, self.best_model
    
    def get_feature_importance(self):
        """
        Retorna a importância das features calculada pelo Random Forest.
        
        Random Forest calcula automaticamente a importância de cada feature
        baseado em quanto ela contribui para reduzir a impureza nas árvores.
        Features mais importantes têm maior impacto nas previsões do modelo.
        Esta informação é útil para interpretação e para identificar quais
        variáveis são mais relevantes para prever a umidade do solo.
        
        Returns:
            DataFrame com features ordenadas por importância (do maior para menor)
            ou None se o Random Forest não foi treinado
        """
        # Tenta obter o modelo Random Forest treinado
        rf_key = "Random Forest"
        rf_model = None
        
        if rf_key in self.trained_models:
            rf_model = self.trained_models[rf_key]["model"]
        
        if rf_model is None:
            return None
        
        # Extrai a importância das features do modelo
        if rf_model and hasattr(rf_model, "feature_importances_"):
            importances = rf_model.feature_importances_
            
            # Verifica se o número de importâncias corresponde ao número de features
            if self.feature_names and len(importances) == len(self.feature_names):
                # Cria DataFrame para facilitar visualização e ordenação
                importance_df = pd.DataFrame({
                    "Feature": self.feature_names,
                    "Importance": importances
                }).sort_values("Importance", ascending=False)
                
                # Normaliza para porcentagem (soma = 100%)
                # Facilita interpretação: "Feature X explica Y% da umidade"
                importance_df["Importance_%"] = (
                    importance_df["Importance"] / importance_df["Importance"].sum()
                ) * 100
                
                return importance_df
        
        return None
    
    def predict(self, X):
        """
        Faz previsão de umidade do solo usando o melhor modelo treinado.
        
        O método aplica as mesmas transformações usadas no treinamento:
        normalização. Isso garante que os dados de entrada
        estejam no mesmo formato que os dados de treino.
        
        Args:
            X: DataFrame ou array com features para previsão
        
        Returns:
            Array com previsões de umidade do solo ou None se nenhum modelo foi treinado
        """
        # Seleciona o melhor modelo se ainda não foi selecionado
        if self.best_model is None:
            self.get_best_model()
        
        if self.best_model is None:
            return None
        
        # Aplica normalização usando o scaler treinado
        # IMPORTANTE: usa transform, não fit_transform, pois o scaler já foi treinado
        X_scaled = self.scaler.transform(X)
        
        # Faz a previsão usando o melhor modelo
        return self.best_model.predict(X_scaled)
    
    def save_models(self, directory=None):
        """
        Salva os modelos treinados em arquivos para uso posterior.
        
        Salvar modelos evita ter que retreinar toda vez que o sistema é reiniciado.
        Salva o melhor modelo e o scaler (necessário para normalização).
        Também salva todos os modelos individuais para análise.
        
        Args:
            directory: Diretório onde salvar os modelos (None = usa config.MODELS_DIR)
        """
        if directory is None:
            directory = config.MODELS_DIR
        
        os.makedirs(directory, exist_ok=True)
        
        # Salva o melhor modelo e componentes necessários para previsão
        if self.best_model is not None:
            joblib.dump(self.best_model, os.path.join(directory, "best_regression_model.pkl"))
            joblib.dump(self.scaler, os.path.join(directory, "scaler.pkl"))
        
        # Salva todos os modelos treinados
        for name, model_data in self.trained_models.items():
            if "model" in model_data:
                joblib.dump(
                    model_data["model"],
                    os.path.join(directory, f"regression_{name.lower().replace(' ', '_')}.pkl")
                )
    
    def load_models(self, directory=None):
        """
        Carrega modelos salvos anteriormente.
        
        Útil para carregar modelos treinados sem precisar retreinar, economizando
        tempo e recursos computacionais.
        
        Args:
            directory: Diretório onde os modelos estão salvos (None = usa config.MODELS_DIR)
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        if directory is None:
            directory = config.MODELS_DIR
        
        try:
            self.best_model = joblib.load(os.path.join(directory, "best_regression_model.pkl"))
            self.scaler = joblib.load(os.path.join(directory, "scaler.pkl"))
            
            return True
        except Exception as e:
            print(f"Erro ao carregar modelos: {e}")
            return False
