"""
Módulo de Integração com APIs Meteorológicas

Este módulo fornece interface para consultar dados de previsão do tempo usando
a API Open-Meteo (gratuita, sem necessidade de cadastro ou chave de API).
Os dados meteorológicos são essenciais para o sistema de recomendações de irrigação,
pois chuva prevista e temperatura influenciam diretamente a decisão de quando irrigar.
Retorna None quando a API não está disponível.
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
import config

class WeatherAPI:
    """
    Classe para consultar dados meteorológicos usando Open-Meteo API.
    
    Open-Meteo é uma API meteorológica gratuita e de código aberto que não requer
    cadastro ou chave de API. Usa coordenadas geográficas para obter previsões
    precisas para qualquer localização.
    """
    
    def __init__(self, api_key=None):
        """
        Inicializa a classe de API meteorológica.
        
        Args:
            api_key: Não utilizado (mantido para compatibilidade)
        """
        # Open-Meteo não requer chave de API
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.cache = {}
    
    def get_weather_forecast(self, city, country="BR", days=7):
        """
        Obtém previsão do tempo para os próximos N dias via API Open-Meteo.
        
        Consulta a API usando coordenadas geográficas do município. Não requer
        cadastro ou chave de API. Retorna None se houver erro na requisição.
        
        Args:
            city: Nome da cidade para consulta
            country: Código do país (não utilizado, mantido para compatibilidade)
            days: Número de dias de previsão (padrão: 7, máximo: 16)
        
        Returns:
            DataFrame pandas com previsões diárias contendo:
            - data: Data da previsão
            - temperatura: Temperatura média do dia (°C)
            - umidade: Umidade relativa média (%)
            - probabilidade_chuva: Probabilidade de chuva (%)
            - chuva_mm: Volume de chuva previsto (mm)
            - descricao: Descrição textual do clima
            None se a API não estiver disponível
        """
        # Obtém coordenadas da cidade
        coords = self.get_city_coordinates(city)
        if not coords:
            return None
        
        lat, lon = coords
        
        try:
            # Limita dias a 16 (limite da API gratuita)
            days = min(days, 16)
            
            # Monta URL da API Open-Meteo
            # Parâmetros: latitude, longitude, variáveis meteorológicas, dias de previsão
            # Nota: relative_humidity_2m não está disponível em daily, usamos hourly e agregamos
            url = (
                f"{self.base_url}?"
                f"latitude={lat}&longitude={lon}&"
                f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&"
                f"hourly=relative_humidity_2m&"
                f"timezone=America/Sao_Paulo&"
                f"forecast_days={days}"
            )
            
            response = requests.get(url, timeout=10)
            
            # Se a requisição foi bem-sucedida, processa os dados
            if response.status_code == 200:
                data = response.json()
                return self._parse_openmeteo_data(data, days)
            else:
                # Se houver erro na API, retorna None
                return None
        
        except Exception as e:
            # Em caso de qualquer erro (timeout, conexão, etc), retorna None
            print(f"Erro ao consultar API: {e}")
            return None
    
    def _parse_openmeteo_data(self, data, days):
        """
        Processa e formata dados retornados pela API Open-Meteo.
        
        A API retorna previsões diárias já agregadas. Este método formata os dados
        para o formato esperado pelo sistema.
        
        Args:
            data: Dicionário JSON retornado pela API
            days: Número de dias desejados
        
        Returns:
            DataFrame com previsões diárias
        """
        daily = data.get("daily", {})
        
        if not daily or "time" not in daily:
            return None
        
        # Verifica se há dados suficientes
        if len(daily["time"]) == 0:
            print("Debug: Lista de 'time' vazia")
            return None
        
        forecasts = []
        
        # Itera sobre os dias retornados
        num_days = min(len(daily["time"]), days)
        for i in range(num_days):
            # Calcula temperatura média (média entre máxima e mínima)
            temp_max_list = daily.get("temperature_2m_max", [])
            temp_min_list = daily.get("temperature_2m_min", [])
            
            temp_max = temp_max_list[i] if i < len(temp_max_list) else 25
            temp_min = temp_min_list[i] if i < len(temp_min_list) else 15
            temperatura = (temp_max + temp_min) / 2
            
            # Extrai outros dados
            chuva_list = daily.get("precipitation_sum", [])
            prob_chuva_list = daily.get("precipitation_probability_max", [])
            
            # Calcula umidade média do dia usando dados horários
            hourly = data.get("hourly", {})
            umidade_hourly = hourly.get("relative_humidity_2m", [])
            if umidade_hourly:
                # Calcula média das 24 horas do dia (índices i*24 até (i+1)*24)
                start_idx = i * 24
                end_idx = min((i + 1) * 24, len(umidade_hourly))
                if end_idx > start_idx:
                    umidade = sum(umidade_hourly[start_idx:end_idx]) / (end_idx - start_idx)
                else:
                    umidade = 60
            else:
                umidade = 60
            
            chuva_mm = chuva_list[i] if i < len(chuva_list) else 0
            prob_chuva = prob_chuva_list[i] if i < len(prob_chuva_list) else 0
            
            # Gera descrição baseada na probabilidade de chuva
            if prob_chuva > 70:
                descricao = "chuva intensa"
            elif prob_chuva > 50:
                descricao = "chuva moderada"
            elif prob_chuva > 30:
                descricao = "possibilidade de chuva"
            else:
                descricao = "ceu claro"
            
            forecasts.append({
                "data": daily["time"][i],
                "temperatura": round(temperatura, 1),
                "umidade": round(umidade, 1),
                "probabilidade_chuva": round(prob_chuva, 1),
                "chuva_mm": round(chuva_mm, 1),
                "descricao": descricao,
            })
        
        # Converte lista de dicionários em DataFrame
        if len(forecasts) == 0:
            return None
        
        df = pd.DataFrame(forecasts)
        
        return df
    
    def get_city_coordinates(self, city):
        """
        Retorna coordenadas geográficas (latitude, longitude) de uma cidade.
        
        Mapeia todos os municípios cadastrados no sistema com suas coordenadas
        geográficas precisas para uso em mapas e APIs.
        
        Args:
            city: Nome da cidade
        
        Returns:
            Tupla (latitude, longitude) ou None se cidade não encontrada
        """
        # Dicionário completo com coordenadas de todos os municípios cadastrados
        cities_coords = {
            "São Paulo": (-23.5505, -46.6333),
            "Campinas": (-22.9056, -47.0608),
            "Ribeirão Preto": (-21.1775, -47.8103),
            "Piracicaba": (-22.7253, -47.6493),
            "Londrina": (-23.3045, -51.1696),
            "Cascavel": (-24.9558, -53.4553),
            "Maringá": (-23.4205, -51.9334),
        }
        
        # Retorna coordenadas da cidade ou None se não encontrada
        return cities_coords.get(city)
    
    def test_api_connection(self):
        """
        Testa a conexão com a API Open-Meteo.
        
        Faz uma requisição de teste para verificar se a API está funcionando.
        Open-Meteo não requer chave de API, então sempre retorna True se
        a requisição for bem-sucedida.
        
        Returns:
            True se a API está funcionando, False caso contrário
        """
        try:
            # Testa com coordenadas de São Paulo
            url = (
                f"{self.base_url}?"
                f"latitude=-23.5505&longitude=-46.6333&"
                f"daily=temperature_2m_max&"
                f"timezone=America/Sao_Paulo&"
                f"forecast_days=1"
            )
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                print(f"Erro na API: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"Erro ao testar conexão com API: {e}")
            return False
