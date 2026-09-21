package com.my.salah.tracker.app

import android.app.Activity
import android.app.AlertDialog
import android.content.SharedPreferences
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.view.Gravity
import android.view.View
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

/**
 * Dedicated helper for Bengali (BS) Calendar calculations, year picker, and interactive monthly grid.
 */
object BengaliCalendarHelper {

    private var bnViewYear = 1430
    private var bnViewMonth = 0

    @JvmStatic
    fun getBnDateStr(dateStr: String, sp: SharedPreferences): String {
        return try {
            val p = dateStr.split("-")
            val y = p[0].toInt()
            val m = p[1].toInt()
            val d = p[2].toInt()
            var bY = y - 593
            var bM = 0
            var bD = 0
            val isLeap = (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0)

            when (m) {
                4 -> if (d >= 14) { bM = 0; bD = d - 13 } else { bM = 11; bD = d + 17; bY-- }
                5 -> if (d <= 14) { bM = 0; bD = d + 17 } else { bM = 1; bD = d - 14 }
                6 -> if (d <= 14) { bM = 1; bD = d + 17 } else { bM = 2; bD = d - 14 }
                7 -> if (d <= 15) { bM = 2; bD = d + 16 } else { bM = 3; bD = d - 15 }
                8 -> if (d <= 15) { bM = 3; bD = d + 16 } else { bM = 4; bD = d - 15 }
                9 -> if (d <= 15) { bM = 4; bD = d + 16 } else { bM = 5; bD = d - 15 }
                10 -> if (d <= 15) { bM = 5; bD = d + 15 } else { bM = 6; bD = d - 15 }
                11 -> if (d <= 14) { bM = 6; bD = d + 16 } else { bM = 7; bD = d - 14 }
                12 -> if (d <= 14) { bM = 7; bD = d + 16 } else { bM = 8; bD = d - 14 }
                1 -> if (d <= 13) { bM = 8; bD = d + 17; bY-- } else { bM = 9; bD = d - 13; bY-- }
                2 -> if (d <= 12) { bM = 9; bD = d + 18; bY-- } else { bM = 10; bD = d - 12; bY-- }
                3 -> if (d <= 14) { bM = 10; bD = d + (if (isLeap) 17 else 16); bY-- } else { bM = 11; bD = d - 14; bY-- }
            }

            bD += sp.getInt("bn_date_offset", 0)
            val isBn = sp.getString("app_lang", "en") == "bn"
            val bMs = if (isBn) {
                arrayOf("বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র")
            } else {
                arrayOf("Boishakh", "Joistho", "Ashar", "Srabon", "Bhadro", "Ashwin", "Kartik", "Agrahayon", "Poush", "Magh", "Falgun", "Choitro")
            }

            val suf = if (!isBn) {
                if (bD in 11..13) "th"
                else when (bD % 10) {
                    1 -> "st"
                    2 -> "nd"
                    3 -> "rd"
                    else -> "th"
                }
            } else {
                when {
                    bD == 1 -> "লা"
                    bD in 2..3 -> "রা"
                    bD == 4 -> "ঠা"
                    bD in 5..18 -> "ই"
                    else -> "শে"
                }
            }

            var dayStr = bD.toString()
            var yearStr = bY.toString()
            if (isBn) {
                dayStr = dayStr.toBnDigits()
                yearStr = yearStr.toBnDigits()
            }
            "$dayStr$suf ${bMs[bM]}, $yearStr" + (if (isBn) " বঙ্গাব্দ" else " BS")
        } catch (e: Exception) {
            ""
        }
    }

