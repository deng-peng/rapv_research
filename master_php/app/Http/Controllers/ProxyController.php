<?php

namespace App\Http\Controllers;

use App\Proxy;
use Illuminate\Http\Request;

use App\Http\Requests;

class ProxyController extends Controller
{
    function getProxy(Request $request)
    {
        $proxy = Proxy::where('status', config('status.active'))->where('protocol','socks5')
            ->orderBy('updated_at', 'desc')->first();
        if ($proxy) {
            $proxy->status = config('status.in_use');
            $proxy->save();
            return response()->json($proxy);
        }
        return '';
    }

    function updateProxyStatus(Request $request)
    {
        $id = $request->input('id');
        $proxy = Proxy::findOrFail($id);
        $status = $request->input('status');
        if ($status == 'active') {
            $proxy->status = config('status.active');
        } elseif ($status == 'frozen') {
            $proxy->status = config('status.frozen');
        } elseif ($status == 'in_use') {
            $proxy->status = config('status.in_use');
        } elseif ($status == 'invalid') {
            $proxy->status = config('status.invalid');
        }
        $proxy->save();
    }
}
