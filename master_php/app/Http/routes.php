<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It's a breeze. Simply tell Laravel the URIs it should respond to
| and give it the controller to call when that URI is requested.
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::post('task','TaskController@getTask');

Route::get('account','TaskController@getAccount');
Route::post('account','TaskController@postAccountStatus');

Route::post('result','TaskController@postResult');

Route::post('slave/status','SlaveController@postStatus');
