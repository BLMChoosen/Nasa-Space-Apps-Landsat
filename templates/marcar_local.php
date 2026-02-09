<?php
// Receber dados da requisição POST
$data = json_decode(file_get_contents('php://input'), true);

if ($data) {
    $latitude = $data['latitude'];
    $longitude = $data['longitude'];

    // Criar um arquivo para armazenar a latitude e a longitude
    $file = 'clicked_location.txt';
    $content = "Latitude: $latitude, Longitude: $longitude\n";

    // Salvar os dados no arquivo
    file_put_contents($file, $content, FILE_APPEND);

    // Retornar uma resposta de sucesso
    echo json_encode(['status' => 'success']);
} else {
    // Retornar uma resposta de erro
    echo json_encode(['status' => 'error', 'message' => 'Dados inválidos']);
}
?>