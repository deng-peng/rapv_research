<?php

namespace App\Http\Controllers;

use App\Account;
use App\Person;
use Illuminate\Http\Request;

use App\Http\Requests;

class TaskController extends Controller
{
    function getTask(Request $request)
    {
        $seq = $request->ip() . ' - ' . str_random(10);
        $people = Person::where('working', '')->where('status', Null)->limit(3)->pluck('email');
        Person::whereIn('email', $people)->update(['working' => $seq]);
        return response()->json([$seq => $people]);
    }

    function getAccount()
    {
        $account = Account::where('status', Null)->orWhere('status', config('token_status.active'))->orderBy('updated_at')->first();
        if ($account) {
            $account->status = config('token_status.in_use');
            $account->save();
            return response()->json(['account' => $account->account, 'password' => $account->password]);
        }
        return '';
    }

    function postResult(Request $request)
    {
        $result = $request->input('result');
        $arr = json_decode($result, true);
        foreach ($arr as $key => $value) {
            $person = Person::whereEmail($key)->first();
            if ($person) {
                if (key_exists('errorCode', $value)) {
                    $person->error_code = $value['errorCode'];
                    $person->status = $value['status'];
                    $person->message = $value['message'];
                } else if (key_exists('publicProfileUrl', $value)) {
                    $person->profile_url = $value['publicProfileUrl'];
                }
                $person->working = '';
                $person->save();
            }
        }
    }
}