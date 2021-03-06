<?php

namespace App\Http\Controllers;

use App\Slave;
use Illuminate\Http\Request;

use App\Http\Requests;

class SlaveController extends Controller
{
    function postStatus(Request $request)
    {
        $slave = Slave::firstOrNew(['ip' => $request->ip(), 'name' => $request->input('name')]);
        $slave->status = $request->input('status', '');
        $slave->valid = true;
        $slave->check_count = $request->input('check_count', 0);
        $slave->save();
        return response('updated ' . $slave->id);
    }

    function getStatus()
    {
        return view('status')->withSlaves(Slave::where('valid', true)->orderBy('ip')->orderBy('name')->get());
    }
}
