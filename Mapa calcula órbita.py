from flask import Flask, render_template, request, jsonify
import folium
import time
import threading
import requests as req
import json
from geopy.distance import geodesic

app = Flask(__name__)

# Definir a localização de destino
destino_lat = -15.7801
destino_lon = -47.9292

# Função para obter posições futuras do satélite
def obter_posicoes(sat_id, tempo_total_futuro, modo):
    if modo != 'futuro':
        raise ValueError("Modo inválido. Use 'futuro'.")
    url = f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/{destino_lat}/{destino_lon}/0/{tempo_total_futuro}/&apiKey=YOUR_API_KEY"
    response = req.get(url)
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        print("Erro ao decodificar o JSON. Resposta da API:", response.text)
        return None

# Função para calcular a órbita completa do satélite
def calcular_orbita_completa(sat_id):
    tempo_total_futuro = 5940  # Tempo total futuro em segundos
    posicoes_futuras_response = obter_posicoes(sat_id, tempo_total_futuro, 'futuro')
    if posicoes_futuras_response is not None and 'positions' in posicoes_futuras_response:
        posicoes_futuras = posicoes_futuras_response['positions']
    else:
        posicoes_futuras = []
    return posicoes_futuras

# Função para verificar se o satélite está sobre o local de destino
def satelite_sobre_destino(sat_lat, sat_lon, dest_lat, dest_lon):
    distancia = geodesic((sat_lat, sat_lon), (dest_lat, dest_lon)).km
    return distancia <= 92.5  # Metade da diagonal da cobertura de 185x180 km

# Função para gerar o mapa com a órbita do satélite
def gerar_mapa_orbita(sat_id1, sat_id2):
    posicoes1 = calcular_orbita_completa(sat_id1)
    posicoes2 = calcular_orbita_completa(sat_id2)
    if not posicoes1 or not posicoes2:
        print("Erro: Não foi possível obter as posições dos satélites.")
        return None

    initial_position1 = posicoes1[len(posicoes1) // 2]
    initial_position2 = posicoes2[len(posicoes2) // 2]
    mapa = folium.Map(location=[destino_lat, destino_lon], zoom_start=4)
    
    # Filtrar pontos inválidos
    orbit_points1 = [(p['satlatitude'], p['satlongitude']) for p in posicoes1 if -90 <= p['satlatitude'] <= 90 and -180 <= p['satlongitude'] <= 180]
    orbit_points2 = [(p['satlatitude'], p['satlongitude']) for p in posicoes2 if -90 <= p['satlatitude'] <= 90 and -180 <= p['satlongitude'] <= 180]
    
    # Adicionar a órbita do primeiro satélite ao mapa
    folium.PolyLine(
        locations=orbit_points1,
        color='red',
        weight=2.5,
        opacity=1,
        line_cap="square",
    ).add_to(mapa)
    
    # Adicionar a órbita do segundo satélite ao mapa
    folium.PolyLine(
        locations=orbit_points2,
        color='orange',
        weight=2.5,
        opacity=1,
        line_cap="square",
    ).add_to(mapa)
    
    # Adicionar marcador para a posição atual do primeiro satélite
    folium.Marker(
        location=[initial_position1['satlatitude'], initial_position1['satlongitude']],
        popup='Posição Atual do Landsat 8',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(mapa)
    
    # Adicionar marcador para a posição atual do segundo satélite
    folium.Marker(
        location=[initial_position2['satlatitude'], initial_position2['satlongitude']],
        popup='Posição Atual do Landsat 9',
        icon=folium.Icon(color='orange', icon='info-sign')
    ).add_to(mapa)
    
    # Verificar se o primeiro satélite está sobre o local de destino
    if satelite_sobre_destino(initial_position1['satlatitude'], initial_position1['satlongitude'], destino_lat, destino_lon):
        folium.Marker(
            location=[destino_lat, destino_lon],
            popup='Landsat 8 está sobre o destino',
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(mapa)
    
    # Verificar se o segundo satélite está sobre o local de destino
    if satelite_sobre_destino(initial_position2['satlatitude'], initial_position2['satlongitude'], destino_lat, destino_lon):
        folium.Marker(
            location=[destino_lat, destino_lon],
            popup='Landsat 9 está sobre o destino',
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(mapa)
    
    # Salvar o mapa gerado em um arquivo HTML
    mapa.save('templates/mapa_satelite_orbita.html')

@app.route('/')
def index():
    return render_template('mapa_satelite_orbita.html')

@app.route('/update_map')
def update_map():
    gerar_mapa_orbita(25544, 25545)  # Exemplo: Landsat 8 e Landsat 9
    return jsonify(success=True)

# Função para atualizar o mapa a cada 14 segundos
def atualizar_mapa():
    while True:
        gerar_mapa_orbita(25544, 25545)  # Exemplo: Landsat 8 e Landsat 9
        time.sleep(14)

# Iniciar a thread para atualizar o mapa
threading.Thread(target=atualizar_mapa, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
print("teste")
print("teste")