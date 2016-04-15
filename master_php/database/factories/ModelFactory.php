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
        'status'     => 0,
    ];
});
$factory->define(App\Account::class, function ($faker) {
    return [
        'email'  => $faker->email,
        'password' => $faker->password,
        'status'   => Null,
        'token'    => '',
    ];
});