<?php
$token = "8783459954:AAGAf-LwIZEtaPyxIaw1imq-dBLuf4QshBc";
$update = json_decode(file_get_contents('php://input'), true);

if (!$update) exit;

$chatId = $update['message']['chat']['id'] ?? null;
$message = $update['message']['text'] ?? '';

if ($chatId && $message == '/start') {
    file_get_contents("https://api.telegram.org/bot$token/sendMessage?" . http_build_query([
        'chat_id' => $chatId,
        'text' => "✅ BOT IS WORKING!"
    ]));
}
?>
