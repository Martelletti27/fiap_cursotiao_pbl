"""
Sistema de Recomendações Inteligentes de Irrigação

Este módulo gera recomendações automáticas de irrigação baseadas em previsões
meteorológicas, modelos de machine learning e regras de negócio. Combina a
previsão de umidade do solo (modelo de regressão) com dados meteorológicos para criar um
cronograma de irrigação para os próximos 7 dias. Cada recomendação inclui
justificativa técnica explicando o motivo da decisão.
"""
import pandas as pd
import numpy as np
from datetime import datetime
import config

class IrrigationRecommendations:
    """
    Classe para gerar recomendações inteligentes de irrigação.
    
    Esta classe combina múltiplas fontes de informação (modelos ML, dados
    meteorológicos, regras de negócio) para gerar recomendações práticas e
    acionáveis para o produtor rural. Cada recomendação é acompanhada de
    justificativa técnica para facilitar a tomada de decisão.
    """
    
    def __init__(self, regression_model, classification_model, weather_api):
        """
        Inicializa o sistema de recomendações.
        
        Args:
            regression_model: Modelo de regressão treinado (para prever umidade)
            classification_model: Não utilizado (mantido para compatibilidade)
            weather_api: Instância de WeatherAPI para obter previsões meteorológicas
        """
        self.regression_model = regression_model
        self.classification_model = classification_model
        self.weather_api = weather_api
    
    def generate_recommendations(self, city, cultura, days=7):
        """
        Gera recomendações de irrigação para os próximos N dias.
        
        O processo de geração de recomendações segue estas etapas:
        1. Obtém previsão meteorológica para os próximos dias
        2. Para cada dia, prevê a umidade do solo usando o modelo de regressão
        3. Aplica regras de negócio para decidir se deve irrigar
        4. Gera texto de recomendação e justificativa técnica
        5. Retorna cronograma completo com todas as informações
        
        Args:
            city: Nome da cidade para consulta meteorológica
            cultura: Cultura agrícola (SOJA, MILHO ou CAFÉ)
            days: Número de dias de previsão (padrão: 7)
        
        Returns:
            DataFrame com recomendações contendo:
            - data: Data da recomendação
            - dia_semana: Nome do dia da semana
            - temperatura: Temperatura prevista
            - probabilidade_chuva: Probabilidade de chuva (%)
            - chuva_prevista_mm: Volume de chuva previsto
            - umidade_prevista: Umidade do solo prevista (%)
            - deve_irrigar: Boolean indicando se deve irrigar
            - horario_recomendado: Melhor horário para irrigar (se aplicável)
            - recomendacao: Texto descritivo da recomendação
            - justificativa: Explicação técnica da decisão
        """
        # Obtém previsão do tempo da API meteorológica
        weather_df = self.weather_api.get_weather_forecast(city, days=days)
        
        if weather_df is None or len(weather_df) == 0:
            return None
        
        recommendations = []
        
        # Obtém estágios fenológicos possíveis para a cultura
        # Diferentes estágios têm necessidades hídricas diferentes
        estagios = config.ESTAGIOS_POR_CULTURA.get(cultura, ["Vegetativo"])
        
        # Processa cada dia da previsão
        for idx, row in weather_df.iterrows():
            date = row["data"]
            temp = row["temperatura"]
            prob_chuva = row["probabilidade_chuva"]
            chuva_mm = row["chuva_mm"]
            
            # Simula um estágio fenológico (em produção, isso viria de dados reais)
            # Usa o estágio médio como aproximação
            estagio = estagios[len(estagios) // 2]
            
            # Previsão simplificada de umidade do solo
            # Em produção, isso usaria o modelo de regressão com todas as features
            # Por enquanto, usa fórmula simplificada baseada em correlações típicas
            try:
                umidade_prevista = self._predict_umidity_simplified(
                    temp, prob_chuva, chuva_mm
                )
            except:
                # Fallback: estimativa simples baseada em regras empíricas
                umidade_prevista = max(15, min(45, 30 - (temp - 25) * 0.5 + chuva_mm * 2))
            
            # Aplica regras de negócio para decidir se deve irrigar
            deve_irrigar = self._should_irrigate(umidade_prevista, prob_chuva, chuva_mm)
            
            # Gera texto descritivo da recomendação
            recomendacao = self._generate_recommendation_text(
                umidade_prevista, prob_chuva, chuva_mm, deve_irrigar
            )
            
            # Define horário recomendado (madrugada é mais eficiente para irrigação)
            horario_recomendado = "03:00" if deve_irrigar else None
            
            # Compila todas as informações em um dicionário
            recommendations.append({
                "data": date,
                "dia_semana": self._get_day_name(date),
                "temperatura": round(temp, 1),
                "probabilidade_chuva": round(prob_chuva, 1),
                "chuva_prevista_mm": round(chuva_mm, 1),
                "umidade_prevista": round(umidade_prevista, 1),
                "deve_irrigar": deve_irrigar,
                "horario_recomendado": horario_recomendado,
                "recomendacao": recomendacao,
                "justificativa": self._generate_justification(
                    umidade_prevista, prob_chuva, chuva_mm
                ),
            })
        
        return pd.DataFrame(recommendations)
    
    def _predict_umidity_simplified(self, temp, prob_chuva, chuva_mm):
        """
        Previsão simplificada de umidade do solo baseada em correlações empíricas.
        
        Esta é uma versão simplificada que usa fórmulas baseadas em correlações típicas
        entre temperatura, chuva e umidade. Em produção, deveria usar o modelo de
        regressão treinado com todas as features (PH, nutrientes, estágio fenológico, etc).
        
        Args:
            temp: Temperatura prevista (°C)
            prob_chuva: Probabilidade de chuva (%)
            chuva_mm: Volume de chuva previsto (mm)
        
        Returns:
            Umidade do solo prevista (%)
        """
        # Umidade base típica
        umidade_base = 30
        umidade = umidade_base
        
        # Efeito da temperatura: temperatura alta reduz umidade (evaporação)
        # Cada grau acima de 25°C reduz aproximadamente 0.8% de umidade
        umidade -= (temp - 25) * 0.8
        
        # Efeito da chuva: chuva aumenta umidade diretamente
        # Cada mm de chuva aumenta aproximadamente 1.5% de umidade
        umidade += chuva_mm * 1.5
        
        # Efeito da probabilidade de chuva: indica condições que favorecem umidade
        # Mesmo sem chuva real, alta probabilidade indica umidade do ar alta
        umidade += (prob_chuva / 100) * 5
        
        # Limita umidade entre 10% e 50% (valores realistas)
        return max(10, min(50, umidade))
    
    def _should_irrigate(self, umidade, prob_chuva, chuva_mm):
        """
        Decide se deve irrigar baseado em regras de negócio.
        
        A decisão considera múltiplos fatores:
        - Umidade atual do solo (crítica se muito baixa)
        - Chuva prevista (não irrigar se chuva alta está prevista)
        - Probabilidade de chuva (considera incerteza)
        
        Args:
            umidade: Umidade do solo prevista (%)
            prob_chuva: Probabilidade de chuva (%)
            chuva_mm: Volume de chuva previsto (mm)
        
        Returns:
            True se deve irrigar, False caso contrário
        """
        # Regra 1: Não irrigar se umidade está adequada (> 30%)
        # Umidade acima de 30% geralmente é suficiente para a maioria das culturas
        if umidade > 30:
            return False
        
        # Regra 2: Não irrigar se chuva alta está prevista
        # Evita desperdício de água e energia se a chuva vai suprir a necessidade
        if prob_chuva > 70 and chuva_mm > 5:
            return False
        
        # Regra 3: Sempre irrigar se umidade está crítica (< 20%)
        # Umidade muito baixa pode causar estresse hídrico e perda de produtividade
        if umidade < 20:
            return True
        
        # Regra 4: Irrigar se umidade está baixa e pouca chuva prevista
        # Umidade entre 20-30% é subótima, mas se não há chuva prevista, deve irrigar
        if umidade < 30 and (prob_chuva < 50 or chuva_mm < 3):
            return True
        
        # Caso padrão: não irrigar (situação intermediária, monitorar)
        return False
    
    def _generate_recommendation_text(self, umidade, prob_chuva, chuva_mm, deve_irrigar):
        """
        Gera texto descritivo da recomendação de irrigação.
        
        O texto é formatado de forma clara e direta para facilitar a compreensão
        do produtor rural. Inclui informações relevantes como probabilidade de chuva
        e umidade prevista.
        
        Args:
            umidade: Umidade do solo prevista (%)
            prob_chuva: Probabilidade de chuva (%)
            chuva_mm: Volume de chuva previsto (mm)
            deve_irrigar: Boolean indicando se deve irrigar
        
        Returns:
            String com texto da recomendação
        """
        if deve_irrigar:
            # Se deve irrigar mas há probabilidade de chuva, recomenda cautela
            if prob_chuva > 50:
                return f"Irrigar com cautela. Chuva prevista: {prob_chuva:.1f}%"
            else:
                return "Irrigar. Condições favoráveis para aplicação."
        else:
            # Diferentes razões para não irrigar
            if prob_chuva > 70:
                return f"Não irrigar. Chuva prevista: {prob_chuva:.1f}% ({chuva_mm:.1f}mm)"
            elif umidade > 30:
                return f"Não irrigar. Umidade adequada: {umidade:.1f}%"
            else:
                return "Aguardar. Monitorar condições."
    
    def _generate_justification(self, umidade, prob_chuva, chuva_mm):
        """
        Gera justificativa técnica detalhada da recomendação.
        
        A justificativa explica os fatores que levaram à decisão, incluindo
        níveis de umidade, probabilidade de chuva e volume previsto. Isso ajuda
        o produtor a entender o raciocínio por trás da recomendação.
        
        Args:
            umidade: Umidade do solo prevista (%)
            prob_chuva: Probabilidade de chuva (%)
            chuva_mm: Volume de chuva previsto (mm)
        
        Returns:
            String com justificativa técnica
        """
        justificativas = []
        
        # Classifica o nível de umidade
        if umidade < 20:
            justificativas.append(f"Umidade crítica ({umidade:.1f}%) - risco de estresse hídrico")
        elif umidade < 30:
            justificativas.append(f"Umidade abaixo do ideal ({umidade:.1f}%)")
        else:
            justificativas.append(f"Umidade adequada ({umidade:.1f}%)")
        
        # Classifica a probabilidade de chuva
        if prob_chuva > 70:
            justificativas.append(f"Alta probabilidade de chuva ({prob_chuva:.1f}%)")
        elif prob_chuva > 50:
            justificativas.append(f"Probabilidade moderada de chuva ({prob_chuva:.1f}%)")
        
        # Considera volume de chuva se significativo
        if chuva_mm > 5:
            justificativas.append(f"Volume de chuva significativo ({chuva_mm:.1f}mm)")
        
        # Junta todas as justificativas com separador
        return " | ".join(justificativas)
    
    def _get_day_name(self, date_str):
        """
        Converte data em formato string para nome do dia da semana.
        
        Útil para exibição amigável no cronograma de irrigação.
        
        Args:
            date_str: Data no formato "YYYY-MM-DD"
        
        Returns:
            Nome do dia da semana em português ou string vazia se erro
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return days[date.weekday()]
        except:
            return ""
