<?php

$input = json_decode(file_get_contents('php://input'), true);

if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
    if (isset($data[$id])) {
        $data[$id]['name'] = $input['name'] ?? $data[$id]['name'];
        $data[$id]['description'] = $input['description'] ?? $data[$id]['description'];
        echo json_encode($data[$id]);
    } else {
        http_response_code(404);
        echo json_encode(['message' => 'Item not found']);
    }
} else {
    http_response_code(400);
    echo json_encode(['message' => 'ID is required']);
}

?> 