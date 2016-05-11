<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Slave extends Model
{
    protected $fillable = ['ip', 'status'];
}
