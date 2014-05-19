<?php
$papers = json_decode(file_get_contents('menu.json'), True);
if ($prepare_email){
    $papers = $papers['coming-up'];
}
else{
    $papers = $papers[$_GET['cat']];
}

if (count($papers)>0){
    $db_path = 'tea-menu.db';
    $db = new SQLite3($db_path) or die("could not connect to database");

    foreach ($papers as $id){
        $stmt = $db->prepare('select * from papers where id==?');
        $stmt->bindValue(1, $id, SQLITE3_TEXT);
        $res = $stmt->execute();
        $row = $res->fetchArray(SQLITE3_ASSOC);
        $title = $row['title'];
        $author = $row['author'];
        $stmt->close();

        $stmt = $db->prepare('select person from assignment where paper==? AND status==?');
        $stmt->bindValue(1, $id, SQLITE3_TEXT);
        $stmt->bindValue(2, 'ok', SQLITE3_TEXT);
        $res = $stmt->execute();
        $people = array();
        while ($row = $res->fetchArray()) $people[] = $row[0];
        $stmt->close();
        $people = implode(', ', $people);

        if($prepare_email){
            if ($people == '') $people = 'TBD';
            echo "<li>[<a href='http://arxiv.org/abs/$id' target='_blank'>$id</a>] discussion led by $people<br/><b>$title</b> by $author et al.<br/><br/></li>";
        }
        else{
            $info = addslashes("$title by $author et al.");
            echo "<li class='ui-state-default' id='$id' title='$info'><a href='http://arxiv.org/abs/$id' target='_blank'><b>$id</b></a><br/><input type='text' value='$people' placeholder='Discussion leader' /> <img src='search.png'/></li>";
        }
    }
    $db->close();
}
?>
