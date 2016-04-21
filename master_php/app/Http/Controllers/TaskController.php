<?php

namespace App\Http\Controllers;

use App\Account;
use App\Person;
use Illuminate\Http\Request;

use App\Http\Requests;
use SuperClosure\Analyzer\Token;

class TaskController extends Controller
{
    function getTask(Request $request)
    {
        $seq = $request->ip() . ' - ' . date("Y-m-d h:i:sa");
        $level = $request->input('level', 0);
        if ($level > 0) {
            $people = Person::where('working', '')->where('status', 403)->limit(10)->pluck('email');
        } else {
            $people = Person::where('working', '')->where('status', 0)->limit(10)->pluck('email');
        }
        Person::whereIn('email', $people)->update(['working' => $seq]);
        return response()->json([$seq => $people]);
    }

    function getAccount(Request $request)
    {
        $query = Account::where('status', Null)->orWhere('status', config('token_status.active'));
        $account = $query->where('best_ip', $request->ip())->orderBy('updated_at')->first();
        if (!$account) {
            $account = $query->orderBy('updated_at')->first();
        }
        if ($account) {
            $account->status = config('token_status.in_use');
            $account->save();
            return response()->json([
                'account'  => $account->email,
                'password' => $account->password,
                'level'    => $account->level
            ]);
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
                    $person->status = $value['status'];
                    $person->message = $value['message'];
                } else if (key_exists('publicProfileUrl', $value)) {
                    $person->profile_url = $value['publicProfileUrl'];
                    $person->status = $value['status'];
                }
                $person->working = '';
                $person->save();
            }
        }
        return response('ok');
    }

    function postAccountStatus(Request $request)
    {
        $account = Account::whereEmail($request->input('account'))->first();
        if ($account) {
            $status = $request->input('status');
            if ($status == 'active') {
                $account->status = config('token_status.active');
            } elseif ($status == 'frozen') {
                $account->status = config('token_status.frozen');
            } elseif ($status == 'in_use') {
            }
            $account->token = $request->input('token');
            $account->save();
        } else {
            $account = new Account();
            $account->email = trim($request->input('account'));
            $account->password = trim($request->input('password', env('LINKEDIN_PASSWORD')));
            $account->best_ip = $request->ip();
            $account->level = 0;
            $account->save();
        }
    }
}
