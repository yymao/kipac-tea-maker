<?php
if($_SERVER['HTTP_X_REQUESTED_WITH'] === 'XMLHttpRequest' && $_GET['id']!=''){

    $db_path = 'tea-menu.db';
    $db = new SQLite3($db_path) or die("could not connect to database");

    $id = $_GET['id'];
    $stmt = $db->prepare('select * from papers where id==?');
    $stmt->bindValue(1, $id, SQLITE3_TEXT);
    $res = $stmt->execute();
    if ($row = $res->fetchArray(SQLITE3_ASSOC)){
        $title = $row['title'];
        $author = $row['author'];
        $stmt->close();
    }
    else{
        $stmt->close();
        $res = file_get_contents("http://export.arxiv.org/api/query?id_list=$id&max_results=1");
        $xml = new SimpleXMLElement($res);
        $title = $xml->entry[0]->title->__toString();
        $author = $xml->entry[0]->author[0]->name->__toString();
        if ($title == "" || $author == ""){
            $db->close();
            exit(0);
        }
        $stmt = $db->prepare('insert into papers values (?,?,?)');
        $stmt->bindValue(1, $id, SQLITE3_TEXT);
        $stmt->bindValue(2, $title, SQLITE3_TEXT);
        $stmt->bindValue(3, $author, SQLITE3_TEXT);
        $stmt->execute();
        $stmt->close();
    }
    $db->close();
    
    $info = addslashes("$title by $author et al.");
    echo "<li class='ui-state-default' id='$id' title='$info'><a href='http://arxiv.org/abs/$id' target='_blank'><b>$id</b></a><br/><input type='text' value='' placeholder='Discussion leader' /> <img src='search.png'/></li>";
}

?>
