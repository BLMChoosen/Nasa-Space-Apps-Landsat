<!DOCTYPE html>
<html>
<head>
    <title>Mapa Interativo</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        #map { height: 90vh; }
    </style>
</head>
<body>
    <h3>Mapa Interativo: Clique no mapa para selecionar um local</h3>
    <div id="map"></div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>