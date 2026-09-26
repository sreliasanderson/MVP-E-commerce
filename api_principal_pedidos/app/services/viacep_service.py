import requests

def buscar_endereco(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if not dados.get("erro"):
            return f"{dados.get('logradouro')}, {dados.get('bairro')} - {dados.get('localidade')}/{dados.get('uf')}"
    
    return None