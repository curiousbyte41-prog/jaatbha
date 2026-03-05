<?php
echo "════════════════════════════════════\n";
echo "      🔍 RAILWAY DEBUG INFO        \n";
echo "════════════════════════════════════\n\n";

echo "📂 CURRENT DIRECTORY:\n";
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
echo __DIR__ . "\n\n";

echo "📋 FILES IN DIRECTORY:\n";
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
$files = scandir(__DIR__);
foreach ($files as $file) {
    if ($file != '.' && $file != '..') {
        $size = filesize($file);
        echo "📄 $file - " . $size . " bytes\n";
    }
}
echo "\n";

echo "📄 CONTENT OF my.txt:\n";
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
if (file_exists('my.txt')) {
    $content = file_get_contents('my.txt');
    if (empty($content)) {
        echo "❌ FILE IS EMPTY!\n";
    } else {
        echo "✅ FILE CONTENT:\n";
        echo "------------------------\n";
        echo $content;
        echo "\n------------------------\n";
    }
} else {
    echo "❌ my.txt NOT FOUND!\n";
}

echo "\n════════════════════════════════════\n";
?>
