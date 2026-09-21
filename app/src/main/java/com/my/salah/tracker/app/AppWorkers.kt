package com.my.salah.tracker.app

import android.appwidget.AppWidgetManager
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import androidx.work.Constraints
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequest
import androidx.work.WorkManager
import androidx.work.Worker
import androidx.work.WorkerParameters
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import java.util.Calendar
import java.util.concurrent.TimeUnit

/**
 * Worker to refresh widget and date pointer every midnight.
 */
class MidnightWorker(
    context: Context,
    workerParams: WorkerParameters
) : Worker(context, workerParams) {

    override fun doWork(): Result {
        val context = applicationContext

        // ১. উইজেটকে ব্রডকাস্ট পাঠিয়ে রিফ্রেশ করা (নতুন দিনের ফাঁকা উইজেট দেখাবে)
        val intent = Intent(context, SalahWidget::class.java).apply {
            action = AppWidgetManager.ACTION_APPWIDGET_UPDATE
            val ids = AppWidgetManager.getInstance(context)
                .getAppWidgetIds(ComponentName(context, SalahWidget::class.java))
            putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, ids)
        }
        context.sendBroadcast(intent)

        // ২. আগামীকালের জন্য নিজেকে আবার শিডিউল করা
        scheduleNextMidnight(context)

        return Result.success()
    }

    companion object {
        @JvmStatic
        fun scheduleNextMidnight(context: Context) {
            val currentDate = Calendar.getInstance()
            val midnight = Calendar.getInstance().apply {
                set(Calendar.HOUR_OF_DAY, 0)
                set(Calendar.MINUTE, 0)
                set(Calendar.SECOND, 1)
                set(Calendar.MILLISECOND, 0)
                add(Calendar.DAY_OF_MONTH, 1)
            }

            val timeDiff = midnight.timeInMillis - currentDate.timeInMillis
            val midnightWork = OneTimeWorkRequest.Builder(MidnightWorker::class.java)
                .setInitialDelay(timeDiff, TimeUnit.MILLISECONDS)
                .addTag("midnight_refresh_tag")
                .build()

            WorkManager.getInstance(context).enqueueUniqueWork(
                "midnight_refresh_work",
                ExistingWorkPolicy.REPLACE,
                midnightWork
            )
        }
    }
}

/**
 * Background worker to flush queued offline changes to Firebase when online.
 */
class SyncWorker(
    context: Context,
    workerParams: WorkerParameters
) : Worker(context, workerParams) {

    override fun doWork(): Result {
        val sp = applicationContext.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
        val queue = sp.getString("offline_q", "") ?: ""
        val email = sp.getString("user_email", "") ?: ""

        if (queue.isEmpty() || email.isEmpty()) return Result.success()

        val safeEmail = email.replace(".", "_dot_").replace("@", "_at_")
        val items = queue.split(",")
        val dbUrl = "https://mysalahtracker-49a76-default-rtdb.firebaseio.com/users/"
        var allSuccess = true

        for (item in items) {
            if (item.trim().isEmpty()) continue
            val parts = item.split("|")
            if (parts.size == 3) {
                try {
                    val url = URL("$dbUrl$safeEmail/${parts[0]}_${parts[1]}.json")
                    val con = (url.openConnection() as HttpURLConnection).apply {
                        connectTimeout = 5000
                        readTimeout = 5000
                        requestMethod = "PUT"
                        setRequestProperty("Content-Type", "application/json")
                        doOutput = true
                    }
                    con.outputStream.use { os ->
                        os.write("\"${parts[2]}\"".toByteArray())
                    }
                    if (con.responseCode != 200) allSuccess = false
                } catch (e: Exception) {
                    allSuccess = false
                    break
                }
            }
        }

        if (allSuccess) {
            sp.edit().remove("offline_q").apply()
            return Result.success()
        }
        return Result.retry()
    }

    companion object {
        @JvmStatic
        fun enqueueSync(context: Context) {
            val syncWork = OneTimeWorkRequest.Builder(SyncWorker::class.java)
                .setConstraints(
                    Constraints.Builder()
                        .setRequiredNetworkType(NetworkType.CONNECTED)
                        .build()
                )
                .build()
            WorkManager.getInstance(context).enqueueUniqueWork(
                "auto_sync",
                ExistingWorkPolicy.REPLACE,
                syncWork
            )
        }
    }
}
