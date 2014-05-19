<?php
ob_start();
require 'fetch-calendar.php';
$tea = json_decode(ob_get_clean(), True);

$message = "<h2>{$tea['title']}</h2>";
$message .= "<p>{$tea['date']}</p>";
$message .= "<p>{$tea['description']}</p>";

$prepare_email = 1;
ob_start();
require 'load-menu.php';
$papers = ob_get_clean();

if ($papers != ''){
    $message .= "<h3>Papers to be discussed:</h3><ul>";
    $message .= $papers;
    $message .= "</ul>";
}
else{
    $message .= "<h3>No paper to be discussed!</h3>";
}

echo $message;
?>
