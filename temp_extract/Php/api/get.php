<?php

if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
    if (isset($data[$id])) {
        echo json_encode($data[$id]);
    } else {
        http_response_code(404);
        echo json_encode(['message' => 'Item not found']);
    }
} else {
    echo json_encode(array_values($data));
}

?> 