package com.my.salah.tracker.app

import android.app.Activity
import android.content.SharedPreferences
import androidx.work.Constraints
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequest
import androidx.work.WorkManager
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import java.util.HashMap
import kotlin.concurrent.thread

class FirebaseManager(
    private val activity: Activity,
    private val sp: SharedPreferences
) {
    private val dbUrl = "https://mysalahtracker-49a76-default-rtdb.firebaseio.com/users/"

    fun save(dateKey: String, prayerName: String, status: String) {
        val email = sp.getString("user_email", "") ?: ""
        if (email.isEmpty()) return
        val safeEmail = email.replace(".", "_dot_").replace("@", "_at_")

        thread {
            try {
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
                con.responseCode
                sp.edit().putLong("last_sync", System.currentTimeMillis()).apply()
            } catch (e: Exception) {
                val q = sp.getString("offline_q", "") ?: ""
                sp.edit().putString("offline_q", "$q$dateKey|$prayerName|$status,").apply()

                val syncWork = OneTimeWorkRequest.Builder(SyncWorker::class.java)
                    .setConstraints(
                        Constraints.Builder()
                            .setRequiredNetworkType(NetworkType.CONNECTED)
                            .build()
                    )
                    .build()
                WorkManager.getInstance(activity).enqueueUniqueWork(
                    "auto_sync",
                    ExistingWorkPolicy.REPLACE,
                    syncWork
                )
            }
        }
    }

    fun processOfflineQueue(onStart: Runnable?, onSuccess: Runnable?, onFail: Runnable?) {
        val q = sp.getString("offline_q", "") ?: ""
        val email = sp.getString("user_email", "") ?: ""
        if (q.isNotEmpty() && email.isNotEmpty()) {
            if (onStart != null) activity.runOnUiThread(onStart)
            val safeEmail = email.replace(".", "_dot_").replace("@", "_at_")
            val items = q.split(",")

            thread {
                var success = true
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
                            if (con.responseCode != 200) {
                                success = false
                            }
                        } catch (e: Exception) {
                            success = false
                            break
                        }
                    }
                }
                if (success) {
                    sp.edit()
                        .putString("offline_q", "")
                        .putLong("last_sync", System.currentTimeMillis())
                        .apply()
                    if (onSuccess != null) activity.runOnUiThread(onSuccess)
                } else {
                    if (onFail != null) activity.runOnUiThread(onFail)
                }
            }
        }
    }

    fun fetchAndLoad(onStart: Runnable?, onSuccess: Runnable?, onFail: Runnable?) {
        val email = sp.getString("user_email", "") ?: ""
        if (email.isEmpty()) return
        val safeEmail = email.replace(".", "_dot_").replace("@", "_at_")
        if (onStart != null) activity.runOnUiThread(onStart)

        thread {
            try {
                val url = URL("$dbUrl$safeEmail.json")
                val con = (url.openConnection() as HttpURLConnection).apply {
                    connectTimeout = 5000
                    readTimeout = 5000
                    requestMethod = "GET"
                }

                val jsonResult = BufferedReader(InputStreamReader(con.inputStream)).use { it.readText() }

                // HYBRID SYNC: SharedPreferences + Room Database
                if (jsonResult != "null" && jsonResult.startsWith("{")) {
                    try {
                        val obj = JSONObject(jsonResult)
                        val editor = sp.edit()
                        val dao = SalahDatabase.getDatabase(activity).salahDao()
                        val roomRecords = HashMap<String, SalahRecord>()

                        val keys = obj.keys()
                        while (keys.hasNext()) {
                            val k = keys.next()
                            val valStr = obj.getString(k)
                            editor.putString(k, valStr)

                            if (k.length >= 10 && k.matches(Regex("\\d{4}-\\d{2}-\\d{2}.*"))) {
                                val date = k.substring(0, 10)
                                val type = k.substring(11)

                                val record = roomRecords.getOrPut(date) {
                                    dao.getRecordByDate(date) ?: SalahRecord(date)
                                }

                                when (type) {
                                    "Fajr" -> record.fajr = valStr
                                    "Dhuhr" -> record.dhuhr = valStr
                                    "Asr" -> record.asr = valStr
                                    "Maghrib" -> record.maghrib = valStr
                                    "Isha" -> record.isha = valStr
                                    "Witr" -> record.witr = valStr
                                }
                            }
                        }

                        for (r in roomRecords.values) {
                            dao.insertRecord(r)
                        }

                        editor.putLong("last_sync", System.currentTimeMillis())
                        editor.apply()

                        if (onSuccess != null) activity.runOnUiThread(onSuccess)
                    } catch (e: Exception) {
                        if (onFail != null) activity.runOnUiThread(onFail)
                    }
                } else {
                    if (onFail != null) activity.runOnUiThread(onFail)
                }
            } catch (e: Exception) {
                if (onFail != null) activity.runOnUiThread(onFail)
            }
        }
    }
}