    fun showBengaliCalendar(
        activity: Activity,
        selectedDateKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        isDarkTheme: Boolean,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onDateSelected: (String) -> Unit
    ) {
        try {
            val cal = Calendar.getInstance().apply {
                time = AppDateUtils.parseYmd(selectedDateKey) ?: Date()
            }
            val y = cal.get(Calendar.YEAR)
            val m = cal.get(Calendar.MONTH) + 1
            val d = cal.get(Calendar.DAY_OF_MONTH)
            var bY = y - 593
            bnViewMonth = 0

            when (m) {
                4 -> if (d >= 14) bnViewMonth = 0 else { bnViewMonth = 11; bY-- }
                5 -> if (d <= 14) bnViewMonth = 0 else bnViewMonth = 1
                6 -> if (d <= 14) bnViewMonth = 1 else bnViewMonth = 2
                7 -> if (d <= 15) bnViewMonth = 2 else bnViewMonth = 3
                8 -> if (d <= 15) bnViewMonth = 3 else bnViewMonth = 4
                9 -> if (d <= 15) bnViewMonth = 4 else bnViewMonth = 5
                10 -> if (d <= 15) bnViewMonth = 5 else bnViewMonth = 6
                11 -> if (d <= 14) bnViewMonth = 6 else bnViewMonth = 7
                12 -> if (d <= 14) bnViewMonth = 7 else bnViewMonth = 8
                1 -> if (d <= 13) { bnViewMonth = 8; bY-- } else { bnViewMonth = 9; bY-- }
                2 -> if (d <= 12) { bnViewMonth = 9; bY-- } else { bnViewMonth = 10; bY-- }
                3 -> if (d <= 14) { bnViewMonth = 10; bY-- } else { bnViewMonth = 11; bY-- }
            }
            bnViewYear = bY
        } catch (e: Exception) {
        }

        val container = activity.createCustomDialog(
            bgColor = themeColors[1],
            radiusDp = 20f,
            widthDp = 320,
            padHDp = 20,
            padVDp = 25
        )

        renderBnGrid(activity, container.contentLayout, container.dialog, selectedDateKey, themeColors, colorAccent, isDarkTheme, lang, ui, sp, appFonts, onDateSelected)
        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        if (!activity.isFinishing) container.dialog.show()
    }

    private fun renderBnGrid(
        activity: Activity,
        card: LinearLayout,
        dialog: AlertDialog,
        selectedDateKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        isDarkTheme: Boolean,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onDateSelected: (String) -> Unit
    ) {
        val density = activity.resources.displayMetrics.density
        card.removeAllViews()
        val isBn = sp.getString("app_lang", "en") == "bn"

        val yearChip = TextView(activity).apply {
            setTextColor(colorAccent)
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            val yPadH = (25 * density).toInt()
            val yPadV = (8 * density).toInt()
            setPadding(yPadH, yPadV, yPadH, yPadV)
            background = createDrawable(colorAccent and 0x15FFFFFF, 15f * density)
            layoutParams = LinearLayout.LayoutParams(-2, -2).apply {
                gravity = Gravity.CENTER_HORIZONTAL
                setMargins(0, 0, 0, (15 * density).toInt())
            }
            text = if (isBn) bnViewYear.toString().toBnDigits() else bnViewYear.toString()
            setOnClickListener {
                showBengaliYearPicker(activity, card, dialog, selectedDateKey, themeColors, colorAccent, isDarkTheme, lang, ui, sp, appFonts, onDateSelected)
            }
        }
        card.addView(yearChip)

        val header = LinearLayout(activity).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        val prev = TextView(activity).apply {
            text = "❮"
            textSize = 20f
            setTextColor(themeColors[2])
            val hPad = (10 * density).toInt()
            setPadding(hPad, hPad, hPad, hPad)
        }
        val title = TextView(activity).apply {
            val bMs = if (isBn) arrayOf("বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র")
                      else arrayOf("Boishakh", "Joistho", "Ashar", "Srabon", "Bhadro", "Ashwin", "Kartik", "Agrahayon", "Poush", "Magh", "Falgun", "Choitro")
            text = bMs[bnViewMonth]
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            gravity = Gravity.CENTER
        }
        val next = TextView(activity).apply {
            text = "❯"
            textSize = 20f
            setTextColor(themeColors[2])
            val hPad = (10 * density).toInt()
            setPadding(hPad, hPad, hPad, hPad)
        }
        header.addView(prev)
        header.addView(title)
        header.addView(next)
        card.addView(header)

        val tCal = Calendar.getInstance()
        val tY = tCal.get(Calendar.YEAR)
        val tM = tCal.get(Calendar.MONTH) + 1
        val tD = tCal.get(Calendar.DAY_OF_MONTH)
        var tBY = tY - 593
        var tBM = 0

        when (tM) {
            4 -> if (tD >= 14) tBM = 0 else { tBM = 11; tBY-- }
            5 -> if (tD <= 14) tBM = 0 else tBM = 1
            6 -> if (tD <= 14) tBM = 1 else tBM = 2
            7 -> if (tD <= 15) tBM = 2 else tBM = 3
            8 -> if (tD <= 15) tBM = 3 else tBM = 4
            9 -> if (tD <= 15) tBM = 4 else tBM = 5
            10 -> if (tD <= 15) tBM = 5 else tBM = 6
            11 -> if (tD <= 14) tBM = 6 else tBM = 7
            12 -> if (tD <= 14) tBM = 7 else tBM = 8
            1 -> if (tD <= 13) { tBM = 8; tBY-- } else { tBM = 9; tBY-- }
            2 -> if (tD <= 12) { tBM = 9; tBY-- } else { tBM = 10; tBY-- }
            3 -> if (tD <= 14) { tBM = 10; tBY-- } else { tBM = 11; tBY-- }
        }

        val isFutureMonth = (bnViewYear > tBY) || (bnViewYear == tBY && bnViewMonth >= tBM)
        val cGYear = bnViewYear + 593 + (if (bnViewMonth >= 9) 1 else 0)
        val isOldMonth = cGYear <= (tY - 100)

        next.alpha = if (isFutureMonth) 0.3f else 1f
        prev.alpha = if (isOldMonth) 0.3f else 1f

        prev.setOnClickListener { v ->
            if (isOldMonth) {
                val r: FrameLayout? = activity.findViewById(android.R.id.content)
                if (r != null) {
                    ui.showSmartBanner(
                        r,
                        lang.get("Limit Reached"),
                        lang.get("Cannot go back more than 100 years."),
                        "img_warning", colorAccent, null
                    )
                }
                return@setOnClickListener
            }
            v.bounceClick(0.95f, 50) {
                bnViewMonth--
                if (bnViewMonth < 0) {
                    bnViewMonth = 11
                    bnViewYear--
                }
                renderBnGrid(activity, card, dialog, selectedDateKey, themeColors, colorAccent, isDarkTheme, lang, ui, sp, appFonts, onDateSelected)
            }
        }

        next.setOnClickListener { v ->
            if (isFutureMonth) return@setOnClickListener
            v.bounceClick(0.95f, 50) {
                bnViewMonth++
                if (bnViewMonth > 11) {
                    bnViewMonth = 0
                    bnViewYear++
                }
                renderBnGrid(activity, card, dialog, selectedDateKey, themeColors, colorAccent, isDarkTheme, lang, ui, sp, appFonts, onDateSelected)
            }
        }

        val weekdays = LinearLayout(activity).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(0, (15 * density).toInt(), 0, (10 * density).toInt())
        }
        val wds = if (isBn) arrayOf("র", "স", "ম", "ব", "ব", "শ", "শ")
                  else arrayOf("S", "M", "T", "W", "T", "F", "S")
        for (w in wds) {
            val wt = TextView(activity).apply {
                text = w
                setTextColor(themeColors[3])
                textSize = 12f
                typeface = Typeface.DEFAULT_BOLD
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
                gravity = Gravity.CENTER
            }
            weekdays.addView(wt)
        }
        card.addView(weekdays)

