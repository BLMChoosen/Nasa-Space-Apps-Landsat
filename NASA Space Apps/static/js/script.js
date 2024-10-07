// Inicializar o mapa centrado no Brasil
var map = L.map('map').setView([-15.7801, -47.9292], 4);

// Adicionar camada de tiles ao mapa
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

var existingMarker;

map.on('click', function(e) {
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;

    // Remove existing marker if it exists
    if (existingMarker) {
        map.removeLayer(existingMarker);
    }

    // Add new marker
    existingMarker = L.marker(e.latlng).addTo(map)
        .bindPopup('<b>Confirme a localização:</b><br>Latitude: ' + lat + '<br>Longitude: ' + lon + '<br><button onclick="confirmLocation(' + lat + ', ' + lon + ')">Confirmar</button>')
        .openPopup();
});

function confirmLocation(lat, lon) {
    if (existingMarker) {
        map.closePopup();
    }

    // Enviar dados para o servidor
    $.ajax({
        url: "../../marcar_local",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ latitude: lat, longitude: lon }),
        success: function(response) {
            console.log("Localização salva com sucesso:", response);
        },
        error: function(error) {
            console.error("Erro ao salvar localização:", error);
        }
    });
}