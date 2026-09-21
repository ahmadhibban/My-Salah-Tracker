package com.my.salah.tracker.app

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.SharedPreferences
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.icu.util.IslamicCalendar
import android.os.Build
import android.view.Gravity
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class CalendarHelper(
    private val activity: Activity,
    private val DENSITY: Float,
    private val themeColors: IntArray,
    private val colorAccent: Int,
    private val lang: LanguageEngine,
    private val ui: UIComponents,
    private val sp: SharedPreferences,
    private val prayers: Array<String>,
    private val selectedDate: Array<String>,
    private val calendarViewPointer: Calendar,
    private val onDateSelected: Runnable?
) {
    private val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.US)
    private val monthOnlyF = SimpleDateFormat(
        "MMMM",
        if (sp.getString("app_lang", "en") == "bn") Locale("bn") else Locale.US
    )
    private val hijriViewCal: Calendar = Calendar.getInstance()
    private var tfReg: Typeface = Typeface.DEFAULT
    private var tfBold: Typeface = Typeface.DEFAULT_BOLD

    init {
        try {
            if (sp.getString("app_lang", "en") == "bn") {
                tfReg = Typeface.createFromAsset(activity.assets, "fonts/hind_reg.ttf")
                tfBold = Typeface.createFromAsset(activity.assets, "fonts/hind_bold.ttf")
            } else {
                tfReg = Typeface.createFromAsset(activity.assets, "fonts/poppins_reg.ttf")
                tfBold = Typeface.createFromAsset(activity.assets, "fonts/poppins_bold.ttf")
            }
        } catch (_: Exception) {}
    }

    fun showGregorian() {
        calendarViewPointer.time = Date()
        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val calCard = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (20 * DENSITY).toInt()
            val padV = (25 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            gravity = Gravity.CENTER_HORIZONTAL
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 25f * DENSITY
                setStroke((1.5f * DENSITY).toInt(), themeColors[4])
            }
        }
        val flp = FrameLayout.LayoutParams(-1, -2).apply {
            gravity = Gravity.CENTER
            setMargins((20 * DENSITY).toInt(), 0, (20 * DENSITY).toInt(), 0)
        }
        wrap.addView(calCard, flp)

        val dialog = AlertDialog.Builder(activity).setView(wrap).create()
        dialog.window?.setBackgroundDrawableResource(android.R.color.transparent)
        dialog.window?.setGravity(Gravity.CENTER)

        renderGregorian(calCard, dialog)
        wrap.applyFont(tfReg, tfBold)
        if (!activity.isFinishing) {
            dialog.show()
        }
    }

    private fun renderGregorian(card: LinearLayout, dialog: AlertDialog) {
        card.removeAllViews()

        // Year Chip Container
        val yearContainer = LinearLayout(activity).apply {
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, (10 * DENSITY).toInt())
        }
        val yearBtn = TextView(activity).apply {
            text = lang.bnNum(calendarViewPointer.get(Calendar.YEAR))
            setTextColor(colorAccent)
            typeface = Typeface.DEFAULT_BOLD
            val padH = (25 * DENSITY).toInt()
            val padV = (8 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            background = GradientDrawable().apply {
                setColor(colorAccent and 0x15FFFFFF)
                cornerRadius = 15f * DENSITY
            }
            setOnClickListener { showYearPicker(card, dialog) }
        }
        yearContainer.addView(yearBtn)
        card.addView(yearContainer)

        // Month Navigation Row
        val nav = LinearLayout(activity).apply {
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, (2 * DENSITY).toInt(), 0, (15 * DENSITY).toInt())
        }
        val prev = TextView(activity).apply {
            text = "❮"
            textSize = 22f
            val padH = (15 * DENSITY).toInt()
            val padV = (10 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            setTextColor(colorAccent)
            setOnClickListener {
                val check = calendarViewPointer.clone() as Calendar
                check.add(Calendar.MONTH, -1)
                if (check.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) {
                    calendarViewPointer.add(Calendar.MONTH, -1)
                    renderGregorian(card, dialog)
                } else {
                    ui.showSmartBanner(
                        activity.findViewById(android.R.id.content),
                        lang.get("Limit Reached"),
                        lang.get("Cannot go back more than 100 years."),
                        "img_warning",
                        colorAccent,
                        null
                    )
                }
            }
        }

        val title = TextView(activity).apply {
            text = lang.get(monthOnlyF.format(calendarViewPointer.time))
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
        }

        val now = Calendar.getInstance()
        val isFutureMonth = (calendarViewPointer.get(Calendar.YEAR) > now.get(Calendar.YEAR)) ||
            (calendarViewPointer.get(Calendar.YEAR) == now.get(Calendar.YEAR) && calendarViewPointer.get(Calendar.MONTH) >= now.get(Calendar.MONTH))

        val next = TextView(activity).apply {
            text = "❯"
            textSize = 22f
            val padH = (15 * DENSITY).toInt()
            val padV = (10 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            setTextColor(if (isFutureMonth) Color.LTGRAY else colorAccent)
            setOnClickListener {
                if (!isFutureMonth) {
                    calendarViewPointer.add(Calendar.MONTH, 1)
                    renderGregorian(card, dialog)
                }
            }
        }
        nav.addView(prev)
        nav.addView(title)
        nav.addView(next)
        card.addView(nav)

        // Day Headers
        val daysRow = LinearLayout(activity)
        val days = if (lang.get("Fajr") == "ফজর") {
            arrayOf("র", "সো", "ম", "বু", "বৃ", "শু", "শ")
        } else {
            arrayOf("S", "M", "T", "W", "T", "F", "S")
        }
        for (d in days) {
            val tv = TextView(activity).apply {
                text = d
                gravity = Gravity.CENTER
                setTextColor(themeColors[3])
                textSize = 12f
                typeface = Typeface.DEFAULT_BOLD
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            }
            daysRow.addView(tv)
        }
        card.addView(daysRow)

        // Day Grid
        val temp = calendarViewPointer.clone() as Calendar
        temp.set(Calendar.DAY_OF_MONTH, 1)
        val offset = temp.get(Calendar.DAY_OF_WEEK) - 1
        val totalDays = temp.getActualMaximum(Calendar.DAY_OF_MONTH)
        var currentDay = 1
        val cellHeight = (46 * DENSITY + 0.5f).toInt()
        val boxSize = (36 * DENSITY + 0.5f).toInt()

        val gridContainer = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
        }

        for (row in 0 until 6) {
            val rowLay = LinearLayout(activity)
            for (col in 0 until 7) {
                val cell = FrameLayout(activity).apply {
                    layoutParams = LinearLayout.LayoutParams(0, cellHeight, 1f)
                }

                if (!((row == 0 && col < offset) || currentDay > totalDays)) {
                    val dayNum = currentDay
                    temp.set(Calendar.DAY_OF_MONTH, dayNum)
                    val dKey = sdf.format(temp.time)
                    val isFuture = temp.after(now)
                    val isTooOld = temp.get(Calendar.YEAR) < now.get(Calendar.YEAR) - 100

                    val dRec = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(dKey)
                    val isDayCompleted = dRec != null && prayers.all { p ->
                        val st = dRec.getFardStat(p)
                        st == "yes" || st == "excused"
                    }

                    val isSelected = dKey == selectedDate[0]

                    val tv = TextView(activity).apply {
                        text = lang.bnNum(dayNum)
                        setTextColor(
                            if (isSelected) Color.WHITE
                            else if (isFuture) themeColors[4]
                            else if (isDayCompleted) colorAccent
                            else themeColors[2]
                        )
                        textSize = 13f
                        gravity = Gravity.CENTER
                        typeface = Typeface.DEFAULT_BOLD
                        layoutParams = FrameLayout.LayoutParams(boxSize, boxSize).apply {
                            gravity = Gravity.CENTER
                        }
                    }

                    if (isSelected || (isDayCompleted && !isFuture)) {
                        tv.background = (activity as MainActivity).getProgressBorder(dKey, isSelected)
                    } else {
                        tv.background = null
                    }

                    cell.addView(tv)
                    cell.setOnClickListener {
                        when {
                            isFuture -> ui.showPremiumLocked(colorAccent)
                            isTooOld -> ui.showSmartBanner(
                                activity.findViewById(android.R.id.content),
                                lang.get("Limit Reached"),
                                lang.get("Cannot go back more than 100 years."),
                                "img_warning",
                                colorAccent,
                                null
                            )
                            else -> {
                                selectedDate[0] = dKey
                                dialog.dismiss()
                                onDateSelected?.run()
                            }
                        }
                    }
                    currentDay++
                }
                rowLay.addView(cell)
            }
            gridContainer.addView(rowLay)
            if (currentDay > totalDays) break
        }
        card.addView(gridContainer)

        val close = TextView(activity).apply {
            text = lang.get("CLOSE")
            setTextColor(themeColors[3])
            val padH = (15 * DENSITY).toInt()
            setPadding(padH, padH, padH, (5 * DENSITY).toInt())
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setOnClickListener { dialog.dismiss() }
        }
        card.addView(close)
    }

    private fun showYearPicker(parentCard: LinearLayout, calDialog: AlertDialog) {
        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val container = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val pad = (25 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 30f * DENSITY
            }
        }
        val title = TextView(activity).apply {
            text = lang.get("Select Year")
            gravity = Gravity.CENTER
            setTextColor(themeColors[2])
            textSize = 18f
            setPadding(0, 0, 0, (20 * DENSITY).toInt())
            typeface = Typeface.DEFAULT_BOLD
        }
        container.addView(title)

        val scroll = ScrollView(activity)
        val list = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
        }
        val realCurrentCal = Calendar.getInstance()
        val currentRealYear = realCurrentCal.get(Calendar.YEAR)
        val currentRealMonth = realCurrentCal.get(Calendar.MONTH)

        var yearDialog: AlertDialog? = null

        for (y in currentRealYear downTo currentRealYear - 100) {
            val year = y
            val yTv = TextView(activity).apply {
                text = lang.bnNum(year)
                gravity = Gravity.CENTER
                setPadding(0, (15 * DENSITY).toInt(), 0, (15 * DENSITY).toInt())
                textSize = 18f
                setTextColor(if (calendarViewPointer.get(Calendar.YEAR) == year) colorAccent else themeColors[2])
                setOnClickListener {
                    calendarViewPointer.set(Calendar.YEAR, year)
                    if (year == currentRealYear) {
                        calendarViewPointer.set(Calendar.MONTH, currentRealMonth)
                    }
                    renderGregorian(parentCard, calDialog)
                    yearDialog?.dismiss()
                }
            }
            list.addView(yTv)
        }
        scroll.addView(list)
        container.addView(scroll, -1, (350 * DENSITY).toInt())

        val flp = FrameLayout.LayoutParams((300 * DENSITY).toInt(), -2).apply {
            gravity = Gravity.CENTER
        }
        wrap.addView(container, flp)

        yearDialog = AlertDialog.Builder(activity).setView(wrap).create().apply {
            window?.setBackgroundDrawableResource(android.R.color.transparent)
            window?.setGravity(Gravity.CENTER)
            wrap.applyFont(tfReg, tfBold)
            show()
        }
    }

    fun showHijri() {
        if (Build.VERSION.SDK_INT < 24) return

        try {
            sdf.parse(selectedDate[0])?.let { hijriViewCal.time = it }
        } catch (_: Exception) {}

        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val main = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (20 * DENSITY).toInt()
            val padV = (25 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 25f * DENSITY
                setStroke((1.5f * DENSITY).toInt(), themeColors[4])
            }
        }

        val yearChip = TextView(activity).apply {
            setTextColor(colorAccent)
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            val padH = (25 * DENSITY).toInt()
            val padV = (8 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            background = GradientDrawable().apply {
                setColor(colorAccent and 0x15FFFFFF)
                cornerRadius = 15f * DENSITY
            }
            layoutParams = LinearLayout.LayoutParams(-2, -2).apply {
                gravity = Gravity.CENTER_HORIZONTAL
                setMargins(0, 0, 0, (15 * DENSITY).toInt())
            }
        }
        main.addView(yearChip)

        val nav = LinearLayout(activity).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        val prev = TextView(activity).apply {
            text = "❮"
            val pad = (15 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
        }
        val monthTitle = TextView(activity).apply {
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            gravity = Gravity.CENTER
            setTextColor(themeColors[2])
            typeface = Typeface.DEFAULT_BOLD
            textSize = 18f
        }
        val next = TextView(activity).apply {
            text = "❯"
            val pad = (15 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
        }
        nav.addView(prev)
        nav.addView(monthTitle)
        nav.addView(next)
        main.addView(nav)

        val daysRow = LinearLayout(activity)
        val wDays = if (lang.get("Fajr") == "ফজর") {
            arrayOf("র", "সো", "ম", "বু", "বৃ", "শু", "শ")
        } else {
            arrayOf("S", "M", "T", "W", "T", "F", "S")
        }
        for (d in wDays) {
            val dt = TextView(activity).apply {
                text = d
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
                gravity = Gravity.CENTER
                setTextColor(themeColors[3])
                typeface = Typeface.DEFAULT_BOLD
                textSize = 12f
                setPadding(0, 0, 0, (10 * DENSITY).toInt())
            }
            daysRow.addView(dt)
        }
        main.addView(daysRow)

        val grid = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
        }
        main.addView(grid)

        val footer = LinearLayout(activity).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(0, (15 * DENSITY).toInt(), 0, (15 * DENSITY).toInt())
        }
        val cancelBtn = TextView(activity).apply {
            text = lang.get("CLOSE")
            setTextColor(themeColors[3])
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            val padH = (15 * DENSITY).toInt()
            setPadding(padH, padH, padH, (5 * DENSITY).toInt())
        }
        footer.addView(cancelBtn)
        main.addView(footer)

        val ad = AlertDialog.Builder(activity).setView(wrap).create().apply {
            window?.setBackgroundDrawableResource(android.R.color.transparent)
            window?.setGravity(Gravity.CENTER)
        }
        cancelBtn.setOnClickListener { ad.dismiss() }

        var renderHijriGrid: (() -> Unit)? = null

        yearChip.setOnClickListener {
            val yWrap = FrameLayout(activity).apply {
                layoutParams = FrameLayout.LayoutParams(-1, -1)
            }
            val yMain = LinearLayout(activity).apply {
                orientation = LinearLayout.VERTICAL
                val pad = (25 * DENSITY).toInt()
                setPadding(pad, pad, pad, pad)
                background = GradientDrawable().apply {
                    setColor(themeColors[1])
                    cornerRadius = 30f * DENSITY
                    setStroke((1.5f * DENSITY).toInt(), themeColors[4])
                }
            }
            val yTitle = TextView(activity).apply {
                text = lang.get("Select Year")
                setTextColor(themeColors[2])
                textSize = 20f
                typeface = Typeface.DEFAULT_BOLD
                gravity = Gravity.CENTER
                setPadding(0, 0, 0, (15 * DENSITY).toInt())
            }
            yMain.addView(yTitle)

            val sv = ScrollView(activity)
            val list = LinearLayout(activity).apply {
                orientation = LinearLayout.VERTICAL
                val padH = (20 * DENSITY).toInt()
                setPadding(padH, 0, padH, 0)
            }

            val offset = sp.getInt("hijri_offset", 0)
            val tempIc = IslamicCalendar().apply {
                time = Date()
                add(IslamicCalendar.DATE, offset)
            }
            val currentRealHYear = tempIc.get(IslamicCalendar.YEAR)

            val viewIc = IslamicCalendar().apply {
                time = hijriViewCal.time
                add(IslamicCalendar.DATE, offset)
            }
            val viewHYear = viewIc.get(IslamicCalendar.YEAR)

            var yAd: AlertDialog? = null

            for (y in currentRealHYear downTo currentRealHYear - 100) {
                val selectedY = y
                val yt = TextView(activity).apply {
                    text = "${lang.bnNum(y)} ${lang.get("AH")}"
                    textSize = 18f
                    setPadding(0, (15 * DENSITY).toInt(), 0, (15 * DENSITY).toInt())
                    gravity = Gravity.CENTER
                    typeface = if (y == viewHYear) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
                    setTextColor(if (y == viewHYear) colorAccent else themeColors[2])
                    setOnClickListener {
                        val shiftIc = IslamicCalendar().apply {
                            time = hijriViewCal.time
                            add(IslamicCalendar.DATE, offset)
                            set(IslamicCalendar.YEAR, selectedY)
                            add(IslamicCalendar.DATE, -offset)
                        }
                        hijriViewCal.time = shiftIc.time
                        yAd?.dismiss()
                        renderHijriGrid?.invoke()
                    }
                    layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                        setMargins(0, 0, 0, (5 * DENSITY).toInt())
                    }
                }
                list.addView(yt)
            }
            sv.addView(list)
            yMain.addView(sv, LinearLayout.LayoutParams(-1, (350 * DENSITY).toInt()))

            val yFlp = FrameLayout.LayoutParams((300 * DENSITY).toInt(), -2).apply {
                gravity = Gravity.CENTER
            }
            yWrap.addView(yMain, yFlp)
            yWrap.applyFont(tfReg, tfBold)

            yAd = AlertDialog.Builder(activity).setView(yWrap).create().apply {
                window?.setBackgroundDrawableResource(android.R.color.transparent)
                window?.setGravity(Gravity.CENTER)
                show()
            }
        }

        renderHijriGrid = {
            grid.removeAllViews()
            val offset = sp.getInt("hijri_offset", 0)
            val ic = IslamicCalendar().apply {
                time = hijriViewCal.time
                add(IslamicCalendar.DATE, offset)
            }
            val hMonths = arrayOf(
                "Muharram", "Safar", "Rabi I", "Rabi II", "Jumada I",
                "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal",
                "Dhu al-Qi'dah", "Dhu al-Hijjah"
            )

            yearChip.text = "${lang.bnNum(ic.get(IslamicCalendar.YEAR))} ${lang.get("AH")}"
            monthTitle.text = lang.get(hMonths[ic.get(IslamicCalendar.MONTH)])

            val todayCal = Calendar.getInstance()
            val todayIc = IslamicCalendar().apply {
                time = todayCal.time
                add(IslamicCalendar.DATE, offset)
            }
            val isFutureMonth = (ic.get(IslamicCalendar.YEAR) > todayIc.get(IslamicCalendar.YEAR)) ||
                (ic.get(IslamicCalendar.YEAR) == todayIc.get(IslamicCalendar.YEAR) && ic.get(IslamicCalendar.MONTH) >= todayIc.get(IslamicCalendar.MONTH))

            next.alpha = if (isFutureMonth) 0.3f else 1f
            ic.set(IslamicCalendar.DAY_OF_MONTH, 1)
            val startDOW = ic.get(IslamicCalendar.DAY_OF_WEEK)
            val maxDays = ic.getActualMaximum(IslamicCalendar.DAY_OF_MONTH)
            var cellCount = 1
            var dayNum = 1

            for (r in 0 until 6) {
                val row = LinearLayout(activity).apply {
                    orientation = LinearLayout.HORIZONTAL
                }
                for (c in 0 until 7) {
                    val cell = FrameLayout(activity).apply {
                        layoutParams = LinearLayout.LayoutParams(0, (45 * DENSITY).toInt(), 1f)
                    }
                    if (cellCount >= startDOW && dayNum <= maxDays) {
                        val currentDay = dayNum
                        val dTv = TextView(activity).apply {
                            text = lang.bnNum(currentDay)
                            gravity = Gravity.CENTER
                            typeface = Typeface.DEFAULT_BOLD
                            layoutParams = FrameLayout.LayoutParams((35 * DENSITY).toInt(), (35 * DENSITY).toInt()).apply {
                                gravity = Gravity.CENTER
                            }
                        }
                        val cellIc = ic.clone() as IslamicCalendar
                        cellIc.set(IslamicCalendar.DAY_OF_MONTH, currentDay)
                        val realGregorian = Calendar.getInstance().apply {
                            time = cellIc.time
                            add(Calendar.DATE, -offset)
                        }
                        val cellDateKey = sdf.format(realGregorian.time)
                        val isSelected = cellDateKey == selectedDate[0]
                        val isFutureDate = realGregorian.time.after(todayCal.time) && cellDateKey != sdf.format(todayCal.time)
                        val isTooOld = realGregorian.get(Calendar.YEAR) < todayCal.get(Calendar.YEAR) - 100

                        val dRec = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(cellDateKey)
                        val isAllDone = dRec != null && prayers.all { p ->
                            val st = dRec.getFardStat(p)
                            st == "yes" || st == "excused"
                        }

                        dTv.setTextColor(
                            if (isSelected) Color.WHITE
                            else if (isFutureDate) themeColors[4]
                            else if (isAllDone) colorAccent
                            else themeColors[2]
                        )

                        if (isSelected || (isAllDone && !isFutureDate)) {
                            dTv.background = (activity as MainActivity).getProgressBorder(cellDateKey, isSelected)
                        }

                        cell.addView(dTv)
                        cell.setOnClickListener {
                            when {
                                isFutureDate -> ui.showPremiumLocked(colorAccent)
                                isTooOld -> ui.showSmartBanner(
                                    activity.findViewById(android.R.id.content),
                                    lang.get("Limit Reached"),
                                    lang.get("Cannot go back more than 100 years."),
                                    "img_warning",
                                    colorAccent,
                                    null
                                )
                                else -> {
                                    selectedDate[0] = cellDateKey
                                    ad.dismiss()
                                    onDateSelected?.run()
                                }
                            }
                        }
                        dayNum++
                    }
                    row.addView(cell)
                    cellCount++
                }
                grid.addView(row)
                if (dayNum > maxDays) break
            }
        }

        prev.setOnClickListener {
            val chk = hijriViewCal.clone() as Calendar
            chk.add(Calendar.DATE, -29)
            if (chk.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) {
                hijriViewCal.add(Calendar.DATE, -29)
                renderHijriGrid.invoke()
            } else {
                ui.showSmartBanner(
                    activity.findViewById(android.R.id.content),
                    lang.get("Limit Reached"),
                    lang.get("Cannot go back more than 100 years."),
                    "img_warning",
                    colorAccent,
                    null
                )
            }
        }

        next.setOnClickListener {
            val offset = sp.getInt("hijri_offset", 0)
            val currentIc = IslamicCalendar().apply {
                time = hijriViewCal.time
                add(IslamicCalendar.DATE, offset)
            }
            val todayIc = IslamicCalendar().apply {
                time = Date()
                add(IslamicCalendar.DATE, offset)
            }
            if (currentIc.get(IslamicCalendar.YEAR) < todayIc.get(IslamicCalendar.YEAR) ||
                (currentIc.get(IslamicCalendar.YEAR) == todayIc.get(IslamicCalendar.YEAR) && currentIc.get(IslamicCalendar.MONTH) < todayIc.get(IslamicCalendar.MONTH))) {
                hijriViewCal.add(Calendar.DATE, 30)
                renderHijriGrid.invoke()
            }
        }

        renderHijriGrid.invoke()
        val flp = FrameLayout.LayoutParams(-1, -2).apply {
            gravity = Gravity.CENTER
            setMargins((20 * DENSITY).toInt(), 0, (20 * DENSITY).toInt(), 0)
        }
        wrap.addView(main, flp)
        wrap.applyFont(tfReg, tfBold)
        if (!activity.isFinishing) {
            ad.show()
        }
    }
}
