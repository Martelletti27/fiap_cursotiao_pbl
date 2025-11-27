"""
Módulo de Modelos de Classificação - FASE 2

Este módulo implementa e gerencia os modelos de classificação para prever se o
sistema de irrigação será acionado (Relay_On = 1) ou não (Relay_On = 0). Inclui
5 algoritmos diferentes: Logistic Regression, Random Forest, Gradient Boosting,
SVM e KNN. Cada modelo é treinado e avaliado usando métricas de classificação
como acurácia, precisão, recall e F1-score. O melhor modelo é selecionado
automaticamente baseado no F1-score no conjunto de teste.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from sklearn.base import clone
import joblib
import os
import config

class Phase2Classification:
    """
    Classe para treinar, avaliar e gerenciar modelos de classificação.
    
    Esta classe encapsula toda a lógica de treinamento de múltiplos modelos de
    classificação binária, avaliação de métricas específicas para classificação
    e seleção do melhor modelo. Mantém os modelos treinados em memória para uso
    em previsões e permite salvar/carregar modelos para evitar retreinamento.
    """
    
    def __init__(self):
        """
        Inicializa a classe de classificação.
        
        Atributos:
        - models: Dicionário com modelos treinados e suas métricas
        - results: Dicionário apenas com métricas (para comparação)
        - best_model: Melhor modelo selecionado automaticamente
        - best_model_name: Nome do melhor modelo
        - scaler: Normalizador StandardScaler treinado
        - feature_names: Lista com nomes das features (para interpretação)
        """
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def initialize_models(self):
        """
        Inicializa os 5 modelos de classificação com seus hiperparâmetros.
        
        Define os modelos que serão treinados. Cada modelo tem características
        diferentes: Logistic Regression é linear e rápido, Random Forest e
        Gradient Boosting são ensemble methods poderosos, SVM pode capturar
        padrões complexos e KNN é baseado em similaridade.
        """
        self.models = {
            "Logistic Regression": LogisticRegression(
                random_state=config.RANDOM_STATE,
                max_iter=1000
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=100,
                random_state=config.RANDOM_STATE,
                max_depth=10
            ),
            "Gradient Boosting": GradientBoostingClassifier(
                n_estimators=100,
                random_state=config.RANDOM_STATE,
                max_depth=5
            ),
            "SVM": SVC(
                random_state=config.RANDOM_STATE,
                probability=True
            ),
            "KNN": KNeighborsClassifier(n_neighbors=5),
        }
    
    def train_models(self, X, y):
        """
        Treina todos os modelos de classificação com os dados fornecidos.
        
        O processo de treinamento segue estas etapas:
        1. Divide os dados em treino e teste (80/20)
        2. Normaliza as features usando StandardScaler
        3. Treina cada modelo no conjunto de treino
        4. Avalia cada modelo no conjunto de teste
        5. Calcula métricas de classificação (acurácia, precisão, recall, F1)
        6. Armazena métricas e modelos treinados
        
        Args:
            X: DataFrame ou array com features
            y: Series ou array com variável alvo (0 ou 1)
        
        Returns:
            Dicionário com métricas de todos os modelos treinados
        
        Raises:
            ValueError: Se os dados contêm apenas uma classe (todos 0 ou todos 1)
        """
        # Verifica se há pelo menos 2 classes diferentes nos dados
        # Modelos de classificação precisam de múltiplas classes para aprender
        unique_classes = pd.Series(y).nunique() if hasattr(y, 'nunique') else len(np.unique(y))
        if unique_classes < 2:
            raise ValueError(
                f"Este solver precisa de amostras de pelo menos 2 classes nos dados, "
                f"mas os dados contêm apenas uma classe: {pd.Series(y).unique()[0] if hasattr(y, 'unique') else np.unique(y)[0]}. "
                f"Tente usar dados de múltiplas culturas ou verifique se o filtro não está muito restritivo."
            )
        
        # Armazena nomes das features para uso posterior
        self.feature_names = X.columns.tolist() if hasattr(X, 'columns') else None
        
        # Divide os dados em conjuntos de treino e teste
        # Mantém a mesma proporção e random_state da regressão para consistência
        # Usa stratify=y para garantir que ambas as classes estejam presentes em treino e teste
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE, stratify=y
            )
        except ValueError:
            # Se stratify falhar (classes desbalanceadas), tenta sem stratify
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
            )
        
        # Normalização das features
        # Essencial para modelos como SVM e KNN que são sensíveis à escala
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treina cada modelo definido
        for name, model in self.models.items():
            # Clona o modelo para evitar modificar a definição original
            model_clone = clone(model)
            
            # Treina o modelo no conjunto de treino
            # O modelo aprende a distinguir entre classes (irrigar = 1, não irrigar = 0)
            model_clone.fit(X_train_scaled, y_train)
            
            # Faz previsões nos conjuntos de treino e teste
            y_pred_train = model_clone.predict(X_train_scaled)
            y_pred_test = model_clone.predict(X_test_scaled)
            
            # Calcula probabilidades de previsão (se o modelo suportar)
            # Útil para análise de confiança e threshold customizado
            y_proba_test = None
            if hasattr(model_clone, "predict_proba"):
                y_proba_test = model_clone.predict_proba(X_test_scaled)[:, 1]
            
            # Calcula métricas de classificação
            # Accuracy: Proporção de previsões corretas (pode ser enganosa em classes desbalanceadas)
            # Precision: Dos que previu como positivo, quantos eram realmente positivos
            # Recall: Dos que eram positivos, quantos foram identificados corretamente
            # F1: Média harmônica de precisão e recall (balanceia ambas métricas)
            # Confusion Matrix: Tabela mostrando verdadeiros/falsos positivos/negativos
            metrics = {
                "Accuracy_train": accuracy_score(y_train, y_pred_train),
                "Accuracy_test": accuracy_score(y_test, y_pred_test),
                "Precision_train": precision_score(y_train, y_pred_train, zero_division=0),
                "Precision_test": precision_score(y_test, y_pred_test, zero_division=0),
                "Recall_train": recall_score(y_train, y_pred_train, zero_division=0),
                "Recall_test": recall_score(y_test, y_pred_test, zero_division=0),
                "F1_train": f1_score(y_train, y_pred_train, zero_division=0),
                "F1_test": f1_score(y_test, y_pred_test, zero_division=0),
                "Confusion_Matrix": confusion_matrix(y_test, y_pred_test),
            }
            
            # Armazena o modelo treinado e suas métricas
            # Substitui a definição do modelo pelo modelo treinado
            self.models[name] = {
                "model": model_clone,
                "metrics": metrics,
                "y_test": y_test,
                "y_pred": y_pred_test,
                "y_proba": y_proba_test,
            }
            
            # Armazena métricas no dicionário de resultados para comparação
            self.results[name] = metrics
        
        return self.results
    
    def get_best_model(self):
        """
        Seleciona o melhor modelo baseado na métrica F1-score no conjunto de teste.
        
        F1-score é a média harmônica de precisão e recall, balanceando ambas métricas.
        É preferível à acurácia em problemas de classificação, especialmente quando
        as classes estão desbalanceadas. O modelo com maior F1 no teste indica melhor
        capacidade de generalização.
        
        Returns:
            Tupla (nome_do_melhor_modelo, modelo_treinado) ou None se nenhum modelo foi treinado
        """
        if not self.results:
            return None
        
        # Inicializa com valor muito baixo
        best_f1 = -np.inf
        best_name = None
        
        # Itera sobre todos os modelos treinados
        for name, metrics in self.results.items():
            # Compara F1-score de teste
            if metrics["F1_test"] > best_f1:
                best_f1 = metrics["F1_test"]
                best_name = name
        
        # Armazena o melhor modelo e seu nome
        self.best_model_name = best_name
        self.best_model = self.models[best_name]["model"]
        
        return best_name, self.best_model
    
    def get_feature_importance(self):
        """
        Retorna a importância das features calculada por Random Forest ou Gradient Boosting.
        
        Ambos os algoritmos calculam automaticamente a importância de cada feature.
        Features mais importantes têm maior impacto na decisão de irrigar ou não.
        Esta informação é útil para interpretação e para identificar quais variáveis
        são mais relevantes para a decisão de irrigação.
        
        Returns:
            Tupla (DataFrame com features ordenadas por importância, nome_do_modelo)
            ou (None, None) se nenhum modelo com importância está disponível
        """
        # Tenta obter importância do Random Forest primeiro, depois Gradient Boosting
        for name in ["Random Forest", "Gradient Boosting"]:
            if name in self.models and "model" in self.models[name]:
                model = self.models[name]["model"]
                
                # Verifica se o modelo tem o atributo de importância
                if hasattr(model, "feature_importances_"):
                    importances = model.feature_importances_
                    
                    # Verifica se o número de importâncias corresponde ao número de features
                    if self.feature_names and len(importances) == len(self.feature_names):
                        # Cria DataFrame para facilitar visualização
                        importance_df = pd.DataFrame({
                            "Feature": self.feature_names,
                            "Importance": importances
                        }).sort_values("Importance", ascending=False)
                        
                        # Normaliza para porcentagem
                        importance_df["Importance_%"] = (
                            importance_df["Importance"] / importance_df["Importance"].sum()
                        ) * 100
                        
                        return importance_df, name
        
        return None, None
    
    def predict(self, X):
        """
        Faz previsão binária (irrigar ou não) usando o melhor modelo treinado.
        
        O método aplica a mesma normalização usada no treinamento para garantir
        que os dados de entrada estejam no mesmo formato que os dados de treino.
        
        Args:
            X: DataFrame ou array com features para previsão
        
        Returns:
            Array com previsões (0 = não irrigar, 1 = irrigar) ou None se nenhum modelo foi treinado
        """
        # Seleciona o melhor modelo se ainda não foi selecionado
        if self.best_model is None:
            self.get_best_model()
        
        if self.best_model is None:
            return None
        
        # Aplica normalização usando o scaler treinado
        X_scaled = self.scaler.transform(X)
        
        # Faz a previsão usando o melhor modelo
        return self.best_model.predict(X_scaled)
    
    def predict_proba(self, X):
        """
        Retorna probabilidades de previsão ao invés de classes binárias.
        
        Útil quando é necessário saber a confiança da previsão ou quando se quer
        usar um threshold customizado (ex: irrigar apenas se probabilidade > 0.7).
        
        Args:
            X: DataFrame ou array com features para previsão
        
        Returns:
            Array com probabilidades [P(não irrigar), P(irrigar)] ou None se não suportado
        """
        # Seleciona o melhor modelo se ainda não foi selecionado
        if self.best_model is None:
            self.get_best_model()
        
        if self.best_model is None:
            return None
        
        # Aplica normalização
        X_scaled = self.scaler.transform(X)
        
        # Retorna probabilidades se o modelo suportar
        if hasattr(self.best_model, "predict_proba"):
            return self.best_model.predict_proba(X_scaled)
        
        return None
    
    def save_models(self, directory=None):
        """
        Salva os modelos treinados em arquivos para uso posterior.
        
        Salvar modelos evita ter que retreinar toda vez que o sistema é reiniciado.
        Salva o melhor modelo e o scaler (necessário para normalização).
        
        Args:
            directory: Diretório onde salvar os modelos (None = usa config.MODELS_DIR)
        """
        if directory is None:
            directory = config.MODELS_DIR
        
        os.makedirs(directory, exist_ok=True)
        
        # Salva o melhor modelo e componentes necessários
        if self.best_model is not None:
            joblib.dump(self.best_model, os.path.join(directory, "best_classification_model.pkl"))
            joblib.dump(self.scaler, os.path.join(directory, "classification_scaler.pkl"))
        
        # Salva todos os modelos treinados
        for name, model_data in self.models.items():
            if "model" in model_data:
                joblib.dump(
                    model_data["model"],
                    os.path.join(directory, f"classification_{name.lower().replace(' ', '_')}.pkl")
                )
    
    def load_models(self, directory=None):
        """
        Carrega modelos salvos anteriormente.
        
        Útil para carregar modelos treinados sem precisar retreinar.
        
        Args:
            directory: Diretório onde os modelos estão salvos (None = usa config.MODELS_DIR)
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        if directory is None:
            directory = config.MODELS_DIR
        
        try:
            self.best_model = joblib.load(os.path.join(directory, "best_classification_model.pkl"))
            self.scaler = joblib.load(os.path.join(directory, "classification_scaler.pkl"))
            return True
        except Exception as e:
            print(f"Erro ao carregar modelos: {e}")
            return False