        var daysInMonth = 30
        if (bnViewMonth in 0..5) {
            daysInMonth = 31
        } else if (bnViewMonth == 10) {
            val gYear = bnViewYear + 594
            daysInMonth = if ((gYear % 4 == 0 && gYear % 100 != 0) || (gYear % 400 == 0)) 31 else 30
        }

        val sMG = intArrayOf(
            Calendar.APRIL, Calendar.MAY, Calendar.JUNE,
            Calendar.JULY, Calendar.AUGUST, Calendar.SEPTEMBER,
            Calendar.OCTOBER, Calendar.NOVEMBER, Calendar.DECEMBER,
            Calendar.JANUARY, Calendar.FEBRUARY, Calendar.MARCH
        )
        val sDG = intArrayOf(14, 15, 15, 16, 16, 16, 16, 15, 15, 14, 13, 15)
        val gY = bnViewYear + 593 + (if (bnViewMonth >= 9) 1 else 0)
        val bnCal = Calendar.getInstance().apply {
            set(gY, sMG[bnViewMonth], sDG[bnViewMonth], 0, 0, 0)
        }
        val sDOW = bnCal.get(Calendar.DAY_OF_WEEK)

        val grid = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
        }
        var currentDay = 1
        var cellCount = 1

        for (r in 0 until 6) {
            val row = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
            }
            for (c in 0 until 7) {
                val cell = FrameLayout(activity).apply {
                    layoutParams = LinearLayout.LayoutParams(0, (45 * density).toInt(), 1f)
                }
                if (cellCount >= sDOW && currentDay <= daysInMonth) {
                    val cGreg = AppDateUtils.formatYmd(bnCal.time)
                    val isSel = cGreg == selectedDateKey
                    val isFutureDate = bnCal.time.after(tCal.time) && cGreg != AppDateUtils.formatYmd(tCal.time)
                    var isAllDone = true

                    if (!isFutureDate) {
                        for (pr in AppConstants.PRAYERS) {
                            val stat = sp.getString("${cGreg}_$pr", "no") ?: "no"
                            if (stat != "yes" && stat != "excused") {
                                isAllDone = false
                                break
                            }
                        }
                    } else {
                        isAllDone = false
                    }

                    val dStr = if (isBn) currentDay.toString().toBnDigits() else currentDay.toString()
                    val dt = TextView(activity).apply {
                        text = dStr
                        gravity = Gravity.CENTER
                        typeface = Typeface.DEFAULT_BOLD
                        setTextColor(if (isSel) Color.WHITE else themeColors[2])
                        if (isFutureDate) alpha = 0.3f
                        layoutParams = FrameLayout.LayoutParams((35 * density).toInt(), (35 * density).toInt()).apply {
                            gravity = Gravity.CENTER
                        }
                        if (isSel) {
                            background = createDrawable(colorAccent, shape = GradientDrawable.OVAL)
                        } else if (isAllDone) {
                            background = (activity as? MainActivity)?.getProgressBorder(cGreg, false)
                        }
                    }
                    cell.addView(dt)

                    cell.setOnClickListener {
                        if (isFutureDate) {
                            ui.showPremiumLocked(colorAccent)
                        } else {
                            dialog.dismiss()
                            onDateSelected(cGreg)
                        }
                    }
                    bnCal.add(Calendar.DATE, 1)
                    currentDay++
                }
                row.addView(cell)
                cellCount++
            }
            grid.addView(row)
            if (currentDay > daysInMonth) break
        }
        card.addView(grid)

        val close = TextView(activity).apply {
            text = if (isBn) "বন্ধ করুন" else "CLOSE"
            setTextColor(themeColors[3])
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, (15 * density).toInt(), 0, 0)
            setOnClickListener { dialog.dismiss() }
        }
        card.addView(close)
    }

    private fun showBengaliYearPicker(
        activity: Activity,
        parentCard: LinearLayout,
        calDialog: AlertDialog,
        selectedDateKey: String,
        themeColors: IntArray,
        colorAccent: Int,
        isDarkTheme: Boolean,
        lang: LanguageEngine,
        ui: UIComponents,
        sp: SharedPreferences,
        appFonts: Array<Typeface?>,
        onDateSelected: (String) -> Unit
    ) {
        val isBn = sp.getString("app_lang", "en") == "bn"
        val container = activity.createCustomDialog(
            bgColor = themeColors[1],
            radiusDp = 20f,
            widthDp = 300,
            padHDp = 25,
            padVDp = 25
        )

        val density = activity.resources.displayMetrics.density
        val yTitle = TextView(activity).apply {
            text = if (isBn) "সাল নির্বাচন করুন" else "Select Year"
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, (15 * density).toInt())
        }
        container.contentLayout.addView(yTitle)

        val sv = ScrollView(activity)
        val list = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (20 * density).toInt()
            setPadding(padH, 0, padH, 0)
        }

        val currentRealBYear = Calendar.getInstance().get(Calendar.YEAR) - 593

        for (y in (currentRealBYear + 1) downTo (currentRealBYear - 100)) {
            val selectedY = y
            val yStr = if (isBn) y.toString().toBnDigits() else y.toString()
            val yt = TextView(activity).apply {
                text = "$yStr " + (if (isBn) "বঙ্গাব্দ" else "BS")
                textSize = 18f
                val pPadV = (15 * density).toInt()
                setPadding(0, pPadV, 0, pPadV)
                gravity = Gravity.CENTER
                typeface = if (y == bnViewYear) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
                setTextColor(if (y == bnViewYear) colorAccent else themeColors[2])
                setOnClickListener {
                    bnViewYear = selectedY
                    container.dialog.dismiss()
                    renderBnGrid(activity, parentCard, calDialog, selectedDateKey, themeColors, colorAccent, isDarkTheme, lang, ui, sp, appFonts, onDateSelected)
                }
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, (5 * density).toInt())
                }
            }
            list.addView(yt)
        }

        sv.addView(list)
        container.contentLayout.addView(sv, LinearLayout.LayoutParams(-1, (300 * density).toInt()))
        container.contentLayout.applyFont(appFonts[0], appFonts[1])
        container.dialog.show()
    }
}
