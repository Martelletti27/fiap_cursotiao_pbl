"""
Módulo de Integração com APIs Meteorológicas

Este módulo fornece interface para consultar dados de previsão do tempo de APIs
externas (OpenWeatherMap, INMET) ou gerar dados simulados quando a API não está
disponível. Os dados meteorológicos são essenciais para o sistema de recomendações
de irrigação, pois chuva prevista e temperatura influenciam diretamente a decisão
de quando irrigar. O módulo inclui fallback automático para dados simulados baseados
em padrões sazonais quando a API real não está configurada ou falha.
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config

class WeatherAPI:
    """
    Classe para consultar dados meteorológicos de APIs externas.
    
    Esta classe abstrai a complexidade de integração com diferentes APIs de clima,
    fornecendo uma interface única para obter previsões do tempo. Inclui tratamento
    de erros e fallback automático para dados simulados, garantindo que o sistema
    sempre tenha dados meteorológicos disponíveis mesmo sem conexão com APIs externas.
    """
    
    def __init__(self, api_key=None):
        """
        Inicializa a classe de API meteorológica.
        
        Args:
            api_key: Chave de API para OpenWeatherMap (None = usa config ou dados simulados)
        """
        self.api_key = api_key or config.WEATHER_API_KEY
        self.base_url = config.WEATHER_API_URL
        self.cache = {}
    
    def get_weather_forecast(self, city, country="BR", days=7):
        """
        Obtém previsão do tempo para os próximos N dias.
        
        Tenta primeiro usar a API real (OpenWeatherMap). Se não houver API key
        configurada ou se houver erro na requisição, retorna dados simulados
        baseados em padrões sazonais. Isso garante que o sistema funcione mesmo
        sem configuração de API externa.
        
        Args:
            city: Nome da cidade para consulta
            country: Código do país (padrão: "BR" para Brasil)
            days: Número de dias de previsão (padrão: 7)
        
        Returns:
            DataFrame pandas com previsões diárias contendo:
            - data: Data da previsão
            - temperatura: Temperatura média do dia (°C)
            - umidade: Umidade relativa média (%)
            - probabilidade_chuva: Probabilidade de chuva (%)
            - chuva_mm: Volume de chuva previsto (mm)
            - descricao: Descrição textual do clima
        """
        # Se não houver API key, retorna dados simulados imediatamente
        if not self.api_key:
            return self._get_simulated_weather(city, days)
        
        try:
            # Monta URL da API OpenWeatherMap
            # Parâmetros: cidade, país, chave API, unidades métricas, idioma português
            url = f"{self.base_url}?q={city},{country}&appid={self.api_key}&units=metric&lang=pt_br"
            response = requests.get(url, timeout=10)
            
            # Se a requisição foi bem-sucedida, processa os dados
            if response.status_code == 200:
                data = response.json()
                return self._parse_openweather_data(data, days)
            else:
                # Se houver erro na API, usa dados simulados como fallback
                return self._get_simulated_weather(city, days)
        
        except Exception as e:
            # Em caso de qualquer erro (timeout, conexão, etc), usa dados simulados
            print(f"Erro ao consultar API: {e}. Usando dados simulados.")
            return self._get_simulated_weather(city, days)
    
    def _parse_openweather_data(self, data, days):
        """
        Processa e formata dados retornados pela API OpenWeatherMap.
        
        A API retorna previsões a cada 3 horas. Este método agrupa essas previsões
        por dia, calculando médias para temperatura e umidade, máximo para
        probabilidade de chuva e soma para volume de chuva.
        
        Args:
            data: Dicionário JSON retornado pela API
            days: Número de dias desejados
        
        Returns:
            DataFrame com previsões agrupadas por dia
        """
        forecasts = []
        
        # Itera sobre as previsões retornadas (limitado a days * 8, pois há 8 previsões por dia)
        for item in data.get("list", [])[:days * 8]:
            # Converte timestamp Unix para objeto datetime
            dt = datetime.fromtimestamp(item["dt"])
            
            # Extrai informações relevantes de cada previsão
            forecasts.append({
                "data": dt.strftime("%Y-%m-%d"),
                "hora": dt.strftime("%H:%M"),
                "temperatura": item["main"]["temp"],
                "umidade": item["main"]["humidity"],
                "probabilidade_chuva": item.get("pop", 0) * 100,  # pop vem como decimal (0-1)
                "chuva_mm": item.get("rain", {}).get("3h", 0) if "rain" in item else 0,
                "descricao": item["weather"][0]["description"],
            })
        
        # Converte lista de dicionários em DataFrame
        df = pd.DataFrame(forecasts)
        
        # Agrupa previsões por dia, agregando valores
        # Média para temperatura e umidade, máximo para probabilidade, soma para chuva
        df_daily = df.groupby("data").agg({
            "temperatura": "mean",
            "umidade": "mean",
            "probabilidade_chuva": "max",
            "chuva_mm": "sum",
            "descricao": "first",
        }).reset_index()
        
        # Retorna apenas o número de dias solicitado
        return df_daily.head(days)
    
    def _get_simulated_weather(self, city, days):
        """
        Gera dados meteorológicos simulados baseados em padrões sazonais.
        
        Quando a API real não está disponível, este método gera previsões realistas
        baseadas em padrões sazonais do Brasil. Temperatura e probabilidade de chuva
        variam conforme a estação do ano (verão tem mais chuva e temperatura mais alta).
        Inclui variação aleatória para simular condições reais.
        
        Args:
            city: Nome da cidade (não usado na simulação, mas mantido para compatibilidade)
            days: Número de dias de previsão
        
        Returns:
            DataFrame com previsões simuladas no mesmo formato da API real
        """
        forecasts = []
        base_date = datetime.now()
        
        # Gera previsão para cada dia solicitado
        for i in range(days):
            date = base_date + timedelta(days=i)
            
            # Calcula o dia do ano (1-365) para determinar a estação
            day_of_year = date.timetuple().tm_yday
            
            # Define temperatura base conforme a estação
            # Verão no Brasil (março-junho, aproximadamente dias 80-172): mais quente
            # Inverno: mais frio
            temp_base = 25 if 80 <= day_of_year <= 172 else 20
            temperatura = temp_base + np.random.normal(0, 3)  # Adiciona variação aleatória
            
            # Probabilidade de chuva maior no verão
            prob_chuva_base = 0.4 if 80 <= day_of_year <= 172 else 0.2
            probabilidade_chuva = min(100, max(0, (prob_chuva_base + np.random.normal(0, 0.15)) * 100))
            
            # Chuva real baseada na probabilidade
            # Se a probabilidade for alta, há maior chance de chover
            chuva_mm = np.random.exponential(2) if np.random.random() < (probabilidade_chuva / 100) else 0
            
            # Umidade relativa varia aleatoriamente em torno de 60%
            umidade = 60 + np.random.normal(0, 10)
            umidade = max(30, min(90, umidade))  # Limita entre 30% e 90%
            
            # Adiciona previsão à lista
            forecasts.append({
                "data": date.strftime("%Y-%m-%d"),
                "temperatura": round(temperatura, 1),
                "umidade": round(umidade, 1),
                "probabilidade_chuva": round(probabilidade_chuva, 1),
                "chuva_mm": round(chuva_mm, 1),
                "descricao": "céu parcialmente nublado" if probabilidade_chuva > 50 else "céu claro",
            })
        
        return pd.DataFrame(forecasts)
    
    def get_city_coordinates(self, city):
        """
        Retorna coordenadas geográficas (latitude, longitude) de uma cidade.
        
        Útil para APIs que requerem coordenadas ao invés de nome da cidade.
        Atualmente implementado com um dicionário fixo, mas pode ser expandido
        para usar APIs de geocodificação.
        
        Args:
            city: Nome da cidade
        
        Returns:
            Tupla (latitude, longitude) ou coordenadas padrão de São Paulo
        """
        # Dicionário com coordenadas de algumas cidades brasileiras
        # Pode ser expandido ou integrado com API de geocodificação
        cities_coords = {
            "São Paulo": (-23.5505, -46.6333),
            "Campinas": (-22.9056, -47.0608),
            "Ribeirão Preto": (-21.1775, -47.8103),
            "Piracicaba": (-22.7253, -47.6493),
            "Londrina": (-23.3045, -51.1696),
        }
        
        # Retorna coordenadas da cidade ou padrão (São Paulo)
        return cities_coords.get(city, (-23.5505, -46.6333))
