<?php
$token = "8783459954:AAGAf-LwIZEtaPyxIaw1imq-dBLuf4QshBc";
$website = "https://api.telegram.org/bot".$token;

$update = json_decode(file_get_contents('php://input'), true);
if (!$update) exit;

$chatId = $update['message']['chat']['id'] ?? null;
$message = $update['message']['text'] ?? '';

if ($chatId && $message == '/start') {
    file_get_contents($website."/sendMessage?chat_id=$chatId&text=✅ Simple bot working!&parse_mode=HTML");
}
?>
