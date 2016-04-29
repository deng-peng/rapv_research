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
            //active accounts frozen for 5 hours
            DB::update('update accounts set status = 3 where status = -1 and updated_at + INTERVAL 5 HOUR < NOW()');

            //active accounts not report status for 30 minutes
            DB::update('update accounts set status = 3 where status = 1 and updated_at + INTERVAL 30 MINUTE < NOW()');

        })->everyTenMinutes();
    }
}
