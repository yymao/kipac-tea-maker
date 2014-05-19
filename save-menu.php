<?php
if($_SERVER['HTTP_X_REQUESTED_WITH'] === 'XMLHttpRequest'){
    $data = file_get_contents('php://input');
    if ($data != '') file_put_contents('menu.json', $data);
}
?>
