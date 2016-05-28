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

Route::post('task','PeopleTaskController@getTask');
Route::post('task/people','PeopleTaskController@getTask');

Route::post('result','PeopleTaskController@postResult');
Route::post('result/people','PeopleTaskController@postResult');

Route::post('slave/status','SlaveController@postStatus');

Route::get('slave/status','SlaveController@getStatus');

Route::get('proxy','ProxyController@getProxy');

Route::post('proxy','ProxyController@updateProxyStatus');


Route::post('task/phone','PhoneTaskController@getTask');

Route::post('result/phone','PhoneTaskController@postResult');