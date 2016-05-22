@extends('layouts.app')

@section('content')
    <div class="container">
        <h3>Cookie status</h3>
        <div class="row">
            <div class="col-md-6">
                <ul class="list-group" id="cookie_list">
                </ul>
            </div>
        </div>
        <h3>Slave status</h3>
        <table class="table table-striped">
            <thead>
            <tr>
                <th>IP Address</th>
                <th>Thread</th>
                <th>Status</th>
                <th>Last Report</th>
                <th>Check Count</th>
            </tr>
            </thead>
            <tbody>
            <?php $last_ip = ''; ?>
            @foreach($slaves as $slave)
                <tr>
                    @if($last_ip == $slave->ip)
                        <td></td>
                    @else
                        <td>{{ $slave->ip }}</td>
                        <?php $last_ip = $slave->ip; ?>
                    @endif
                    <td>{{ $slave->name }}</td>
                    <td>{{ $slave->status }}</td>
                    <td>{{ $slave->updated_at->diffForHumans(Carbon\Carbon::now()) }}</td>
                    <td>{{ $slave->check_count }}</td>
                </tr>
            @endforeach
            </tbody>
        </table>
    </div>

@endsection

@section('script')
    <script>
        $.get('{{ env('ACCOUNT_SERVER') }}/api/cookie/status', function (res) {
            var html = '';
            for (var key in res) {
                html += '<li class="list-group-item"><span class="badge">' + res[key] + '</span>' + key + '</li>';
            }
            $('#cookie_list').append(html);
        });
    </script>
@endsection