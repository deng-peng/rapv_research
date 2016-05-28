<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Http\Requests;

class PhoneTaskController extends Controller
{
    function getTask(Request $request)
    {
        $seq = $request->ip() . ' - ' . date("Y-m-d h:i:sa");
//        $people = DB::table($table_name)->where('working', '')->where('status', 403)->where('find_count', '<', 2)->limit(10)->pluck('email');
        $people = DB::table($table_name)->where('working', '')->where('status', 0)->limit(20)->pluck('email');
        if (count($people) == 0) {
            $table_name = Helper::getRandomPeopleTableName();
        }
        DB::table($table_name)->whereIn('email', $people)->update(['working' => $seq]);
        return response()->json([$seq => $people]);
    }

    function postResult(Request $request)
    {
        $result = $request->input('result');
        $arr = json_decode($result, true);

        DB::beginTransaction();
        foreach ($arr as $key => $value) {
            $table_name = Helper::getPeopleTableName($key);
            if (count($value) == 0) {
                continue;
            }
            $save_data = [
                'status'  => $value['status'],
                'working' => ''
            ];
            if (key_exists('errorCode', $value)) {
                $save_data['message'] = $value['message'];
            } else if (key_exists('publicProfileUrl', $value)) {
                $save_data['profile_url'] = $value['publicProfileUrl'];
            }
            $person = DB::table($table_name)->whereEmail($key)->first();
            if ($person) {
                $save_data['find_count'] = $person->find_count + 1;
                DB::table($table_name)->whereEmail($key)->update($save_data);
            } else {
                $save_data['email'] = $key;
                $save_data['find_count'] = 1;
                DB::table($table_name)->insert($save_data);
            }
        }
        DB::commit();
        return response('ok');
    }
}
