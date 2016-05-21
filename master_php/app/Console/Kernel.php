<?php

namespace App\Console;

use DB;
use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    /**
     * The Artisan commands provided by your application.
     *
     * @var array
     */
    protected $commands = [
        // Commands\Inspire::class,
    ];

    /**
     * Define the application's command schedule.
     *
     * @param  \Illuminate\Console\Scheduling\Schedule $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        $schedule->call(function () {
            //mark slave server not running
            DB::update("update slaves set status = '== stopped ==' where updated_at + INTERVAL 60 MINUTE < NOW()");

            //frozen proxies after use
            DB::update("update proxies set status = -1 where status = 1 AND updated_at + INTERVAL 120 MINUTE < NOW()");
            //enable frozen proxies
            DB::update("update proxies set status = 0 where status = -1 AND updated_at + INTERVAL 24 HOUR < NOW()");
        })->everyTenMinutes();
    }
}
