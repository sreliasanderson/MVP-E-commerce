import requests
import os

# O nome do host 'api_secundaria' corresponde ao serviço nomeado no docker-compose.yml
LOGISTICA_URL = os.getenv("LOGISTICA_URL", "http://api_secundaria:5001/api/frete/calcular")

def calcular_frete(cep_destino):
    try:
        response = requests.post(LOGISTICA_URL, json={"cep_destino": cep_destino})
        if response.status_code == 200:
            dados = response.json()
            return dados.get("valor_frete", 0.0)
    except Exception as e:
        print(f"Erro na comunicacao com API secundaria: {e}")
    
    # Retorna frete de fallback caso a API secundária esteja fora do ar
    return 25.0