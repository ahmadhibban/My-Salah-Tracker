package com.my.salah.tracker.app

import android.content.Context
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
 * Worker to refresh date pointer every midnight.
 */
class MidnightWorker(
    context: Context,
    workerParams: WorkerParameters
) : Worker(context, workerParams) {

    override fun doWork(): Result {
        val context = applicationContext

        // আগামীকালের জন্য নিজেকে আবার শিডিউল করা
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
        val prayerList = listOf("fajr", "dhuhr", "asr", "maghrib", "isha", "witr")
        var allSuccess = true

        for (item in items) {
            if (item.trim().isEmpty()) continue
            val parts = item.split("|")
            if (parts.size == 3) {
                val dateKey = parts[0]
                val prayerName = parts[1]
                val status = parts[2]
                val isTrue = status.equals("yes", ignoreCase = true) || status.equals("true", ignoreCase = true)
                val pLower = prayerName.lowercase(java.util.Locale.US)

                try {
                    // 1. Flat key
                    val url = URL("$dbUrl$safeEmail/${dateKey}_$prayerName.json")
                    val con = (url.openConnection() as HttpURLConnection).apply {
                        connectTimeout = 5000
                        readTimeout = 5000
                        requestMethod = "PUT"
                        setRequestProperty("Content-Type", "application/json")
                        doOutput = true
                    }
                    con.outputStream.use { os ->
                        os.write("\"$status\"".toByteArray())
                    }
                    if (con.responseCode !in 200..299) allSuccess = false

                    // 2. Nested web key
                    val webUrlStr = when {
                        pLower.endsWith("_jamaat") -> {
                            val prayer = pLower.substringBefore("_jamaat")
                            "$dbUrl$safeEmail/db/$dateKey/jamaat/$prayer.json"
                        }
                        prayerList.contains(pLower) -> {
                            "$dbUrl$safeEmail/db/$dateKey/core/$pLower.json"
                        }
                        else -> {
                            val subParts = pLower.split("_", limit = 2)
                            val prayer = subParts[0]
                            val sub = if (subParts.size > 1) subParts[1] else prayer
                            if (listOf("asr", "isha", "witr").contains(prayer)) {
                                "$dbUrl$safeEmail/db/$dateKey/sunnah/$prayer.json"
                            } else {
                                "$dbUrl$safeEmail/db/$dateKey/extras/$prayer/$sub.json"
                            }
                        }
                    }
                    val webCon = (URL(webUrlStr).openConnection() as HttpURLConnection).apply {
                        connectTimeout = 5000
                        readTimeout = 5000
                        requestMethod = "PUT"
                        setRequestProperty("Content-Type", "application/json")
                        doOutput = true
                    }
                    webCon.outputStream.use { os ->
                        os.write(isTrue.toString().toByteArray())
                    }
                    webCon.responseCode
                } catch (_: Exception) {
                    allSuccess = false
                    break
                }
            }
        }

        if (allSuccess) {
            sp.edit().remove("offline_q").putLong("last_sync", System.currentTimeMillis()).apply()
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
