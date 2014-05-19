<?php
$id = $_GET['id'];
$res = file_get_contents("http://export.arxiv.org/api/query?id_list=$id&max_results=1");
$xml = new SimpleXMLElement($res);
$title  = $xml->entry[0]->title->__toString();
$abs    = $xml->entry[0]->summary->__toString();
$author = $xml->entry[0]->author[0]->name->__toString();

echo "<p><b>[<a href='http://arxiv.org/abs/$id' target='_blank'>$id</a>] $title</b> by $author el al.</p><p style='font-size: small;'>$abs</p>";
?>
