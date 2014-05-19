<?php
$res = file_get_contents("http://kipac.stanford.edu/collab/seminars/teatalks/schedule/RSS");
$cal = new SimpleXMLElement($res);

foreach ($cal->item as $item) {
    $title = $item->title->__toString();
    $pos = strpos($title, ' - ');
    if ($pos === false) continue;
    $date = substr($title, 0, $pos);
    $title = substr($title, $pos+3);
    $title_l = strtolower($title);
    if (strpos($title_l, 'no ')!==false || strpos($title_l, 'cancel')!==false){
        continue;
    }
    $description = $item->description->__toString();
    echo "{\"date\":\"$date\", \"title\":\"$title\", \"description\":\"$description\"}\n";
    break;
}
?>
