<?php

namespace App;

use Illuminate\Database\Eloquent\Model;


/**
 * App\Person
 *
 * @property integer $id
 * @property string $email
 * @property string $working
 * @property integer $status
 * @property string $message
 * @property string $profile_url
 * @property integer $find_count
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereId($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereEmail($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereWorking($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereStatus($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereMessage($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereProfileUrl($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereFindCount($value)
 * @mixin \Eloquent
 */
class Person extends Model
{
    public $timestamps = false;
}
