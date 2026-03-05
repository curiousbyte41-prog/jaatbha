<?php
$botToken = "8783459954:AAGAf-LwIZEtaPyxIaw1imq-dBLuf4QshBc";
$website = "https://api.telegram.org/bot".$botToken;

// Get incoming update
$content = file_get_contents("php://input");
$update = json_decode($content, true);

if (!$update) {
    http_response_code(200);
    echo "OK";
    exit;
}

// Handle message
if (isset($update["message"])) {
    $chatId = $update["message"]["chat"]["id"];
    $message = $update["message"]["text"] ?? "";
    $userId = $update["message"]["from"]["id"];
    $username = $update["message"]["from"]["username"] ?? "User";
    
    if ($message == "/start") {
        $text = "✅ <b>BOT WORKING!</b>\n\n";
        $text .= "User ID: <code>$userId</code>\n";
        $text .= "Username: @$username";
        
        file_get_contents($website."/sendMessage?" . http_build_query([
            'chat_id' => $chatId,
            'text' => $text,
            'parse_mode' => 'HTML'
        ]));
    }
}

http_response_code(200);
echo "OK";
?>
