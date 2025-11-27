"""
Script principal para executar o dashboard
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    # Verificar se streamlit está instalado
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit não está instalado. Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    # Executar dashboard
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])
