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

    private fun putJson(urlStr: String, jsonBody: String): Boolean {
        return try {
            val url = URL(urlStr)
            val con = (url.openConnection() as HttpURLConnection).apply {
                connectTimeout = 5000
                readTimeout = 5000
                requestMethod = "PUT"
                setRequestProperty("Content-Type", "application/json")
                doOutput = true
            }
            con.outputStream.use { os ->
                os.write(jsonBody.toByteArray())
            }
            con.responseCode in 200..299
        } catch (_: Exception) {
            false
        }
    }

    fun save(dateKey: String, prayerName: String, status: String) {
        val email = sp.getString("user_email", "") ?: ""
        if (email.isEmpty()) return
        val safeEmail = email.replace(".", "_dot_").replace("@", "_at_")
        val isTrue = status.equals("yes", ignoreCase = true) || status.equals("true", ignoreCase = true)
        val prayerList = listOf("fajr", "dhuhr", "asr", "maghrib", "isha", "witr")
        val pLower = prayerName.lowercase(java.util.Locale.US)

        thread {
            try {
                // 1. Flat root key (e.g. 2026-09-24_fajr.json = "yes")
                val flatUrl = "$dbUrl$safeEmail/${dateKey}_$prayerName.json"
                val ok1 = putJson(flatUrl, "\"$status\"")

                // 2. Nested web structure key (e.g. db/2026-09-24/core/fajr.json = true)
                val webUrl = when {
                    pLower.endsWith("_jamaat") -> {
                        val prayer = pLower.substringBefore("_jamaat")
                        "$dbUrl$safeEmail/db/$dateKey/jamaat/$prayer.json"
                    }
                    prayerList.contains(pLower) -> {
                        "$dbUrl$safeEmail/db/$dateKey/core/$pLower.json"
                    }
                    else -> {
                        val parts = pLower.split("_", limit = 2)
                        val prayer = parts[0]
                        val sub = if (parts.size > 1) parts[1] else prayer
                        if (listOf("asr", "isha", "witr").contains(prayer)) {
                            "$dbUrl$safeEmail/db/$dateKey/sunnah/$prayer.json"
                        } else {
                            "$dbUrl$safeEmail/db/$dateKey/extras/$prayer/$sub.json"
                        }
                    }
                }
                putJson(webUrl, isTrue.toString())

                if (ok1) {
                    sp.edit().putLong("last_sync", System.currentTimeMillis()).apply()
                } else {
                    enqueueOffline(dateKey, prayerName, status)
                }
            } catch (_: Exception) {
                enqueueOffline(dateKey, prayerName, status)
            }
        }
    }

    private fun enqueueOffline(dateKey: String, prayerName: String, status: String) {
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

    fun processOfflineQueue(onStart: Runnable?, onSuccess: Runnable?, onFail: Runnable?) {
        val q = sp.getString("offline_q", "") ?: ""
        val email = sp.getString("user_email", "") ?: ""
        if (q.isNotEmpty() && email.isNotEmpty()) {
            if (onStart != null) activity.runOnUiThread(onStart)
            val safeEmail = email.replace(".", "_dot_").replace("@", "_at_")
            val items = q.split(",")
            val prayerList = listOf("fajr", "dhuhr", "asr", "maghrib", "isha", "witr")

            thread {
                var success = true
                for (item in items) {
                    if (item.trim().isEmpty()) continue
                    val parts = item.split("|")
                    if (parts.size == 3) {
                        val dateKey = parts[0]
                        val prayerName = parts[1]
                        val status = parts[2]
                        val isTrue = status.equals("yes", ignoreCase = true) || status.equals("true", ignoreCase = true)
                        val pLower = prayerName.lowercase(java.util.Locale.US)

                        val flatOk = putJson("$dbUrl$safeEmail/${dateKey}_$prayerName.json", "\"$status\"")
                        if (!flatOk) success = false

                        val webUrl = when {
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
                        putJson(webUrl, isTrue.toString())
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
                    connectTimeout = 7000
                    readTimeout = 7000
                    requestMethod = "GET"
                }

                if (con.responseCode != 200) {
                    if (onFail != null) activity.runOnUiThread(onFail)
                    return@thread
                }

                val jsonResult = BufferedReader(InputStreamReader(con.inputStream)).use { it.readText() }

                if (jsonResult != "null" && jsonResult.startsWith("{")) {
                    try {
                        val obj = JSONObject(jsonResult)
                        val editor = sp.edit()
                        val dao = SalahDatabase.getDatabase(activity).salahDao()
                        val roomRecords = HashMap<String, SalahRecord>()
                        val prayerList = listOf("fajr", "dhuhr", "asr", "maghrib", "isha", "witr")

                        // 1. Parse Nested Web DB ("db": { "YYYY-MM-DD": { "core": ..., "jamaat": ..., "extras": ..., "sunnah": ... } })
                        if (obj.has("db") && !obj.isNull("db")) {
                            val dbObj = obj.optJSONObject("db")
                            if (dbObj != null) {
                                val dateKeys = dbObj.keys()
                                while (dateKeys.hasNext()) {
                                    val dKey = dateKeys.next()
                                    if (dKey.length == 10 && dKey.matches(Regex("\\d{4}-\\d{2}-\\d{2}"))) {
                                        val dayData = dbObj.optJSONObject(dKey) ?: continue
                                        val record = roomRecords.getOrPut(dKey) {
                                            dao.getRecordByDate(dKey) ?: SalahRecord(dKey)
                                        }

                                        // Core / Farz
                                        val coreObj = dayData.optJSONObject("core")
                                        if (coreObj != null) {
                                            for (p in prayerList) {
                                                if (coreObj.has(p)) {
                                                    val done = coreObj.optBoolean(p, false)
                                                    record.setFardStat(p, if (done) "yes" else "no")
                                                }
                                            }
                                        }

                                        // Jamaat
                                        val jamaatObj = dayData.optJSONObject("jamaat")
                                        if (jamaatObj != null) {
                                            for (p in prayerList) {
                                                if (jamaatObj.has(p)) {
                                                    val isJ = jamaatObj.optBoolean(p, true)
                                                    record.setJamaatStat(p, if (isJ) "yes" else "no")
                                                }
                                            }
                                        }

                                        // Extras (Fajr, Dhuhr, Maghrib)
                                        val extrasObj = dayData.optJSONObject("extras")
                                        if (extrasObj != null) {
                                            val pKeys = extrasObj.keys()
                                            while (pKeys.hasNext()) {
                                                val p = pKeys.next()
                                                val subObj = extrasObj.optJSONObject(p)
                                                if (subObj != null) {
                                                    val sKeys = subObj.keys()
                                                    while (sKeys.hasNext()) {
                                                        val s = sKeys.next()
                                                        val isDone = subObj.optBoolean(s, false)
                                                        editor.putBoolean("${dKey}_${p}_$s", isDone)
                                                    }
                                                }
                                            }
                                        }

                                        // Sunnah (Asr, Isha, Witr)
                                        val sunnahObj = dayData.optJSONObject("sunnah")
                                        if (sunnahObj != null) {
                                            val sKeys = sunnahObj.keys()
                                            while (sKeys.hasNext()) {
                                                val p = sKeys.next()
                                                val isDone = sunnahObj.optBoolean(p, false)
                                                editor.putBoolean("${dKey}_${p}_$p", isDone)
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // 2. Parse Flat Root Keys (e.g. "2026-09-24_fajr": "yes", "2026-09-24_fajr_jamaat": "yes")
                        val keys = obj.keys()
                        while (keys.hasNext()) {
                            val k = keys.next()
                            if (k == "auth" || k == "db") continue

                            val valStr = obj.optString(k, "")
                            val isTrue = valStr.equals("yes", ignoreCase = true) || valStr.equals("true", ignoreCase = true)

                            if (k.length >= 11 && k.matches(Regex("\\d{4}-\\d{2}-\\d{2}_.+"))) {
                                val date = k.substring(0, 10)
                                val remainder = k.substring(11).lowercase(java.util.Locale.US)

                                val record = roomRecords.getOrPut(date) {
                                    dao.getRecordByDate(date) ?: SalahRecord(date)
                                }

                                if (remainder.endsWith("_jamaat")) {
                                    val prayer = remainder.substringBefore("_jamaat")
                                    if (prayerList.contains(prayer)) {
                                        record.setJamaatStat(prayer, if (isTrue) "yes" else "no")
                                    }
                                } else if (prayerList.contains(remainder)) {
                                    // Case-insensitive match guarantees prayers are restored!
                                    record.setFardStat(remainder, if (isTrue) "yes" else "no")
                                } else {
                                    // Sunnah or extras key: strictly store as Boolean in SharedPreferences
                                    editor.putBoolean(k, isTrue)
                                }
                            }
                        }

                        // 3. Persist all records into native SQLite database
                        for (r in roomRecords.values) {
                            dao.insertRecord(r)
                        }

                        editor.putLong("last_sync", System.currentTimeMillis())
                        editor.apply()

                        if (onSuccess != null) activity.runOnUiThread(onSuccess)
                    } catch (_: Exception) {
                        if (onFail != null) activity.runOnUiThread(onFail)
                    }
                } else {
                    if (onFail != null) activity.runOnUiThread(onFail)
                }
            } catch (_: Exception) {
                if (onFail != null) activity.runOnUiThread(onFail)
            }
        }
    }

    fun loginWithEmail(email: String, onResult: (Boolean) -> Unit) {
        val trimmed = email.trim().lowercase(java.util.Locale.US)
        sp.edit()
            .putBoolean("is_logged_in", true)
            .putString("user_email", trimmed)
            .apply()

        fetchAndLoad(
            onStart = null,
            onSuccess = Runnable {
                processOfflineQueue(null, null, null)
                activity.runOnUiThread { onResult(true) }
            },
            onFail = Runnable {
                activity.runOnUiThread { onResult(true) }
            }
        )
    }

    fun loginAndSync(email: String, pass: String, onResult: (Boolean) -> Unit) {
        loginWithEmail(email, onResult)
    }
}
