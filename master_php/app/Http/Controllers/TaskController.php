<?php

namespace App\Http\Controllers;

use App\Account;
use App\Utils\Helper;
use DB;
use Illuminate\Http\Request;

use App\Http\Requests;

class TaskController extends Controller
{
    function getTask(Request $request)
    {
        $seq = $request->ip() . ' - ' . date("Y-m-d h:i:sa");
        $table_name = Helper::getRandomPeopleTableName();
//        $people = DB::table($table_name)->where('working', '')->where('status', 403)->where('find_count', '<', 2)->limit(10)->pluck('email');
        $people = DB::table($table_name)->where('working', '')->where('status', 0)->limit(10)->pluck('email');
        if (count($people) == 0) {
            $table_name = Helper::getRandomPeopleTableName();
        }
        DB::table($table_name)->whereIn('email', $people)->update(['working' => $seq]);
        return response()->json([$seq => $people]);
    }

    function getAccount(Request $request)
    {
        $account = Account::where('status', Null)->orWhere('status', config('token_status.active'))
            ->where('best_ip', $request->ip())->orderBy('updated_at')->first();
        if (!$account) {
            $account = Account::where('status', Null)->orWhere('status', config('token_status.active'))
                ->where('level', '>', 0)->orderBy('updated_at')->first();
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

        DB::beginTransaction();
        foreach ($arr as $key => $value) {
            $table_name = Helper::getPeopleTableName($key);
            $save_data = [
                'status'  => $value['status'],
                'working' => ''
            ];
            if (key_exists('errorCode', $value)) {
                $save_data['message'] = $value['message'];
            } else if (key_exists('publicProfileUrl', $value)) {
                $save_data['profile_url'] = $value['publicProfileUrl'];
            }
            DB::table($table_name)->whereEmail($key)->update($save_data);
            DB::table($table_name)->whereEmail($key)->increment('find_count');
        }
        DB::commit();
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
            $new_email = trim($request->input('account'));
            if (!empty($new_email)) {
                $account = new Account();
                $account->email = $new_email;
                $account->password = trim($request->input('password', env('LINKEDIN_PASSWORD')));
                //mark new account as in use
                $account->status = config('token_status.in_use');
                $account->best_ip = $request->ip();
                $account->level = 0;
                $account->save();
            }
        }
    }
}
