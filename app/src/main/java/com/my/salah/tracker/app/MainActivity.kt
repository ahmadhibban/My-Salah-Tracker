package com.my.salah.tracker.app

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.my.salah.tracker.app.ui.*
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : ComponentActivity() {

    private lateinit var sp: SharedPreferences
    private lateinit var dao: SalahDao
    private lateinit var fbManager: FirebaseManager

    private val sdfKey = SimpleDateFormat("yyyy-MM-dd", Locale.US)
    private val prayers = listOf("fajr", "dhuhr", "asr", "maghrib", "isha", "witr")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        sp = getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
        dao = SalahDatabase.getDatabase(this).salahDao()
        fbManager = FirebaseManager(this, sp)

        setContent {
            SalahDashboardScreen()
        }
    }


    private fun getOrCreateRecord(dateKey: String): SalahRecord {
        var record = dao.getRecordByDate(dateKey)
        if (record == null) {
            record = SalahRecord(dateKey)
            dao.insertRecord(record)
        }
        return record
    }

    private fun calculateStreak(): Int {
        var streak = 0
        val cal = Calendar.getInstance()
        val todayKey = sdfKey.format(cal.time)
        val todayRecord = dao.getRecordByDate(todayKey)
        val isTodayAllDone = todayRecord != null && prayers.all { todayRecord.getFardStat(it) == "yes" }

        if (isTodayAllDone) {
            streak = 1
            cal.add(Calendar.DAY_OF_MONTH, -1)
            while (true) {
                val key = sdfKey.format(cal.time)
                val record = dao.getRecordByDate(key) ?: break
                if (prayers.all { record.getFardStat(it) == "yes" }) {
                    streak++
                    cal.add(Calendar.DAY_OF_MONTH, -1)
                } else {
                    break
                }
            }
        } else {
            cal.add(Calendar.DAY_OF_MONTH, -1)
            while (true) {
                val key = sdfKey.format(cal.time)
                val record = dao.getRecordByDate(key) ?: break
                if (prayers.all { record.getFardStat(it) == "yes" }) {
                    streak++
                    cal.add(Calendar.DAY_OF_MONTH, -1)
                } else {
                    break
                }
            }
        }
        return streak
    }

    @Composable
    private fun SalahDashboardScreen() {
        val today = remember { Date() }
        var selectedDate by remember { mutableStateOf(Date()) }
        val dateKey = remember(selectedDate) { sdfKey.format(selectedDate) }
        val isToday = remember(dateKey) { dateKey == sdfKey.format(today) }

        // State triggers to re-read database and SharedPreferences
        var updateTrigger by remember { mutableIntStateOf(0) }

        // Background auto-sync on app open
        LaunchedEffect(Unit) {
            if (sp.getBoolean("is_logged_in", false)) {
                fbManager.fetchAndLoad(
                    onStart = null,
                    onSuccess = Runnable {
                        fbManager.processOfflineQueue(null, null, null)
                        runOnUiThread { updateTrigger++ }
                    },
                    onFail = Runnable {
                        fbManager.processOfflineQueue(null, null, null)
                    }
                )
            }
        }

        val record = remember(dateKey, updateTrigger) {
            getOrCreateRecord(dateKey)
        }

        val streakDays = remember(updateTrigger) {
            calculateStreak()
        }

        val isLoggedIn = remember(updateTrigger) {
            sp.getBoolean("is_logged_in", false)
        }

        // Dialog State Holders
        var showCalendarDialog by remember { mutableStateOf(false) }
        var showFutureDateDialog by remember { mutableStateOf(false) }
        var showMarkOptionsDialog by remember { mutableStateOf(false) }
        var showStatsDialog by remember { mutableStateOf(false) }
        var showAuthDialog by remember { mutableStateOf(false) }
        var showTasbihLimitDialog by remember { mutableStateOf(false) }
        var currentTasbihLimit by remember { mutableIntStateOf(33) }
        var tasbihSaveCallback by remember { mutableStateOf<((Int) -> Unit)?>(null) }

        var sunnahExtrasTarget by remember {
            mutableStateOf<Triple<String, String, String>?>(null) // id, name, type
        }

        // Farz completion status
        val doneFarzCount = remember(record) {
            prayers.count { record.getFardStat(it) == "yes" }
        }
        val isAllMarked = doneFarzCount == prayers.size

        // Root Dashboard Container (Web matching background #E6E9EA)
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0xFFE6E9EA))
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 14.dp, vertical = 10.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                // 1. Neumorphic Header Row
                NeumorphicHeaderRow(
                    selectedDate = selectedDate,
                    streakDays = streakDays,
                    isLoggedIn = isLoggedIn,
                    onDateClick = { showCalendarDialog = true },
                    onAuthClick = { showAuthDialog = true }
                )

                // 2. Ultra 3D Tasbih Card
                UltraTasbihNeumorphicCard(
                    onOpenLimitDialog = { limit, onSave ->
                        currentTasbihLimit = limit
                        tasbihSaveCallback = onSave
                        showTasbihLimitDialog = true
                    }
                )

                // 3. Neumorphic Week Days Row
                NeumorphicWeekDaysRow(
                    selectedDate = selectedDate,
                    today = today,
                    onDateSelected = { newDate ->
                        selectedDate = newDate
                        updateTrigger++
                    },
                    onFutureDateAttempt = { showFutureDateDialog = true }
                )

                // 4. Neumorphic Actions Row
                NeumorphicActionsRow(
                    isAllMarked = isAllMarked,
                    isToday = isToday,
                    onMarkToggle = { showMarkOptionsDialog = true },
                    onStatsOrToday = {
                        if (isToday) {
                            showStatsDialog = true
                        } else {
                            selectedDate = Date()
                            updateTrigger++
                        }
                    }
                )

                // 5. 6 Neumorphic Prayer Cards (Filling entire remaining screen space evenly, NO empty gap)
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    PrayerPalettes.forEach { palette ->
                        val p = palette.id
                        val isCompleted = record.getFardStat(p) == "yes"
                        val isJamaat = record.getJamaatStat(p) == "yes"

                        // Calculate sub-text & sub-completion status
                        val (subText, isSubCompleted) = remember(palette, dateKey, updateTrigger) {
                            if (palette.type == "sunnah") {
                                val isDone = sp.getBoolean("${dateKey}_${p}_${p}", false)
                                val label = "Sunnah"
                                label to isDone
                            } else {
                                val items = when (p) {
                                    "fajr" -> listOf("sunnah_before", "ishraq", "chasht")
                                    "dhuhr" -> listOf("sunnah_before", "sunnah_after")
                                    "maghrib" -> listOf("sunnah_after", "awabin")
                                    else -> emptyList()
                                }
                                val doneCount = items.count { sp.getBoolean("${dateKey}_${p}_$it", false) }
                                val allDone = items.isNotEmpty() && doneCount == items.size
                                "Extras ($doneCount/${items.size})" to allDone
                            }
                        }

                        NeumorphicPrayerCard(
                            palette = palette,
                            isCompleted = isCompleted,
                            isJamaat = isJamaat,
                            subText = subText,
                            isSubCompleted = isSubCompleted,
                            onJamaatToggle = {
                                val newJ = if (isJamaat) "no" else "yes"
                                record.setJamaatStat(p, newJ)
                                dao.updateRecord(record)
                                fbManager.save(dateKey, "${p}_jamaat", newJ)
                                updateTrigger++
                            },
                            onSubClick = {
                                sunnahExtrasTarget = Triple(palette.id, palette.name, palette.type)
                            },
                            onCheckToggle = { newChecked ->
                                val newStat = if (newChecked) "yes" else "no"
                                record.setFardStat(p, newStat)
                                dao.updateRecord(record)
                                fbManager.save(dateKey, p, newStat)
                                updateTrigger++
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .weight(1f)
                        )
                    }
                }
            }

            // ==========================================
            // Compose Dialog Overlays
            // ==========================================
            if (showCalendarDialog) {
                CalendarNeumorphicDialog(
                    selectedDate = selectedDate,
                    today = today,
                    onDismiss = { showCalendarDialog = false },
                    onDateSelected = { newDate ->
                        selectedDate = newDate
                        updateTrigger++
                    },
                    onFutureDateAttempt = {
                        showCalendarDialog = false
                        showFutureDateDialog = true
                    }
                )
            }

            if (showFutureDateDialog) {
                FutureDateWarningNeumorphicDialog(
                    onDismiss = { showFutureDateDialog = false }
                )
            }

            if (showTasbihLimitDialog) {
                TasbihLimitNeumorphicDialog(
                    currentLimit = currentTasbihLimit,
                    onDismiss = { showTasbihLimitDialog = false },
                    onSave = { newLimit ->
                        tasbihSaveCallback?.invoke(newLimit)
                    }
                )
            }

            if (showMarkOptionsDialog) {
                MarkOptionsNeumorphicDialog(
                    isMark = !isAllMarked,
                    onDismiss = { showMarkOptionsDialog = false },
                    onExecute = { scope ->
                        val stat = if (!isAllMarked) "yes" else "no"
                        val boolStat = !isAllMarked

                        if (scope == "farz" || scope == "all") {
                            for (p in prayers) {
                                record.setFardStat(p, stat)
                                fbManager.save(dateKey, p, stat)
                            }
                            dao.updateRecord(record)
                        }

                        if (scope == "all") {
                            val editor = sp.edit()
                            // Fajr
                            editor.putBoolean("${dateKey}_fajr_sunnah_before", boolStat)
                            editor.putBoolean("${dateKey}_fajr_ishraq", boolStat)
                            editor.putBoolean("${dateKey}_fajr_chasht", boolStat)
                            // Dhuhr
                            editor.putBoolean("${dateKey}_dhuhr_sunnah_before", boolStat)
                            editor.putBoolean("${dateKey}_dhuhr_sunnah_after", boolStat)
                            // Asr
                            editor.putBoolean("${dateKey}_asr_asr", boolStat)
                            // Maghrib
                            editor.putBoolean("${dateKey}_maghrib_sunnah_after", boolStat)
                            editor.putBoolean("${dateKey}_maghrib_awabin", boolStat)
                            // Isha
                            editor.putBoolean("${dateKey}_isha_isha", boolStat)
                            // Witr
                            editor.putBoolean("${dateKey}_witr_witr", boolStat)
                            editor.apply()

                            val sunnahKeys = listOf(
                                "fajr_sunnah_before", "fajr_ishraq", "fajr_chasht",
                                "dhuhr_sunnah_before", "dhuhr_sunnah_after",
                                "asr_asr",
                                "maghrib_sunnah_after", "maghrib_awabin",
                                "isha_isha",
                                "witr_witr"
                            )
                            val syncVal = if (boolStat) "yes" else "no"
                            for (sKey in sunnahKeys) {
                                fbManager.save(dateKey, sKey, syncVal)
                            }
                        }

                        updateTrigger++
                    }
                )
            }

            if (showStatsDialog) {
                WeeklyStatsNeumorphicDialog(
                    selectedDate = selectedDate,
                    sp = sp,
                    dao = dao,
                    onDismiss = { showStatsDialog = false }
                )
            }

            if (showAuthDialog) {
                AuthNeumorphicDialog(
                    sp = sp,
                    fbManager = fbManager,
                    onDismiss = { showAuthDialog = false },
                    onAuthChanged = { updateTrigger++ }
                )
            }

            sunnahExtrasTarget?.let { (pId, pName, pType) ->
                SunnahExtrasNeumorphicDialog(
                    prayerId = pId,
                    prayerName = pName,
                    prayerType = pType,
                    dateKey = dateKey,
                    sp = sp,
                    fbManager = fbManager,
                    onDismiss = { sunnahExtrasTarget = null },
                    onDone = { updateTrigger++ }
                )
            }
        }
    }
}
