package com.my.salah.tracker.app

import android.animation.AnimatorSet
import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.content.SharedPreferences
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.text.InputType
import android.text.TextUtils
import android.view.Gravity
import android.view.HapticFeedbackConstants
import android.view.View
import android.view.animation.OvershootInterpolator
import android.widget.Button
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import java.util.Calendar
import java.util.Date

/**
 * Clean, modular dialog manager providing all 12 dialogs for the main application.
 */
object MainDialogs {

    fun showJamaatDialog(
        activity: Activity,
        jKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onDone: () -> Unit
    ) {
        val isBn = sp.getString("app_lang", "en") == "bn"
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 25, 30)

        val title = TextView(activity).apply {
            text = if (isBn) "কিভাবে পড়েছেন?" else "How did you pray?"
            setTextColor(colorAccent)
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        val sv = ScrollView(activity)
        val list = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL }

        val opts = if (isBn) arrayOf("জামাতের সাথে", "একাকী") else arrayOf("Jamaat", "Alone")
        val vals = arrayOf("jamaat", "alone")
        val curType = sp.getString(jKey, "jamaat") ?: "jamaat"

        for (s in opts.indices) {
            val sName = opts[s]
            val sVal = vals[s]
            val sChecked = curType == sVal

            val row = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                val padH = activity.dp(10)
                val padV = activity.dp(12)
                setPadding(padH, padV, padH, padV)
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, activity.dp(10))
                }
                background = createDrawable(if (sChecked) themeColors[4] else Color.TRANSPARENT, activity.dp(15).toFloat())
            }

            val tv = TextView(activity).apply {
                text = sName
                setTextColor(if (sChecked) colorAccent else themeColors[2])
                textSize = 16f
                typeface = if (sChecked) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            }
            val chk = ui.getPremiumCheckbox(if (sChecked) "yes" else "no", colorAccent)
            row.addView(tv)
            row.addView(chk)
            list.addView(row)

            row.setOnClickListener { v ->
                v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                sp.edit().putString(jKey, sVal).apply()
                container.dialog.dismiss()
                onDone()
            }
        }

        sv.addView(list)
        container.contentLayout.addView(sv, LinearLayout.LayoutParams(-1, -2, 1f))

        val closeBtn = TextView(activity).apply {
            text = lang.get("Done")
            setTextColor(Color.parseColor("#F1F5F9"))
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            val padV = activity.dp(15)
            setPadding(0, padV, 0, padV)
            background = createDrawable(colorAccent, activity.dp(20).toFloat())
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, activity.dp(15), 0, 0)
            }
            setOnClickListener { container.dialog.dismiss() }
        }
        container.contentLayout.addView(closeBtn)

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showRakatEditDialog(
        activity: Activity,
        globKey: String,
        titleStr: String,
        currentRakat: Int,
        themeColors: IntArray,
        colorAccent: Int,
        appFonts: Array<Typeface?>,
        sp: SharedPreferences,
        onDone: () -> Unit
    ) {
        val isBn = sp.getString("app_lang", "en") == "bn"
        val container = activity.createCustomDialog(themeColors[1], 25f, 300, 25, 30)

        val title = TextView(activity).apply {
            text = "$titleStr - " + (if (isBn) "রাকাত সেট করুন" else "Set Rakat")
            setTextColor(colorAccent)
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        val rakIn = EditText(activity).apply {
            setText(currentRakat.toString())
            inputType = InputType.TYPE_CLASS_NUMBER
            setTextColor(themeColors[2])
            gravity = Gravity.CENTER
            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
            val padH = activity.dp(20)
            val padV = activity.dp(15)
            setPadding(padH, padV, padH, padV)
        }
        container.contentLayout.addView(rakIn, LinearLayout.LayoutParams(-1, -2).apply {
            setMargins(0, 0, 0, activity.dp(25))
        })

        val btn = Button(activity).apply {
            text = if (isBn) "সেট করুন" else "Set Rakat"
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            isAllCaps = false
            background = createDrawable(colorAccent, activity.dp(20).toFloat())
        }
        container.contentLayout.addView(btn, LinearLayout.LayoutParams(-1, activity.dp(55)))

        btn.setOnClickListener {
            val rStr = rakIn.text.toString().trim()
            if (rStr.isNotEmpty()) {
                try {
                    sp.edit().putInt(globKey, rStr.toInt()).apply()
                    container.dialog.dismiss()
                    onDone()
                } catch (e: Exception) {
                }
            }
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showExcuseDialog(
        activity: Activity,
        selectedDateKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        isDarkTheme: Boolean,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        fbHelper: FirebaseManager,
        onDone: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 30f, 300, 25, 30)

        val iconView = ui.getRoundImage(
            "img_period", 12,
            Color.parseColor(if (isDarkTheme) "#331520" else "#FCE4EC"),
            Color.parseColor("#D81B60")
        ).apply {
            val size = activity.dp(55)
            layoutParams = LinearLayout.LayoutParams(size, size).apply {
                gravity = Gravity.CENTER_HORIZONTAL
            }
        }
        container.contentLayout.addView(iconView)

        val title = TextView(activity).apply {
            text = lang.get("Excused Mode")
            setTextColor(colorAccent)
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, activity.dp(15), 0, activity.dp(10))
        }
        container.contentLayout.addView(title)

        val dao = SalahDatabase.getInstance(activity).salahDao()
        val todayRec = dao.getRecordByDate(selectedDateKey) ?: SalahRecord(selectedDateKey)
        val isAlreadyExcused = AppConstants.PRAYERS.all { todayRec.getFardStat(it) == "excused" }

        val sub = TextView(activity).apply {
            text = lang.get(
                if (isAlreadyExcused) "Prayers are currently marked as excused."
                else "Mark today's prayers as excused. Streak will not break."
            )
            gravity = Gravity.CENTER
            setTextColor(themeColors[3])
            textSize = 11f
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(sub)

        val actionBtn = Button(activity).apply {
            text = lang.get(if (isAlreadyExcused) "Remove Excused Status" else "Mark Today as Excused")
            isAllCaps = false
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            background = createDrawable(colorAccent, activity.dp(20).toFloat())
        }
        container.contentLayout.addView(actionBtn, LinearLayout.LayoutParams(-1, activity.dp(50)))

        actionBtn.setOnClickListener {
            val newVal = if (isAlreadyExcused) "no" else "excused"
            for (p in AppConstants.PRAYERS) {
                todayRec.setFardStat(p, newVal)
                sp.edit().putString("${selectedDateKey}_$p", newVal).apply()
                fbHelper.save(selectedDateKey, p, newVal)
            }
            dao.updateRecord(todayRec)
            container.dialog.dismiss()
            onDone()
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showSettingsMenu(
        activity: Activity,
        selectedDateKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        activeTheme: Int,
        isDarkTheme: Boolean,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        statsHelper: StatsHelper,
        backupHelper: BackupHelper,
        onReload: () -> Unit,
        onShowQazaList: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 20, 25)

        val title = TextView(activity).apply {
            text = lang.get("Settings & Options")
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        fun addRow(titleStr: String, imgName: String, action: () -> Unit) {
            val btn = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                val pad = activity.dp(15)
                setPadding(pad, pad, pad, pad)
                background = createDrawable(themeColors[4], activity.dp(15).toFloat())
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, activity.dp(10))
                }
            }
            val icon = ui.getRoundImage(imgName, 0, Color.TRANSPARENT, colorAccent).apply {
                val s = activity.dp(28)
                layoutParams = LinearLayout.LayoutParams(s, s).apply {
                    setMargins(0, 0, activity.dp(15), 0)
                }
            }
            btn.addView(icon)

            val t = TextView(activity).apply {
                text = lang.get(titleStr)
                setTextColor(themeColors[2])
                textSize = 16f
                typeface = Typeface.DEFAULT_BOLD
            }
            btn.addView(t)
            btn.setOnClickListener {
                container.dialog.dismiss()
                action()
            }
            container.contentLayout.addView(btn)
        }

        val isBn = sp.getString("app_lang", "en") == "bn"

        // Theme / Dark mode
        addRow(if (isBn) "কালার ও থিম পরিবর্তন" else "Change Color & Theme", if (isDarkTheme) "ic_sun" else "ic_moon") {
            showThemeSelector(activity, themeColors, colorAccent, activeTheme, isDarkTheme, isBn, sp, appFonts, selectedDateKey)
        }

        // Date adjusters
        addRow(if (isBn) "তারিখ এডজাস্ট (আরবি/বাংলা)" else "Adjust Date (+/-)", "img_moon") {
            showDateAdjuster(activity, themeColors, colorAccent, isBn, sp, appFonts, onReload)
        }

        // Stats
        addRow("Advanced Statistics", "img_stats") {
            try {
                statsHelper.syncDate(AppDateUtils.parseYmd(selectedDateKey) ?: Date())
            } catch (e: Exception) {
            }
            statsHelper.showStatsOptionsDialog()
        }

        // Backup & Sync
        addRow(if (isBn) "ব্যাকআপ এবং সিঙ্ক" else "Backup & Sync", "img_cloud") {
            backupHelper.showProfileDialog(Runnable { onReload() })
        }

        // Language toggle
        addRow("Change Language", "img_lang") {
            val nextL = if (sp.getString("app_lang", "en") == "en") "bn" else "en"
            sp.edit().putString("app_lang", nextL).apply()
            activity.finish()
            val intent = Intent(activity, MainActivity::class.java).apply {
                putExtra("RESTORE_DATE", AppDateUtils.parseYmd(selectedDateKey)?.time ?: Date().time)
            }
            activity.startActivity(intent)
            if (Build.VERSION.SDK_INT >= 34) {
                activity.overrideActivityTransition(Activity.OVERRIDE_TRANSITION_OPEN, 0, 0)
            } else {
                @Suppress("DEPRECATION")
                activity.overridePendingTransition(0, 0)
            }
        }

        // Qaza list
        addRow(if (isBn) "কাজা নামাজের তালিকা" else "View Qaza List", "img_custom_qaza") {
            onShowQazaList()
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    private fun showThemeSelector(
        activity: Activity,
        themeColors: IntArray,
        colorAccent: Int,
        activeTheme: Int,
        isDarkTheme: Boolean,
        isBn: Boolean,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        selectedDateKey: String
    ) {
        val container = activity.createCustomDialog(themeColors[1], 20f, 300, 25, 30)
        val title = TextView(activity).apply {
            text = if (isBn) "নির্বাচন করুন" else "Select Option"
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        val copts = if (isBn) arrayOf("ডার্ক/লাইট মোড (Dark/Light)", "কালার পরিবর্তন (Change Color)")
                    else arrayOf("Dark/Light Mode", "Change Theme Color")

        for (i in copts.indices) {
            val w = i
            val box = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                val pad = activity.dp(15)
                setPadding(pad, pad, pad, pad)
                background = createDrawable(themeColors[4], activity.dp(15).toFloat())
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, activity.dp(10))
                }
            }
            val dot = View(activity).apply {
                background = createDrawable(colorAccent, shape = GradientDrawable.OVAL)
                val s = activity.dp(8)
                layoutParams = LinearLayout.LayoutParams(s, s).apply {
                    setMargins(0, 0, activity.dp(15), 0)
                }
            }
            val tv = TextView(activity).apply {
                text = copts[i]
                setTextColor(themeColors[2])
                textSize = 16f
                typeface = Typeface.DEFAULT_BOLD
            }
            box.addView(dot)
            box.addView(tv)
            container.contentLayout.addView(box)

            box.setOnClickListener {
                if (w == 0) {
                    sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply()
                } else {
                    sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply()
                }
                container.dialog.dismiss()
                activity.finish()
                if (Build.VERSION.SDK_INT >= 34) {
                    activity.overrideActivityTransition(Activity.OVERRIDE_TRANSITION_OPEN, 0, 0)
                } else {
                    @Suppress("DEPRECATION")
                    activity.overridePendingTransition(0, 0)
                }
                val intent = Intent(activity, MainActivity::class.java).apply {
                    putExtra("RESTORE_DATE", AppDateUtils.parseYmd(selectedDateKey)?.time ?: Date().time)
                }
                activity.startActivity(intent)
            }
        }
        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        container.dialog.show()
    }

    private fun showDateAdjuster(
        activity: Activity,
        themeColors: IntArray,
        colorAccent: Int,
        isBn: Boolean,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onReload: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 20f, 300, 25, 30)
        val title = TextView(activity).apply {
            text = if (isBn) "ক্যালেন্ডার নির্বাচন" else "Select Calendar"
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        val ops = if (isBn) arrayOf("আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)")
                  else arrayOf("Hijri Date", "Bengali Date")

        for (i in ops.indices) {
            val w = i
            val box = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                val pad = activity.dp(15)
                setPadding(pad, pad, pad, pad)
                background = createDrawable(themeColors[4], activity.dp(15).toFloat())
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, activity.dp(10))
                }
            }
            val dot = View(activity).apply {
                background = createDrawable(colorAccent, shape = GradientDrawable.OVAL)
                val s = activity.dp(8)
                layoutParams = LinearLayout.LayoutParams(s, s).apply {
                    setMargins(0, 0, activity.dp(15), 0)
                }
            }
            val tv = TextView(activity).apply {
                text = ops[i]
                setTextColor(themeColors[2])
                textSize = 16f
                typeface = Typeface.DEFAULT_BOLD
            }
            box.addView(dot)
            box.addView(tv)
            container.contentLayout.addView(box)

            box.setOnClickListener {
                container.dialog.dismiss()
                val isHijri = w == 0
                val pKey = if (isHijri) "hijri_offset" else "bn_date_offset"
                val subContainer = activity.createCustomDialog(themeColors[1], 20f, 300, 25, 30)

                val subTitle = TextView(activity).apply {
                    text = if (isHijri) (if (isBn) "আরবি তারিখ এডজাস্ট" else "Adjust Hijri")
                           else (if (isBn) "বাংলা তারিখ এডজাস্ট" else "Adjust Bengali")
                    setTextColor(themeColors[2])
                    textSize = 18f
                    typeface = Typeface.DEFAULT_BOLD
                    setPadding(0, 0, 0, activity.dp(15))
                }
                subContainer.contentLayout.addView(subTitle)

                val subOpts = if (isBn) arrayOf("-১ দিন (গতকাল)", "ডিফল্ট (০)", "+১ দিন (আগামীকাল)")
                              else arrayOf("-1 Day (Yesterday)", "Default (0)", "+1 Day (Tomorrow)")
                val vals = intArrayOf(-1, 0, 1)
                val currentVal = sp.getInt(pKey, 0)

                for (j in 0 until 3) {
                    val sj = j
                    val isMatch = vals[sj] == currentVal
                    val sBox = LinearLayout(activity).apply {
                        orientation = LinearLayout.HORIZONTAL
                        gravity = Gravity.CENTER_VERTICAL
                        val pad = activity.dp(15)
                        setPadding(pad, pad, pad, pad)
                        background = createDrawable(if (isMatch) colorAccent else themeColors[4], activity.dp(15).toFloat())
                        layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                            setMargins(0, 0, 0, activity.dp(10))
                        }
                    }
                    val sDot = View(activity).apply {
                        background = createDrawable(if (isMatch) Color.WHITE else colorAccent, shape = GradientDrawable.OVAL)
                        val s = activity.dp(8)
                        layoutParams = LinearLayout.LayoutParams(s, s).apply {
                            setMargins(0, 0, activity.dp(15), 0)
                        }
                    }
                    val sTv = TextView(activity).apply {
                        text = subOpts[sj]
                        setTextColor(if (isMatch) Color.WHITE else themeColors[2])
                        textSize = 16f
                        typeface = Typeface.DEFAULT_BOLD
                    }
                    sBox.addView(sDot)
                    sBox.addView(sTv)
                    subContainer.contentLayout.addView(sBox)

                    sBox.setOnClickListener {
                        sp.edit().putInt(pKey, vals[sj]).apply()
                        onReload()
                        subContainer.dialog.dismiss()
                    }
                }
                subContainer.contentLayout.applyFont(appFonts[0], appFonts[1])
                subContainer.dialog.show()
            }
        }
        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        container.dialog.show()
    }

    fun showQazaListDialog(
        activity: Activity,
        themeColors: IntArray,
        colorAccent: Int,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onDone: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 0, 30)

        val title = TextView(activity).apply {
            text = lang.get("View Qaza List")
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        val scroll = ScrollView(activity)
        val list = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val pad = activity.dp(20)
            setPadding(pad, 0, pad, 0)
        }

        val cal = Calendar.getInstance()
        var qazaCount = 0
        val dao = SalahDatabase.getInstance(activity).salahDao()

        for (i in 0 until 365) {
            val dK = AppDateUtils.formatYmd(cal.time)
            val r = dao.getRecordByDate(dK)
            if (r != null) {
                for (p in AppConstants.PRAYERS) {
                    if (r.getQazaStat(p) && r.getFardStat(p) == "no") {
                        qazaCount++
                        val row = LinearLayout(activity).apply {
                            orientation = LinearLayout.HORIZONTAL
                            gravity = Gravity.CENTER_VERTICAL
                            val pad = activity.dp(15)
                            setPadding(pad, pad, pad, pad)
                            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
                            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                                setMargins(0, 0, 0, activity.dp(10))
                            }
                        }

                        val tLay = LinearLayout(activity).apply {
                            orientation = LinearLayout.VERTICAL
                            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
                        }
                        val t1 = TextView(activity).apply {
                            text = lang.get(p)
                            setTextColor(themeColors[2])
                            textSize = 16f
                            typeface = Typeface.DEFAULT_BOLD
                        }
                        val t2 = TextView(activity).apply {
                            text = lang.getShortGreg(cal.time)
                            setTextColor(themeColors[3])
                            textSize = 12f
                        }
                        tLay.addView(t1)
                        tLay.addView(t2)
                        row.addView(tLay)

                        val btn = TextView(activity).apply {
                            text = lang.get("Done")
                            setTextColor(colorAccent)
                            typeface = Typeface.DEFAULT_BOLD
                            val padH = activity.dp(15)
                            val padV = activity.dp(8)
                            setPadding(padH, padV, padH, padV)
                            background = createDrawable(themeColors[5], activity.dp(10).toFloat())
                        }
                        row.addView(btn)

                        btn.setOnClickListener {
                            r.setQazaStat(p, false)
                            r.setFardStat(p, "yes")
                            dao.updateRecord(r)
                            sp.edit()
                                .putBoolean("${dK}_${p}_qaza", false)
                                .putString("${dK}_$p", "yes")
                                .apply()
                            list.removeView(row)
                            onDone()
                        }
                        list.addView(row)
                    }
                }
            }
            cal.add(Calendar.DATE, -1)
        }

        if (qazaCount == 0) {
            val customEmptyIcon = ui.getRoundImage("img_empty_qaza", 0, Color.TRANSPARENT, colorAccent).apply {
                val size = activity.dp(80)
                layoutParams = LinearLayout.LayoutParams(size, size).apply {
                    gravity = Gravity.CENTER
                    setMargins(0, activity.dp(20), 0, activity.dp(10))
                }
            }
            list.addView(customEmptyIcon)

            val empty = TextView(activity).apply {
                text = lang.get("Alhamdulillah! No pending Qaza.")
                setTextColor(themeColors[3])
                gravity = Gravity.CENTER
                setPadding(0, 0, 0, activity.dp(20))
            }
            list.addView(empty)
        }

        scroll.addView(list)
        container.contentLayout.addView(scroll, LinearLayout.LayoutParams(-1, activity.dp(300)))

        val closeBtn = TextView(activity).apply {
            text = lang.get("CLOSE")
            setTextColor(themeColors[3])
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, activity.dp(20), 0, 0)
            setOnClickListener { container.dialog.dismiss() }
        }
        container.contentLayout.addView(closeBtn)

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showMarkOptions(
        activity: Activity,
        selectedDateKey: String,
        themeColors: IntArray,
        appFonts: Array<Typeface?>,
        sp: SharedPreferences,
        fbHelper: FirebaseManager,
        lang: LanguageEngine,
        onDone: () -> Unit,
        onShowSuccess: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 25, 30)

        val title = TextView(activity).apply {
            text = lang.get("Mark Options")
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        fun createOptBtn(txt: String, textColor: Int): TextView = TextView(activity).apply {
            text = lang.get(txt)
            setTextColor(textColor)
            textSize = 16f
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            val padH = activity.dp(15)
            val padV = activity.dp(20)
            setPadding(padH, padV, padH, padV)
            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
        }

        val t1 = createOptBtn("Fard Only (6 Prayers)", themeColors[2])
        container.contentLayout.addView(t1)

        val t2 = createOptBtn("Include All Sunnahs", themeColors[2]).apply {
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, activity.dp(10), 0, 0)
            }
        }
        container.contentLayout.addView(t2)

        val dao = SalahDatabase.getInstance(activity).salahDao()
        t1.setOnClickListener {
            val r = dao.getRecordByDate(selectedDateKey) ?: SalahRecord(selectedDateKey)
            for (p in AppConstants.PRAYERS) {
                r.setFardStat(p, "yes")
                r.setQazaStat(p, false)
                sp.edit().putString("${selectedDateKey}_$p", "yes").apply()
                sp.edit().putBoolean("${selectedDateKey}_${p}_qaza", false).apply()
                fbHelper.save(selectedDateKey, p, "yes")
            }
            dao.insertRecord(r)
            container.dialog.dismiss()
            onDone()
            onShowSuccess()
        }

        t2.setOnClickListener {
            val r = dao.getRecordByDate(selectedDateKey) ?: SalahRecord(selectedDateKey)
            for (i in AppConstants.PRAYERS.indices) {
                val prayer = AppConstants.PRAYERS[i]
                r.setFardStat(prayer, "yes")
                r.setQazaStat(prayer, false)
                sp.edit().putString("${selectedDateKey}_$prayer", "yes").apply()
                sp.edit().putBoolean("${selectedDateKey}_${prayer}_qaza", false).apply()
                fbHelper.save(selectedDateKey, prayer, "yes")

                for (exKey in AppConstants.EXTRA_DB_KEYS) {
                    sp.edit().putString("${selectedDateKey}_$exKey", "yes").apply()
                    fbHelper.save(selectedDateKey, exKey, "yes")
                }
                for (sName in AppConstants.SUNNAHS[i]) {
                    sp.edit().putString("${selectedDateKey}_${prayer}_Sunnah_$sName", "yes").apply()
                    fbHelper.save(selectedDateKey, "${prayer}_Sunnah_$sName", "yes")
                }
            }
            dao.insertRecord(r)
            container.dialog.dismiss()
            onDone()
            onShowSuccess()
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showUnmarkOptions(
        activity: Activity,
        selectedDateKey: String,
        themeColors: IntArray,
        appFonts: Array<Typeface?>,
        sp: SharedPreferences,
        fbHelper: FirebaseManager,
        lang: LanguageEngine,
        onDone: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 25, 30)

        val title = TextView(activity).apply {
            text = lang.get("Unmark Options")
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        fun createOptBtn(txt: String, textColor: Int): TextView = TextView(activity).apply {
            text = lang.get(txt)
            setTextColor(textColor)
            textSize = 16f
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            val padH = activity.dp(15)
            val padV = activity.dp(20)
            setPadding(padH, padV, padH, padV)
            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
        }

        val t1 = createOptBtn("Remove Fard Only", themeColors[2])
        container.contentLayout.addView(t1)

        val t2 = createOptBtn("Remove All (Inc. Sunnah)", Color.parseColor("#FF5252")).apply {
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, activity.dp(10), 0, 0)
            }
        }
        container.contentLayout.addView(t2)

        val dao = SalahDatabase.getInstance(activity).salahDao()
        t1.setOnClickListener {
            val r = dao.getRecordByDate(selectedDateKey) ?: SalahRecord(selectedDateKey)
            for (p in AppConstants.PRAYERS) {
                r.setFardStat(p, "no")
                sp.edit().putString("${selectedDateKey}_$p", "no").apply()
                fbHelper.save(selectedDateKey, p, "no")
            }
            dao.insertRecord(r)
            container.dialog.dismiss()
            onDone()
        }

        t2.setOnClickListener {
            val r = dao.getRecordByDate(selectedDateKey) ?: SalahRecord(selectedDateKey)
            for (i in AppConstants.PRAYERS.indices) {
                val prayer = AppConstants.PRAYERS[i]
                r.setFardStat(prayer, "no")
                sp.edit().putString("${selectedDateKey}_$prayer", "no").apply()
                fbHelper.save(selectedDateKey, prayer, "no")

                for (exKey in AppConstants.EXTRA_DB_KEYS) {
                    sp.edit().putString("${selectedDateKey}_$exKey", "no").apply()
                    fbHelper.save(selectedDateKey, exKey, "no")
                }
                for (sName in AppConstants.SUNNAHS[i]) {
                    sp.edit().putString("${selectedDateKey}_${prayer}_Sunnah_$sName", "no").apply()
                    fbHelper.save(selectedDateKey, "${prayer}_Sunnah_$sName", "no")
                }
            }
            dao.insertRecord(r)
            container.dialog.dismiss()
            onDone()
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showSuccessSequence(
        activity: Activity,
        root: FrameLayout,
        selectedDateKey: String,
        colorAccent: Int,
        lang: LanguageEngine,
        appFonts: Array<Typeface?>,
        sp: SharedPreferences
    ) {
        if (sp.getBoolean("${selectedDateKey}_success_shown", false)) return
        sp.edit().putBoolean("${selectedDateKey}_success_shown", true).apply()

        val main = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            val padH = activity.dp(30)
            val padV = activity.dp(45)
            setPadding(padH, padV, padH, padV)
            background = createDrawable(colorAccent, activity.dp(30).toFloat())
            if (Build.VERSION.SDK_INT >= 21) elevation = 50f
        }

        val iconView = TextView(activity).apply {
            text = "💎"
            textSize = 60f
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, activity.dp(10))
        }
        main.addView(iconView)

        val title = TextView(activity).apply {
            text = lang.get("Mashallah!")
            setTextColor(Color.WHITE)
            textSize = 26f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, activity.dp(8))
        }
        main.addView(title)

        val isToday = selectedDateKey == AppDateUtils.formatYmd(Date())
        val msg = TextView(activity).apply {
            text = lang.get(
                if (isToday) "You've completed all prayers today.\nMay Allah accept it."
                else "You've completed all prayers for this day.\nMay Allah accept it."
            )
            setTextColor(Color.parseColor("#F0F0F0"))
            gravity = Gravity.CENTER
            if (Build.VERSION.SDK_INT >= 17) textAlignment = View.TEXT_ALIGNMENT_CENTER
            textSize = 14f
            setLineSpacing(0f, 1.2f)
        }
        main.addView(msg)

        val flp = FrameLayout.LayoutParams(activity.dp(300), -2).apply {
            gravity = Gravity.CENTER
        }
        root.addView(main, flp)

        main.scaleX = 0.5f
        main.scaleY = 0.5f
        main.alpha = 0f
        main.animate()
            .scaleX(1f)
            .scaleY(1f)
            .alpha(1f)
            .setDuration(300)
            .setInterpolator(OvershootInterpolator())
            .start()

        val scaleX = ObjectAnimator.ofFloat(iconView, "scaleX", 1f, 1.15f, 1f).apply {
            repeatCount = ValueAnimator.INFINITE
            duration = 1000
        }
        val scaleY = ObjectAnimator.ofFloat(iconView, "scaleY", 1f, 1.15f, 1f).apply {
            repeatCount = ValueAnimator.INFINITE
            duration = 1000
        }
        AnimatorSet().apply {
            playTogether(scaleX, scaleY)
            start()
        }

        Handler(Looper.getMainLooper()).postDelayed({
            main.animate()
                .scaleX(0.8f)
                .scaleY(0.8f)
                .alpha(0f)
                .setDuration(200)
                .withEndAction { root.removeView(main) }
                .start()
        }, 2500)

        main.applyFont(appFonts[0], appFonts[1])
    }

    fun showWipeDataDialog(
        activity: Activity,
        root: FrameLayout,
        selectedDateKey: String,
        themeColors: IntArray,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>
    ) {
        val container = activity.createCustomDialog(themeColors[1], 25f, 300, 25, 30)

        val icon = ui.getRoundImage("img_offline_warning", 0, Color.TRANSPARENT, Color.parseColor("#FF5252")).apply {
            val s = activity.dp(50)
            layoutParams = LinearLayout.LayoutParams(s, s).apply {
                gravity = Gravity.CENTER_HORIZONTAL
                setMargins(0, 0, 0, activity.dp(3))
            }
        }
        container.contentLayout.addView(icon)

        val title = TextView(activity).apply {
            text = lang.get("Wipe All Data")
            setTextColor(Color.parseColor("#FF5252"))
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
        }
        container.contentLayout.addView(title)

        val sub = TextView(activity).apply {
            text = lang.get("Are you sure? This will delete all your local data permanently.")
            setTextColor(themeColors[3])
            textSize = 14f
            gravity = Gravity.CENTER
            setPadding(0, activity.dp(10), 0, activity.dp(25))
        }
        container.contentLayout.addView(sub)

        val row = LinearLayout(activity).apply { orientation = LinearLayout.HORIZONTAL }

        val btnC = Button(activity).apply {
            text = lang.get("CANCEL")
            setTextColor(themeColors[2])
            isAllCaps = false
            typeface = Typeface.DEFAULT_BOLD
            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
        }
        row.addView(btnC, LinearLayout.LayoutParams(0, activity.dp(50), 1f).apply {
            setMargins(0, 0, activity.dp(10), 0)
        })

        val btnD = Button(activity).apply {
            text = lang.get("Delete")
            setTextColor(Color.parseColor("#F1F5F9"))
            isAllCaps = false
            typeface = Typeface.DEFAULT_BOLD
            background = createDrawable(Color.parseColor("#FF5252"), activity.dp(15).toFloat())
        }
        row.addView(btnD, LinearLayout.LayoutParams(0, activity.dp(50), 1f))
        container.contentLayout.addView(row)

        btnC.setOnClickListener { container.dialog.dismiss() }
        btnD.setOnClickListener {
            container.dialog.dismiss()
            ui.showSmartBanner(root, lang.get("Deleting..."), "", "img_offline_warning", Color.parseColor("#FF5252"), null)
            Thread {
                SalahDatabase.getInstance(activity).clearAllTables()
                sp.edit().clear().apply()
                activity.runOnUiThread {
                    activity.finish()
                    val intent = Intent(activity, MainActivity::class.java).apply {
                        putExtra("RESTORE_DATE", AppDateUtils.parseYmd(selectedDateKey)?.time ?: Date().time)
                    }
                    activity.startActivity(intent)
                }
            }.start()
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showRozaCategoryDialog(
        activity: Activity,
        selectedDateKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onDone: () -> Unit
    ) {
        val isBn = sp.getString("app_lang", "en") == "bn"
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 25, 30)

        val title = TextView(activity).apply {
            text = if (isBn) "রোজার ক্যাটাগরি" else "Fasting Category"
            setTextColor(colorAccent)
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        val sv = ScrollView(activity)
        val list = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL }

        val opts = if (isBn) arrayOf("ফরজ", "কাজা", "নফল") else arrayOf("Fard", "Qaza", "Nafil")
        val vals = arrayOf("fard", "qaza", "nafil")
        val curType = sp.getString("${selectedDateKey}_roza_type", "nafil") ?: "nafil"

        for (s in opts.indices) {
            val sName = opts[s]
            val sVal = vals[s]
            val sChecked = curType == sVal

            val row = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                val padH = activity.dp(10)
                val padV = activity.dp(12)
                setPadding(padH, padV, padH, padV)
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, activity.dp(10))
                }
                background = createDrawable(if (sChecked) themeColors[4] else Color.TRANSPARENT, activity.dp(15).toFloat())
            }

            val tv = TextView(activity).apply {
                text = sName
                setTextColor(if (sChecked) colorAccent else themeColors[2])
                textSize = 16f
                typeface = if (sChecked) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            }
            val chk = ui.getPremiumCheckbox(if (sChecked) "yes" else "no", colorAccent)
            row.addView(tv)
            row.addView(chk)
            list.addView(row)

            row.setOnClickListener { v ->
                v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                sp.edit().putString("${selectedDateKey}_roza_type", sVal).apply()
                sp.edit().putString("${selectedDateKey}_roza_stat", "yes").apply()
                container.dialog.dismiss()
                onDone()
            }
        }

        sv.addView(list)
        container.contentLayout.addView(sv, LinearLayout.LayoutParams(-1, -2, 1f))

        val closeBtn = TextView(activity).apply {
            text = lang.get("Done")
            setTextColor(Color.parseColor("#F1F5F9"))
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            val padV = activity.dp(15)
            setPadding(0, padV, 0, padV)
            background = createDrawable(colorAccent, activity.dp(20).toFloat())
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, activity.dp(15), 0, 0)
            }
            setOnClickListener {
                container.dialog.dismiss()
                onDone()
            }
        }
        container.contentLayout.addView(closeBtn)

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showSunnahDialog(
        activity: Activity,
        selectedDateKey: String,
        prayer: String,
        sunnahList: Array<String>,
        themeColors: IntArray,
        colorAccent: Int,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        fbHelper: FirebaseManager,
        onDone: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 25, 30)

        val title = TextView(activity).apply {
            text = "${lang.get(prayer)} ${lang.get("Extras")}"
            setTextColor(colorAccent)
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(title)

        val sv = ScrollView(activity)
        val list = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL }

        for (sName in sunnahList) {
            val sKey = "${selectedDateKey}_${prayer}_Sunnah_$sName"
            val sChecked = sp.getString(sKey, "no") == "yes"

            val rowBg = createDrawable(if (sChecked) themeColors[4] else Color.TRANSPARENT, activity.dp(15).toFloat())
            val row = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                val padH = activity.dp(10)
                val padV = activity.dp(12)
                setPadding(padH, padV, padH, padV)
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, activity.dp(10))
                }
                background = rowBg
            }

            val tv = TextView(activity).apply {
                text = lang.get(sName)
                setTextColor(if (sChecked) colorAccent else themeColors[2])
                textSize = 16f
                typeface = if (sChecked) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            }
            val chk = ui.getPremiumCheckbox(if (sChecked) "yes" else "no", colorAccent)
            row.addView(tv)
            row.addView(chk)
            list.addView(row)

            row.setOnClickListener { v ->
                v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                val cur = sp.getString(sKey, "no") == "yes"
                val newVal = !cur
                sp.edit().putString(sKey, if (newVal) "yes" else "no").apply()
                fbHelper.save(selectedDateKey, "${prayer}_Sunnah_$sName", if (newVal) "yes" else "no")

                val t = chk as? TextView
                val bg = t?.background as? GradientDrawable
                if (newVal) {
                    bg?.setColor(colorAccent)
                    bg?.setStroke(0, Color.TRANSPARENT)
                    t?.text = "✓"
                    t?.setTextColor(Color.parseColor("#F1F5F9"))
                    rowBg.setColor(themeColors[4])
                    tv.setTextColor(colorAccent)
                    tv.typeface = Typeface.DEFAULT_BOLD
                } else {
                    bg?.setColor(Color.TRANSPARENT)
                    bg?.setStroke(activity.dp(2), themeColors[4])
                    t?.text = ""
                    rowBg.setColor(Color.TRANSPARENT)
                    tv.setTextColor(themeColors[2])
                    tv.typeface = Typeface.DEFAULT
                }
            }
        }

        val cStr = sp.getString("custom_nafl_$prayer", "") ?: ""
        if (cStr.isNotEmpty()) {
            for (cItem in cStr.split(",")) {
                if (cItem.trim().isEmpty()) continue
                val pts = cItem.split(":")
                val cName = pts[0]
                val cRak = if (pts.size > 1) pts[1] else "2"
                val cKey = "${selectedDateKey}_${prayer}_Custom_$cName"
                val cChecked = sp.getString(cKey, "no") == "yes"

                val rowBg = createDrawable(if (cChecked) themeColors[4] else Color.TRANSPARENT, activity.dp(15).toFloat())
                val row = LinearLayout(activity).apply {
                    orientation = LinearLayout.HORIZONTAL
                    gravity = Gravity.CENTER_VERTICAL
                    val padH = activity.dp(10)
                    val padV = activity.dp(12)
                    setPadding(padH, padV, padH, padV)
                    layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                        setMargins(0, 0, 0, activity.dp(10))
                    }
                    background = rowBg
                }

                val tCon = LinearLayout(activity).apply {
                    orientation = LinearLayout.VERTICAL
                    layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
                }
                val tv = TextView(activity).apply {
                    text = cName
                    isSingleLine = true
                    ellipsize = TextUtils.TruncateAt.END
                    setTextColor(if (cChecked) colorAccent else themeColors[2])
                    textSize = 16f
                    typeface = if (cChecked) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
                }
                tCon.addView(tv)

                val tvR = TextView(activity).apply {
                    text = "${lang.bnNum(cRak)} ${lang.get("Rakats")}"
                    setTextColor(themeColors[3])
                    textSize = 12f
                    setPadding(5, 2, 5, 2)
                }
                tCon.addView(tvR)
                row.addView(tCon)

                val chk = ui.getPremiumCheckbox(if (cChecked) "yes" else "no", colorAccent)
                row.addView(chk)
                list.addView(row)

                row.setOnClickListener { v ->
                    v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    val cur = sp.getString(cKey, "no") == "yes"
                    val newVal = !cur
                    sp.edit().putString(cKey, if (newVal) "yes" else "no").apply()
                    fbHelper.save(selectedDateKey, "${prayer}_Custom_$cName", if (newVal) "yes" else "no")

                    val t = chk as? TextView
                    val bg = t?.background as? GradientDrawable
                    if (newVal) {
                        bg?.setColor(colorAccent)
                        bg?.setStroke(0, Color.TRANSPARENT)
                        t?.text = "✓"
                        t?.setTextColor(Color.parseColor("#F1F5F9"))
                        rowBg.setColor(themeColors[4])
                        tv.setTextColor(colorAccent)
                        tv.typeface = Typeface.DEFAULT_BOLD
                    } else {
                        bg?.setColor(Color.TRANSPARENT)
                        bg?.setStroke(activity.dp(2), themeColors[4])
                        t?.text = ""
                        rowBg.setColor(Color.TRANSPARENT)
                        tv.setTextColor(themeColors[2])
                        tv.typeface = Typeface.DEFAULT
                    }
                }

                row.setOnLongClickListener { v ->
                    v.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS)
                    showDeleteCustomPrayerDialog(activity, prayer, cName, themeColors, lang, sp, appFonts, container.dialog) {
                        onDone()
                    }
                    true
                }
            }
        }

        val addBtn = LinearLayout(activity).apply {
            val pad = activity.dp(15)
            setPadding(pad, pad, pad, pad)
            gravity = Gravity.CENTER
            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, activity.dp(10), 0, activity.dp(10))
            }
        }
        val aTxt = TextView(activity).apply {
            text = "➕ " + lang.get("Add Extra Prayer")
            setTextColor(themeColors[2])
            typeface = Typeface.DEFAULT_BOLD
        }
        addBtn.addView(aTxt)
        addBtn.setOnClickListener { v ->
            v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
            showAddCustomPrayerDialog(activity, prayer, themeColors, colorAccent, lang, sp, appFonts, container.dialog) {
                onDone()
            }
        }
        list.addView(addBtn)

        sv.addView(list)
        container.contentLayout.addView(sv, LinearLayout.LayoutParams(-1, -2, 1f))

        val closeBtn = TextView(activity).apply {
            text = lang.get("Done")
            setTextColor(Color.parseColor("#F1F5F9"))
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            val padV = activity.dp(15)
            setPadding(0, padV, 0, padV)
            background = createDrawable(colorAccent, activity.dp(20).toFloat())
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, activity.dp(15), 0, 0)
            }
            setOnClickListener {
                container.dialog.dismiss()
                onDone()
            }
        }
        container.contentLayout.addView(closeBtn)

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showAddCustomPrayerDialog(
        activity: Activity,
        prayer: String,
        themeColors: IntArray,
        colorAccent: Int,
        lang: LanguageEngine,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        parentDialog: AlertDialog?,
        onDone: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 30f, 320, 25, 30)

        val title = TextView(activity).apply {
            text = lang.get("Add Extra Prayer")
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, activity.dp(10), 0, activity.dp(25))
        }
        container.contentLayout.addView(title)

        val iBg = createDrawable(themeColors[4], activity.dp(15).toFloat())
        val nameIn = EditText(activity).apply {
            hint = lang.get("Prayer Name (e.g. Ishraq)")
            setTextColor(themeColors[2])
            setHintTextColor(themeColors[3])
            background = iBg
            val padH = activity.dp(20)
            val padV = activity.dp(15)
            setPadding(padH, padV, padH, padV)
        }
        container.contentLayout.addView(nameIn, LinearLayout.LayoutParams(-1, -2))

        val rakIn = EditText(activity).apply {
            hint = lang.get("Rakats (e.g. 2)")
            inputType = InputType.TYPE_CLASS_NUMBER
            setTextColor(themeColors[2])
            setHintTextColor(themeColors[3])
            background = iBg
            val padH = activity.dp(20)
            val padV = activity.dp(15)
            setPadding(padH, padV, padH, padV)
        }
        container.contentLayout.addView(rakIn, LinearLayout.LayoutParams(-1, -2).apply {
            setMargins(0, activity.dp(10), 0, activity.dp(25))
        })

        val btn = Button(activity).apply {
            text = lang.get("Add Prayer")
            setTextColor(Color.parseColor("#F1F5F9"))
            typeface = Typeface.DEFAULT_BOLD
            isAllCaps = false
            background = createDrawable(colorAccent, activity.dp(20).toFloat())
        }
        container.contentLayout.addView(btn, LinearLayout.LayoutParams(-1, activity.dp(55)))

        btn.setOnClickListener {
            val n = nameIn.text.toString().trim().replace(":", "").replace(",", "").replace("|", "")
            val r = rakIn.text.toString().trim()
            if (n.isNotEmpty()) {
                val cList = sp.getString("custom_nafl_$prayer", "") ?: ""
                val entry = "$n:" + (if (r.isEmpty()) "2" else r)
                sp.edit().putString("custom_nafl_$prayer", cList + (if (cList.isEmpty()) "" else ",") + entry).apply()
                container.dialog.dismiss()
                parentDialog?.dismiss()
                onDone()
            }
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showDeleteCustomPrayerDialog(
        activity: Activity,
        prayer: String,
        cName: String,
        themeColors: IntArray,
        lang: LanguageEngine,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        parentDialog: AlertDialog?,
        onDone: () -> Unit
    ) {
        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 25, 30)

        val title = TextView(activity).apply {
            text = lang.get("Delete Extra Prayer?")
            setTextColor(Color.parseColor("#FF5252"))
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
        }
        container.contentLayout.addView(title)

        val sub = TextView(activity).apply {
            text = lang.get("This will remove it from your list.")
            setTextColor(themeColors[3])
            gravity = Gravity.CENTER
            setPadding(0, activity.dp(10), 0, activity.dp(25))
        }
        container.contentLayout.addView(sub)

        val row = LinearLayout(activity).apply { orientation = LinearLayout.HORIZONTAL }

        val btnC = Button(activity).apply {
            text = lang.get("CANCEL")
            setTextColor(themeColors[2])
            typeface = Typeface.DEFAULT_BOLD
            isAllCaps = false
            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
        }
        row.addView(btnC, LinearLayout.LayoutParams(0, activity.dp(50), 1f).apply {
            setMargins(0, 0, activity.dp(10), 0)
        })

        val btnD = Button(activity).apply {
            text = lang.get("Delete")
            setTextColor(Color.parseColor("#F1F5F9"))
            typeface = Typeface.DEFAULT_BOLD
            isAllCaps = false
            background = createDrawable(Color.parseColor("#FF5252"), activity.dp(15).toFloat())
        }
        row.addView(btnD, LinearLayout.LayoutParams(0, activity.dp(50), 1f))
        container.contentLayout.addView(row)

        btnC.setOnClickListener { container.dialog.dismiss() }
        btnD.setOnClickListener {
            val cList = sp.getString("custom_nafl_$prayer", "") ?: ""
            val pts = cList.split(",")
            val sb = StringBuilder()
            for (p in pts) {
                if (!p.startsWith("$cName:") && p != cName) {
                    sb.append(p).append(",")
                }
            }
            var res = sb.toString()
            if (res.endsWith(",")) res = res.substring(0, res.length - 1)
            sp.edit().putString("custom_nafl_$prayer", res).apply()
            container.dialog.dismiss()
            parentDialog?.dismiss()
            onDone()
        }

        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    fun showQuranDialog(
        activity: Activity,
        dateKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onDone: () -> Unit
    ) {
        val isQuranBn = sp.getString("app_lang", "en") == "bn"
        val quranDbKey = "${dateKey}_quran_stat"
        val quranParaKey = "${dateKey}_quran_para"
        val quranPageKey = "${dateKey}_quran_page"

        val container = activity.createCustomDialog(themeColors[1], 25f, 320, 25, 30)

        val t = TextView(activity).apply {
            text = if (isQuranBn) "কতটুকু পড়েছেন?" else "How much did you read?"
            setTextColor(colorAccent)
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, activity.dp(20))
        }
        container.contentLayout.addView(t)

        val ib = createDrawable(themeColors[4], activity.dp(15).toFloat())
        val paraIn = EditText(activity).apply {
            hint = if (isQuranBn) "পারা (যেমন: ১)" else "Para (e.g. 1)"
            inputType = InputType.TYPE_CLASS_NUMBER
            setTextColor(themeColors[2])
            setHintTextColor(themeColors[3])
            background = ib
            val ePadH = activity.dp(20)
            val ePadV = activity.dp(15)
            setPadding(ePadH, ePadV, ePadH, ePadV)
            if (sp.getInt(quranParaKey, 0) > 0) setText(sp.getInt(quranParaKey, 0).toString())
        }
        container.contentLayout.addView(paraIn, LinearLayout.LayoutParams(-1, -2).apply {
            setMargins(0, 0, 0, activity.dp(10))
        })

        val pageIn = EditText(activity).apply {
            hint = if (isQuranBn) "পৃষ্ঠা (যেমন: ২)" else "Page (e.g. 2)"
            inputType = InputType.TYPE_CLASS_NUMBER
            setTextColor(themeColors[2])
            setHintTextColor(themeColors[3])
            background = createDrawable(themeColors[4], activity.dp(15).toFloat())
            val ePadH = activity.dp(20)
            val ePadV = activity.dp(15)
            setPadding(ePadH, ePadV, ePadH, ePadV)
            if (sp.getInt(quranPageKey, 0) > 0) setText(sp.getInt(quranPageKey, 0).toString())
        }
        container.contentLayout.addView(pageIn, LinearLayout.LayoutParams(-1, -2).apply {
            setMargins(0, 0, 0, activity.dp(20))
        })

        val b = Button(activity).apply {
            text = if (isQuranBn) "সেভ করুন" else "Save"
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            isAllCaps = false
            background = createDrawable(colorAccent, activity.dp(20).toFloat())
        }
        container.contentLayout.addView(b, LinearLayout.LayoutParams(-1, activity.dp(55)))

        b.setOnClickListener {
            var p1 = 0
            var p2 = 0
            try {
                if (paraIn.text.toString().trim().isNotEmpty()) p1 = paraIn.text.toString().trim().toInt()
            } catch (e: Exception) {}
            try {
                if (pageIn.text.toString().trim().isNotEmpty()) p2 = pageIn.text.toString().trim().toInt()
            } catch (e: Exception) {}
            sp.edit()
                .putInt(quranParaKey, p1)
                .putInt(quranPageKey, p2)
                .putString(quranDbKey, if (p1 > 0 || p2 > 0) "yes" else "no")
                .apply()
            container.dialog.dismiss()
            onDone()
        }
        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }
}
