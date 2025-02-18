<?php

require_once 'data/data.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        require 'api/get.php';
        break;
    case 'POST':
        require 'api/post.php';
        break;
    case 'PUT':
        require 'api/put.php';
        break;
    case 'DELETE':
        require 'api/delete.php';
        break;
    default:
        http_response_code(405);
        echo json_encode(['message' => 'Method not allowed']);
        break;
}

?> 