<?php

/*
|--------------------------------------------------------------------------
| Model Factories
|--------------------------------------------------------------------------
|
| Here you may define all of your model factories. Model factories give
| you a convenient way to create models for testing and seeding your
| database. Just tell the factory how a default model should look.
|
*/

$factory->define(App\Person::class, function ($faker) {
    return [
        'email'      => $faker->email,
        'status'     => Null,
        'error_code' => Null,
    ];
});
$factory->define(App\Account::class, function ($faker) {
    return [
        'account'  => $faker->userName,
        'password' => $faker->password,
        'status'   => Null,
        'token'    => '',
    ];
});