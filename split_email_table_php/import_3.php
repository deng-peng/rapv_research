<?php
/**
 * Created by PhpStorm.
 * User: dengpeng
 * Date: 16/5/13
 * Time: 下午4:09
 */

error_reporting(E_ERROR);

require 'config.php';

$count = 0;
$batchSize = 10000;

$handle = new SplFileObject('./data/linked1.cfg', 'r');
$db->query('SET AUTOCOMMIT=0');
$db->query('BEGIN');
foreach ($handle as $line) {
    $count = $count + 1;

    if ($count <= 8570000)
        //28380000
        //42570000
        //56830000
        //70870000
        //84950000
        //28310000
        //42540000
        //56770000
        continue;

    $email = parse_email($line);
    insert_email($email, $db);
    if ($count % $batchSize === 0) {
        if ($db->query('COMMIT') !== false) {
            echo "commit success , count : {$count}" . PHP_EOL;
            $db->query('BEGIN');
        } else {
            echo 'commit error';
            die();
        }
    }
}
$db->query('COMMIT');
echo 'finished';

function parse_email($s)
{
    $s = strtolower(trim($s));
    $arr = explode(':', $s);
    if (count($arr) >= 2)
        return $arr[1];
    return '';
}

function insert_email($email, $db)
{
    if ($email == '')
        return;
    $first = substr($email, 0, 1);
    $alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    if (in_array($first, $alphabet)) {
        $table_name = "people_{$first}";
    } else {
        $table_name = "people_0";
    }
    $sql = "insert into {$table_name} VALUE (0,'$email','', 0, '', '' ,0, 0);";
    $db->query($sql);
}
