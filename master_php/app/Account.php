<?php

namespace App;

use Illuminate\Database\Eloquent\Model;


/**
 * App\Account
 *
 * @property integer $id
 * @property string $email
 * @property string $password
 * @property boolean $status
 * @property string $token
 * @property \Carbon\Carbon $created_at
 * @property \Carbon\Carbon $updated_at
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereId($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereEmail($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account wherePassword($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereStatus($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereToken($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereCreatedAt($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereUpdatedAt($value)
 * @mixin \Eloquent
 */
class Account extends Model
{
    //
}
