from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Página inicial que renderiza o mapa
@app.route('/')
def index():
    return render_template('mapa.php')

# Rota para receber as coordenadas clicadas pelo usuário
@app.route('/marcar_local', methods=['POST'])
def marcar_local():
    data = request.get_json()
    lat = data['latitude']
    lon = data['longitude']
    # Criar arquivos para armazenar a latitude e a longitude
    lat_file = 'latitude.txt'
    lon_file = 'longitude.txt'

    # Salvar a latitude no arquivo (substituindo o conteúdo antigo)
    with open(lat_file, 'w') as f:
        f.write(f"{lat}")

    # Salvar a longitude no arquivo (substituindo o conteúdo antigo)
    with open(lon_file, 'w') as f:
        f.write(f"{lon}")

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)