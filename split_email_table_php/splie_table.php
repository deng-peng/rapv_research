<?php
/**
 * Created by PhpStorm.
 * User: dengpeng
 * Date: 16/5/13
 * Time: 下午12:58
 */

include_once "./lib/ez_sql_core.php";

include_once "./lib/ez_sql_mysqli.php";

$db = new ezSQL_mysqli('root', '1234', 'rapv_research', 'localhost');

$last_id = 0;
$batch_size = 1000;

$max_id = $db->get_var("select id from people order by id desc limit 1");
echo $max_id . PHP_EOL;

while ($last_id < $max_id) {
    $sql = "select * from people order by id limit $last_id, $batch_size;";
    $people = $db->get_results($sql);
    foreach ($people as $p) {
        insert_people($p, $db);
    }
    echo $last_id . PHP_EOL;
    $last_id += $batch_size;
}

function insert_people($p, $db)
{
    $email = strtolower($p->email);
    $first = substr($email, 0, 1);
    $alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    if (in_array($first, $alphabet)) {
        $table_name = "people_{$first}";
    } else {
        $table_name = "people_0";
    }
    $sql = "insert into {$table_name} VALUE (0,'$email','', {$p->status}, '', '{$p->profile_url}' ,{$p->find_count});";
    $db->query($sql);
}