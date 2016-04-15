<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

/**
 * App\Person
 *
 * @mixin \Eloquent
 * @property integer $id
 * @property string $email
 * @property boolean $working
 * @property boolean $status
 * @property string $message
 * @property string $profile_url
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereId($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereEmail($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereWorking($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereStatus($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereErrorCode($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereMessage($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Person whereProfileUrl($value)
 */
class Person extends Model
{
    public $timestamps = false;
}
