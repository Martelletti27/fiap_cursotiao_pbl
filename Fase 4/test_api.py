"""
Script de Teste da API Meteorológica

Este script testa a conexão com a API OpenWeatherMap e verifica se os dados
estão sendo carregados corretamente para todos os municípios cadastrados.
"""
import sys
import os

# Adiciona o diretório atual ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_api import WeatherAPI
import config

def test_api():
    """Testa a API meteorológica para todos os municípios cadastrados."""
    
    print("=" * 60)
    print("TESTE DA API METEOROLÓGICA - OpenWeatherMap")
    print("=" * 60)
    print()
    
    # Open-Meteo não requer chave de API
    print("[INFO] Usando API Open-Meteo (gratuita, sem cadastro necessario)")
    print()
    
    # Inicializa a API (sem chave necessária)
    weather_api = WeatherAPI()
    
    # Testa conexão geral
    print("Testando conexao com a API...")
    if weather_api.test_api_connection():
        print("[OK] Conexao com API estabelecida com sucesso!")
    else:
        print("[ERRO] Falha na conexao com a API. Verifique sua chave de API.")
        return False
    
    print()
    print("=" * 60)
    print("TESTANDO MUNICÍPIOS CADASTRADOS")
    print("=" * 60)
    print()
    
    # Testa cada município cadastrado
    municipios = config.MUNICIPIOS_CADASTRADOS
    resultados = []
    
    for municipio in municipios:
        print(f"Testando: {municipio}...", end=" ")
        
        # Verifica coordenadas
        coords = weather_api.get_city_coordinates(municipio)
        if not coords:
            print(f"[ERRO] Coordenadas nao encontradas")
            resultados.append((municipio, False, "Coordenadas nao encontradas"))
            continue
        
        # Tenta obter previsão
        try:
            weather_df = weather_api.get_weather_forecast(municipio, days=7)
            
            if weather_df is not None and len(weather_df) > 0:
                print(f"[OK] {len(weather_df)} dias de previsao")
                print(f"   Temperatura media: {weather_df['temperatura'].mean():.1f}C")
                print(f"   Probabilidade de chuva media: {weather_df['probabilidade_chuva'].mean():.1f}%")
                resultados.append((municipio, True, f"{len(weather_df)} dias"))
            else:
                print(f"[ERRO] Falha - Nenhum dado retornado")
                resultados.append((municipio, False, "Nenhum dado retornado"))
        except Exception as e:
            print(f"[ERRO] Erro: {str(e)}")
            resultados.append((municipio, False, str(e)))
        
        print()
    
    # Resumo dos resultados
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print()
    
    sucessos = sum(1 for _, status, _ in resultados if status)
    total = len(resultados)
    
    for municipio, status, info in resultados:
        status_icon = "[OK]" if status else "[ERRO]"
        print(f"{status_icon} {municipio}: {info}")
    
    print()
    print(f"Total: {sucessos}/{total} municipios funcionando")
    
    if sucessos == total:
        print()
        print("[SUCESSO] Todos os testes passaram! A API esta funcionando corretamente.")
        return True
    else:
        print()
        print("[AVISO] Alguns municipios falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    sucesso = test_api()
    sys.exit(0 if sucesso else 1)

