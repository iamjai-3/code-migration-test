<?php

if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
    if (isset($data[$id])) {
        unset($data[$id]);
        echo json_encode(['message' => 'Item deleted']);
    } else {
        http_response_code(404);
        echo json_encode(['message' => 'Item not found']);
    }
} else {
    http_response_code(400);
    echo json_encode(['message' => 'ID is required']);
}

?> 