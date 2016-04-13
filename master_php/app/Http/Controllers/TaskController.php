<?php

namespace App\Http\Controllers;

use App\Account;
use App\Person;
use DB;
use Illuminate\Http\Request;

use App\Http\Requests;

class TaskController extends Controller
{
    function getTask()
    {
        $people = Person::where('working', false)->where('status', Null)->limit(3)->pluck('email');
        Person::whereIn('email', $people)->update(['working' => true]);
        return response()->json($people);
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
    }
}
