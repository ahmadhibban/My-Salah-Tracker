package com.my.salah.tracker.app;

import android.appwidget.AppWidgetManager;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import androidx.annotation.NonNull;
import androidx.work.OneTimeWorkRequest;
import androidx.work.WorkManager;
import androidx.work.Worker;
import androidx.work.WorkerParameters;
import java.util.Calendar;
import java.util.concurrent.TimeUnit;

public class MidnightWorker extends Worker {

    public MidnightWorker(@NonNull Context context, @NonNull WorkerParameters workerParams) {
        super(context, workerParams);
    }

    @NonNull
    @Override
    public Result doWork() {
        Context context = getApplicationContext();

        // ১. উইজেটকে ব্রডকাস্ট পাঠিয়ে রিফ্রেশ করা (যাতে নতুন দিনের ফাঁকা উইজেট দেখায়)
        Intent intent = new Intent(context, SalahWidget.class);
        intent.setAction(AppWidgetManager.ACTION_APPWIDGET_UPDATE);
        int[] ids = AppWidgetManager.getInstance(context).getAppWidgetIds(new ComponentName(context, SalahWidget.class));
        intent.putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, ids);
        context.sendBroadcast(intent);

        // ২. আজকের কাজ শেষ, এবার আগামীকালের জন্য আবার নিজেকে সেট করে ঘুমিয়ে পড়া
        scheduleNextMidnight(context);

        return Result.success();
    }

    public static void scheduleNextMidnight(Context context) {
        Calendar currentDate = Calendar.getInstance();
        Calendar midnight = Calendar.getInstance();
        midnight.set(Calendar.HOUR_OF_DAY, 0);
        midnight.set(Calendar.MINUTE, 0);
        midnight.set(Calendar.SECOND, 1); // ঠিক রাত ১২টা বেজে ১ সেকেন্ড
        midnight.set(Calendar.MILLISECOND, 0);
        midnight.add(Calendar.DAY_OF_MONTH, 1); // আগামীকালের জন্য

        // রাত ১২টা বাজতে আর কতক্ষণ বাকি, তার হিসাব
        long timeDiff = midnight.getTimeInMillis() - currentDate.getTimeInMillis();

        OneTimeWorkRequest midnightWork = new OneTimeWorkRequest.Builder(MidnightWorker.class)
                .setInitialDelay(timeDiff, TimeUnit.MILLISECONDS)
                .addTag("midnight_refresh_tag")
                .build();

        // শিডিউল করে দেওয়া (REPLACE মানে আগে কোনো শিডিউল থাকলে সেটা মুছে নতুনটা বসবে)
        WorkManager.getInstance(context).enqueueUniqueWork(
                "midnight_refresh_work",
                androidx.work.ExistingWorkPolicy.REPLACE,
                midnightWork
        );
    }
}