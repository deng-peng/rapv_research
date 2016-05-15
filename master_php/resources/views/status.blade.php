@extends('layouts.app')

@section('content')
    <div class="container">
        <table class="table table-striped">
            <thead>
            <tr>
                <th>#</th>
                <th>IP Address</th>
                <th>Status</th>
                <th>Last Report</th>
                <th>Launched</th>
            </tr>
            </thead>
            <tbody>
            @foreach($slaves as $slave)
                <tr>
                    <th scope="row">{{ $slave->id }}</th>
                    <td>{{ $slave->ip }}</td>
                    <td>{{ $slave->status }}</td>
                    <td>{{ $slave->updated_at->diffForHumans(Carbon\Carbon::now()) }}</td>
                    <td>{{ $slave->created_at }}</td>
                </tr>
            @endforeach
            </tbody>
        </table>

    </div>
@endsection