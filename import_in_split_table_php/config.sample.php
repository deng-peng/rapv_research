<?php
/**
 * Created by PhpStorm.
 * User: dengpeng
 * Date: 16/5/13
 * Time: 下午2:46
 */
include_once "./lib/ez_sql_core.php";

include_once "./lib/ez_sql_mysqli.php";

$db = new ezSQL_mysqli('root', '', 'table', 'localhost');