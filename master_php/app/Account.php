<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

/**
 * App\Account
 *
 * @mixin \Eloquent
 * @property integer $id
 * @property string $account
 * @property string $password
 * @property boolean $status
 * @property \Carbon\Carbon $created_at
 * @property \Carbon\Carbon $updated_at
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereId($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereAccount($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account wherePassword($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereStatus($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereCreatedAt($value)
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereUpdatedAt($value)
 * @property string $token
 * @method static \Illuminate\Database\Query\Builder|\App\Account whereToken($value)
 */
class Account extends Model
{
    //
}
