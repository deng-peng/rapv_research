<?php

namespace App\Http\Controllers;

use App\Slave;
use Illuminate\Http\Request;

use App\Http\Requests;

class SlaveController extends Controller
{
    function postStatus(Request $request)
    {
        $slave = Slave::firstOrNew(['ip' => $request->ip()]);
        $slave->status = $request->input('status', '');
        $slave->valid = true;
        $slave->save();
        return response('updated ' . $slave->id);
    }
}
