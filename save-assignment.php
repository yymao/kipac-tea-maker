<?php
if($_SERVER['HTTP_X_REQUESTED_WITH'] === 'XMLHttpRequest' && $_POST['paper'] != ''){
    $db_path = 'tea-menu.db';
    $db = new SQLite3($db_path) or die("could not connect to database");
    $stmt = $db->prepare('delete from assignment where paper==?');
    $stmt->bindValue(1, $_POST['paper'], SQLITE3_TEXT);
    $stmt->execute();
    $stmt->close();
    $stmt = $db->prepare('insert into assignment values (?,?,?)');
    $stmt->bindValue(1, $_POST['paper'], SQLITE3_TEXT);
    $stmt->bindValue(2, $_POST['person'], SQLITE3_TEXT);
    $stmt->bindValue(3, 'ok', SQLITE3_TEXT);
    $stmt->execute();
    $stmt->close();
    $db->close();
}
?>
