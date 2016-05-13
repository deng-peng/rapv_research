<?php
/**
 * Created by PhpStorm.
 * User: dengpeng
 * Date: 16/5/13
 * Time: 下午9:15
 */

namespace App\Utils;


class Helper
{
    public static function getPeopleTableName($email)
    {
        $tables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
        $first = substr($email, 0, 1);
        if (in_array($first, $tables)) {
            $table_name = "people_{$first}";
        } else {
            $table_name = "people_0";
        }

        return $table_name;
    }

    public static function getRandomPeopleTableName()
    {
        $tables = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
        $rand_key = array_rand($tables, 1);
        return 'people_' . $tables[$rand_key];
    }
}