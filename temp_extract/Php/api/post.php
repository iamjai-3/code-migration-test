<?php

$input = json_decode(file_get_contents('php://input'), true);
$id = count($data) + 1;
$data[$id] = [
    'id' => $id,
    'name' => $input['name'],
    'description' => $input['description']
];
echo json_encode($data[$id]);

?> 