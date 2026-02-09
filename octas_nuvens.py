# Autor: Davi Oliz
import requests as req

validdatetime = "2024-10-06T00:00:00Z"  # Atualize para uma data válida
parameters = "total_cloud_cover:octas"
api_url = "https://api.meteomatics.com/{}/{}/{},{}/{}"

def verificar_nuvens(latitude, longitude):
    format = "json"

    # Fazer a requisição GET para a API
    try:
        response = req.get(api_url.format(validdatetime, parameters, latitude, longitude, format), 
                           auth=('nasaspaceapps_oliz_davi', '474VenDvuT'))
    except req.RequestException as e:
        print(f"Erro na requisição: {e}")
        return False

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        try:
            dados = response.json()
        except ValueError as e:
            print("Erro ao analisar JSON:", e)
            return False

        # Extrair o valor de octas de nuvens do JSON retornado
        try:
            octas = dados['data'][0]['coordinates'][0]['dates'][0]['value']
            # Verificar se a quantidade de nuvens é maior que 15%
            if octas >= 1.2:  # 1 octa = 12.5%, então 15% é aproximadamente 1.2 octas
                return True
            else:
                return False
                
        except (KeyError, IndexError) as e:
            print("Erro ao extrair dados de nuvens:", e)
            return False
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(f"Resposta da API: {response.text}")
        return False
