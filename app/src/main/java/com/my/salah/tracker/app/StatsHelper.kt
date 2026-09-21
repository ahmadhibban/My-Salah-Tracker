package com.my.salah.tracker.app

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.graphics.pdf.PdfDocument
import android.net.Uri
import android.os.Environment
import android.os.Handler
import android.os.Looper
import android.os.StrictMode
import android.view.Gravity
import android.view.View
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.core.content.FileProvider
import com.github.mikephil.charting.charts.BarChart
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.formatter.ValueFormatter
import com.github.mikephil.charting.highlight.Highlight
import com.github.mikephil.charting.interfaces.datasets.IBarDataSet
import com.github.mikephil.charting.listener.OnChartValueSelectedListener
import com.github.mikephil.charting.renderer.BarChartRenderer
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStreamWriter
import java.io.PrintWriter
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class StatsHelper(
    private val activity: Activity,
    private val DENSITY: Float,
    private val themeColors: IntArray,
    private val colorAccent: Int,
    private val lang: LanguageEngine,
    private val ui: UIComponents,
    private val sp: SharedPreferences,
    private val prayers: Array<String>,
    private val appFonts: Array<Typeface?>
) {
    private val statsCalPointer: Calendar = Calendar.getInstance()

    private fun getRoomRecord(date: String): SalahRecord? {
        return SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(date)
    }

    private fun getTotalExtras(dKey: String): Int {
        var c = 0
        for (p in prayers.indices) {
            val pr = prayers[p]
            for (sn in AppConstants.SUNNAHS[p]) {
                if (sp.getString("${dKey}_${pr}_Sunnah_$sn", "no") == "yes") c++
            }
            val cStr = sp.getString("custom_nafl_$pr", "") ?: ""
            if (cStr.isNotEmpty()) {
                for (item in cStr.split(",")) {
                    val cN = if (item.contains(":")) item.split(":")[0] else item
                    if (sp.getString("${dKey}_${pr}_Custom_$cN", "no") == "yes") c++
                }
            }
        }
        return c
    }

    fun exportXls() {
        val isBn = sp.getString("app_lang", "en") == "bn"
        try {
            val dir = activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
            if (dir != null && !dir.exists()) dir.mkdirs()
            val file = File(dir, "Salah_Premium_Report_${System.currentTimeMillis()}.xls")
            val pw = PrintWriter(OutputStreamWriter(FileOutputStream(file), "UTF-8"))

            var tD = 0
            var tDn = 0
            var tM = 0
            var tE = 0
            var tQ = 0
            var tExt = 0

            val sumCal = statsCalPointer.clone() as Calendar
            sumCal.set(Calendar.DAY_OF_MONTH, 1)
            val mDays = sumCal.getActualMaximum(Calendar.DAY_OF_MONTH)
            val nowSum = Calendar.getInstance()
            val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.US)

            for (j in 1..mDays) {
                sumCal.set(Calendar.DAY_OF_MONTH, j)
                val dk = sdf.format(sumCal.time)
                if (sumCal.after(nowSum) && dk != sdf.format(nowSum.time)) continue
                tD++
                val rec = getRoomRecord(dk)
                if (rec != null) {
                    for (p in prayers) {
                        val st = rec.getFardStat(p)
                        when (st) {
                            "yes" -> tDn++
                            "excused" -> tE++
                            else -> {
                                if (rec.getQazaStat(p)) tQ++ else tM++
                            }
                        }
                    }
                }
                tExt += getTotalExtras(dk)
            }

            val streak = ui.calculateStreak(sp, prayers)
            val title = (if (isBn) "মাসিক রিপোর্ট • " else "Monthly Report • ") +
                SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.time)

            val xml = StringBuilder().apply {
                append("<?xml version=\"1.0\" encoding=\"UTF-8\"?><?mso-application progid=\"Excel.Sheet\"?><Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\" xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\"><Styles><Style ss:ID=\"Default\" ss:Name=\"Normal\"><Alignment ss:Vertical=\"Center\"/></Style>")
                append("<Style ss:ID=\"sTitle\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"22\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#10B981\" ss:Pattern=\"Solid\"/></Style>")
                append("<Style ss:ID=\"sSumH\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"13\" ss:Bold=\"1\" ss:Color=\"#5F6368\"/><Interior ss:Color=\"#F8F9FA\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>")
                append("<Style ss:ID=\"sSumV\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"16\" ss:Bold=\"1\" ss:Color=\"#202124\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#10B981\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>")
                append("<Style ss:ID=\"sHead\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"14\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#334155\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#0F172A\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>")
                append("<Style ss:ID=\"sDate\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#334155\"/><Interior ss:Color=\"#F8FAFC\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>")
                append("<Style ss:ID=\"sYes\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#059669\"/><Interior ss:Color=\"#D1FAE5\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>")
                append("<Style ss:ID=\"sNo\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#DC2626\"/><Interior ss:Color=\"#FEE2E2\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>")
                append("<Style ss:ID=\"sExc\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#7C3AED\"/><Interior ss:Color=\"#EDE9FE\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>")
                append("<Style ss:ID=\"sExt\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#D97706\"/><Interior ss:Color=\"#FEF3C7\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>")
                append("</Styles><Worksheet ss:Name=\"Report\"><Table><Column ss:Width=\"150\"/>")
                for (i in 0 until 6) append("<Column ss:Width=\"115\"/>")
                append("<Column ss:Width=\"130\"/><Column ss:Width=\"160\"/>")
                append("<Row ss:Height=\"70\"><Cell ss:MergeAcross=\"8\" ss:StyleID=\"sTitle\"><Data ss:Type=\"String\">$title</Data></Cell></Row>")

                val em = sp.getString("user_email", "guest@salah.com")
                append("<Row ss:Height=\"30\"><Cell ss:MergeAcross=\"8\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">$em</Data></Cell></Row><Row ss:Height=\"20\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>")
                append("<Row ss:Height=\"40\"><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">${if (isBn) "মোট দিন" else "Total Days"}</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">${if (isBn) "আদায়কৃত" else "Done"}</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">${if (isBn) "কাজা" else "Missed"}</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">${if (isBn) "অপেক্ষমান কাজা" else "Pending Qaza"}</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">${if (isBn) "ছুটি" else "Excused"}</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">${if (isBn) "নফল/সুন্নাহ" else "Extras"}</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">${if (isBn) "স্ট্রিক" else "Streak"}</Data></Cell></Row>")
                append("<Row ss:Height=\"50\"><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">${lang.bnNum(tD)}</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">${lang.bnNum(tDn)}</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">${lang.bnNum(tM)}</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">${lang.bnNum(tQ)}</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">${lang.bnNum(tE)}</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">${lang.bnNum(tExt)}</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">${lang.bnNum(streak)} ★</Data></Cell></Row><Row ss:Height=\"25\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>")

                append("<Row ss:Height=\"45\">")
                val hdrs = if (isBn) {
                    arrayOf("তারিখ", "ফজর", "যোহর", "আসর", "মাগরিব", "এশা", "বিতর", "অতিরিক্ত (নফল)", "সারসংক্ষেপ")
                } else {
                    arrayOf("Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr", "Extras (Nafl)", "Status")
                }
                for (h in hdrs) {
                    append("<Cell ss:StyleID=\"sHead\"><Data ss:Type=\"String\">$h</Data></Cell>")
                }
                append("</Row>")

                val cal = statsCalPointer.clone() as Calendar
                cal.set(Calendar.DAY_OF_MONTH, 1)
                for (i in 1..mDays) {
                    cal.set(Calendar.DAY_OF_MONTH, i)
                    val dK = sdf.format(cal.time)
                    val r = getRoomRecord(dK)
                    val dDisp = if (isBn) {
                        "${lang.bnNum(i)} ${lang.get(SimpleDateFormat("MMM", Locale.US).format(cal.time))}, ${lang.bnNum(cal.get(Calendar.YEAR))}"
                    } else {
                        dK
                    }
                    append("<Row ss:Height=\"40\"><Cell ss:StyleID=\"sDate\"><Data ss:Type=\"String\">$dDisp</Data></Cell>")
                    var aD = true
                    for (p in prayers) {
                        val s = r?.getFardStat(p) ?: "no"
                        val sty = if (s == "yes") "sYes" else if (s == "excused") "sExc" else "sNo"
                        val txt = when (s) {
                            "yes" -> "\u2713 " + (if (isBn) "সম্পন্ন" else "Done")
                            "excused" -> "\u273F " + (if (isBn) "ছুটি" else "Excused")
                            else -> "\u2715 " + (if (isBn) "কাজা" else "Missed")
                        }
                        append("<Cell ss:StyleID=\"$sty\"><Data ss:Type=\"String\">$txt</Data></Cell>")
                        if (s != "yes" && s != "excused") aD = false
                    }
                    val dEx = getTotalExtras(dK)
                    val exTxt = if (dEx > 0) "+ ${lang.bnNum(dEx)}" else "-"
                    append("<Cell ss:StyleID=\"sExt\"><Data ss:Type=\"String\">$exTxt</Data></Cell>")
                    val sSt = if (aD) "sYes" else "sNo"
                    val sTxt = if (aD) (if (isBn) "★ আলহামদুলিল্লাহ" else "★ Perfect") else (if (isBn) "⚠ অসম্পূর্ণ" else "⚠ Incomplete")
                    append("<Cell ss:StyleID=\"$sSt\"><Data ss:Type=\"String\">$sTxt</Data></Cell></Row>")
                }
                append("</Table></Worksheet></Workbook>")
            }

            pw.write(xml.toString())
            pw.close()

            ui.showSmartBanner(
                activity.findViewById(android.R.id.content),
                if (isBn) "সফল" else "Success",
                if (isBn) "XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)" else "XLS Saved",
                "img_tick",
                colorAccent
            ) {
                val intent = Intent(Intent.ACTION_VIEW).apply {
                    setDataAndType(
                        FileProvider.getUriForFile(activity, "${activity.packageName}.provider", file),
                        "application/vnd.ms-excel"
                    )
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                activity.startActivity(Intent.createChooser(intent, "Open with..."))
            }
        } catch (_: Exception) {}
    }

    fun showStatsOptionsDialog() {
        val isBn = sp.getString("app_lang", "en") == "bn"
        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val main = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (25 * DENSITY).toInt()
            val padV = (30 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 25f * DENSITY
            }
        }
        val title = TextView(activity).apply {
            text = if (isBn) "উন্নত পরিসংখ্যান" else "Advanced Statistics"
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, (20 * DENSITY).toInt())
        }
        main.addView(title)

        val ad = AlertDialog.Builder(activity).setView(wrap).create().apply {
            window?.setBackgroundDrawableResource(android.R.color.transparent)
            window?.setGravity(Gravity.CENTER)
        }

        fun addButton(t: String, act: () -> Unit) {
            val btn = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                val pad = (15 * DENSITY).toInt()
                setPadding(pad, pad, pad, pad)
                background = GradientDrawable().apply {
                    setColor(themeColors[4])
                    cornerRadius = 15f * DENSITY
                }
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, (10 * DENSITY).toInt())
                }
            }
            val dot = View(activity).apply {
                background = GradientDrawable().apply {
                    shape = GradientDrawable.OVAL
                    setColor(colorAccent)
                }
                layoutParams = LinearLayout.LayoutParams((10 * DENSITY).toInt(), (10 * DENSITY).toInt())
            }
            btn.addView(dot)

            val tv = TextView(activity).apply {
                text = t
                setTextColor(themeColors[2])
                textSize = 16f
                typeface = Typeface.DEFAULT_BOLD
                setPadding((15 * DENSITY).toInt(), 0, 0, 0)
            }
            btn.addView(tv)

            btn.setOnClickListener {
                ad.dismiss()
                act.invoke()
            }
            main.addView(btn)
        }

        addButton(if (isBn) "সাপ্তাহিক পরিসংখ্যান" else "Weekly Statistics") { showStats(true) }
        addButton(if (isBn) "মাসিক পরিসংখ্যান" else "Monthly Statistics") { showStats(false) }
        addButton(if (isBn) "রিপোর্ট শেয়ার (ছবি)" else "Share Report (Image)") { showShareTypeDialog() }
        addButton(if (isBn) "প্রিমিয়াম এক্সেল (XLS) এক্সপোর্ট" else "Export Premium XLS") { exportXls() }
        addButton(if (isBn) "প্রিমিয়াম পিডিএফ এক্সপোর্ট" else "Export Premium PDF") { exportPdf() }

        val flp = FrameLayout.LayoutParams((300 * DENSITY).toInt(), -2).apply {
            gravity = Gravity.CENTER
        }
        wrap.addView(main, flp)
        wrap.applyFont(appFonts[0], appFonts[1])

        if (!activity.isFinishing) {
            ad.show()
        }
    }

    private fun showShareTypeDialog() {
        val isBn = sp.getString("app_lang", "en") == "bn"
        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val main = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (25 * DENSITY).toInt()
            val padV = (30 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 25f * DENSITY
            }
        }
        val title = TextView(activity).apply {
            text = if (isBn) "রিপোর্টের ধরন নির্বাচন করুন" else "Select Report Type"
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, (20 * DENSITY).toInt())
        }
        main.addView(title)

        val ad = AlertDialog.Builder(activity).setView(wrap).create().apply {
            window?.setBackgroundDrawableResource(android.R.color.transparent)
            window?.setGravity(Gravity.CENTER)
        }

        val btn1 = LinearLayout(activity).apply {
            val pad = (15 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
            gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                setColor(colorAccent)
                cornerRadius = 15f * DENSITY
            }
            setOnClickListener {
                ad.dismiss()
                shareImageReport(true)
            }
        }
        val t1 = TextView(activity).apply {
            text = if (isBn) "সাপ্তাহিক রিপোর্ট" else "Weekly Report"
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }
        btn1.addView(t1)
        main.addView(btn1)

        val btn2 = LinearLayout(activity).apply {
            val pad = (15 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
            gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                setColor(themeColors[4])
                cornerRadius = 15f * DENSITY
            }
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, (10 * DENSITY).toInt(), 0, 0)
            }
            setOnClickListener {
                ad.dismiss()
                shareImageReport(false)
            }
        }
        val t2 = TextView(activity).apply {
            text = if (isBn) "মাসিক রিপোর্ট" else "Monthly Report"
            setTextColor(themeColors[2])
            typeface = Typeface.DEFAULT_BOLD
        }
        btn2.addView(t2)
        main.addView(btn2)

        val flp = FrameLayout.LayoutParams((300 * DENSITY).toInt(), -2).apply {
            gravity = Gravity.CENTER
        }
        wrap.addView(main, flp)
        wrap.applyFont(appFonts[0], appFonts[1])

        if (!activity.isFinishing) {
            ad.show()
        }
    }

    fun shareImageReport(isWeekly: Boolean) {
        val isBn = sp.getString("app_lang", "en") == "bn"
        try {
            val w = 2160
            val h = 2850
            val bm = Bitmap.createBitmap(w, h, Bitmap.Config.RGB_565)
            val cv = Canvas(bm)
            val pt = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                color = themeColors[0]
            }
            cv.drawRect(0f, 0f, w.toFloat(), h.toFloat(), pt)

            val ph = Path().apply {
                moveTo(0f, 0f)
                lineTo(w.toFloat(), 0f)
                lineTo(w.toFloat(), 550f)
                cubicTo(w / 2f, 750f, w / 2f, 350f, 0f, 550f)
                close()
            }
            pt.color = colorAccent
            cv.drawPath(ph, pt)

            pt.color = Color.WHITE
            pt.textAlign = Paint.Align.CENTER
            pt.textSize = 120f
            pt.typeface = Typeface.create(appFonts[1], Typeface.BOLD)
            cv.drawText("My Salah Tracker", w / 2f, 220f, pt)

            pt.textSize = 60f
            pt.typeface = appFonts[0]
            var em = sp.getString("user_email", "guest@salah.com") ?: "guest@salah.com"
            if (em.length > 25) em = em.substring(0, 22) + "..."
            cv.drawText(em, w / 2f, 320f, pt)

            pt.textSize = 70f
            pt.typeface = appFonts[1]
            cv.drawText(
                if (isWeekly) (if (isBn) "সাপ্তাহিক রিপোর্ট" else "Weekly Report")
                else (if (isBn) "মাসিক রিপোর্ট" else "Monthly Report"),
                w / 2f, 440f, pt
            )

            var eC = statsCalPointer.clone() as Calendar
            val sC = statsCalPointer.clone() as Calendar
            val now = Calendar.getInstance()

            if (isWeekly) {
                while (sC.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) sC.add(Calendar.DATE, -1)
                eC = sC.clone() as Calendar
                eC.add(Calendar.DATE, 6)
                if (eC.after(now)) eC = now
            } else {
                sC.set(Calendar.DAY_OF_MONTH, 1)
                eC.set(Calendar.DAY_OF_MONTH, sC.getActualMaximum(Calendar.DAY_OF_MONTH))
                if (eC.after(now)) eC = now
            }

            val sk = SimpleDateFormat("yyyy-MM-dd", Locale.US)
            val sd = SimpleDateFormat("EEEE", Locale.US)
            val gR = "${lang.getShortGreg(sC.time)} - ${lang.getShortGreg(eC.time)}"
            val hR = "${ui.getHijriDate(sC.time, sp.getInt("hijri_offset", 0))} - ${ui.getHijriDate(eC.time, sp.getInt("hijri_offset", 0))}"
            var sDy = lang.get(sd.format(sC.time))
            var eDy = lang.get(sd.format(eC.time))
            if (isBn) {
                val bD = arrayOf("রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার")
                sDy = bD[sC.get(Calendar.DAY_OF_WEEK) - 1]
                eDy = bD[eC.get(Calendar.DAY_OF_WEEK) - 1]
            }

            pt.color = themeColors[2]
            pt.textSize = 55f
            pt.typeface = appFonts[1]
            cv.drawText(gR, w / 2f, 750f, pt)

            pt.color = themeColors[3]
            pt.textSize = 45f
            pt.typeface = appFonts[0]
            cv.drawText(hR, w / 2f, 830f, pt)
            cv.drawText("$sDy - $eDy", w / 2f, 900f, pt)

            var tD = 0
            var tDn = 0
            var tM = 0
            var tE = 0
            var tQ = 0
            val lC = sC.clone() as Calendar
            val dFV = ArrayList<Float>()
            val dSV = ArrayList<Float>()
            val dC = ArrayList<Int>()
            val dL = ArrayList<String>()

            while (!lC.after(eC)) {
                tD++
                val dK = sk.format(lC.time)
                val r = getRoomRecord(dK)
                var dyDn = 0
                var dyE = 0
                var sC_cnt = 0
                if (r != null) {
                    for (p in prayers) {
                        val st = r.getFardStat(p)
                        when (st) {
                            "yes" -> {
                                tDn++
                                dyDn++
                            }
                            "excused" -> {
                                tE++
                                dyE++
                            }
                            else -> {
                                if (r.getQazaStat(p)) tQ++ else tM++
                            }
                        }
                    }
                    if (isWeekly) sC_cnt += getTotalExtras(dK)
                }
                dFV.add((dyDn + dyE).toFloat())
                dSV.add(sC_cnt.toFloat())
                if (lC.after(now) && dK != sk.format(now.time)) {
                    dC.add(Color.TRANSPARENT)
                } else if (dyDn + dyE == 0) {
                    dC.add(Color.TRANSPARENT)
                } else if (dyE > 0) {
                    dC.add(Color.parseColor("#8B5CF6"))
                } else {
                    dC.add(Color.parseColor("#22C55E"))
                }

                dL.add(if (isWeekly) lang.get(sd.format(lC.time)).substring(0, 3) else lang.bnNum(lC.get(Calendar.DAY_OF_MONTH)))
                lC.add(Calendar.DATE, 1)
            }

            val sY = 1050f
            val pd = 80f
            val cW = (w - (pd * 3)) / 2f
            val cH = 280f

            drawReportCard(cv, pt, pd, sY, cW, cH, colorAccent, if (isBn) "মোট দিন" else "Total Days", lang.bnNum(tD))
            drawReportCard(cv, pt, pd * 2 + cW, sY, cW, cH, Color.parseColor("#3B82F6"), if (isBn) "আদায়কৃত নামাজ" else "Prayers Done", lang.bnNum(tDn))
            drawReportCard(cv, pt, pd, sY + cH + 60, cW, cH, Color.parseColor("#FF5252"), if (isBn) "কাজা হয়েছে" else "Missed", lang.bnNum(tM))
            drawReportCard(cv, pt, pd * 2 + cW, sY + cH + 60, cW, cH, Color.parseColor("#FF9500"), if (isBn) "অপেক্ষমান কাজা" else "Pending Qaza", lang.bnNum(tQ))
            drawReportCard(cv, pt, pd, sY + (cH * 2) + 120, cW, cH, Color.parseColor("#8B5CF6"), if (isBn) "পিরিয়ড/ছুটি" else "Excused Mode", lang.bnNum(tE))
            drawReportCard(cv, pt, pd * 2 + cW, sY + (cH * 2) + 120, cW, cH, Color.parseColor("#9B59B6"), if (isBn) "বর্তমান স্ট্রিক" else "Current Streak", lang.bnNum(ui.calculateStreak(sp, prayers)))

            val cyY = sY + (cH * 3) + 200
            val cyH = 480f
            pt.color = themeColors[1]
            cv.drawRoundRect(RectF(pd, cyY, w - pd, cyY + cyH), 50f, 50f, pt)

            val cIW = w - (pd * 2) - 80
            val cCol = cIW / dFV.size
            val mBH = cyH - 140
            for (i in dFV.indices) {
                val cx = pd + 40 + (i * cCol) + (cCol / 2f)
                val fH = (dFV[i] / 6f) * mBH
                val sH = (dSV[i] / 12f) * mBH
                val bW = if (isWeekly) 35f else 12f
                val gap = if (isWeekly) 5f else 2f

                if (fH > 0) {
                    pt.color = dC[i]
                    cv.drawRoundRect(RectF(cx - bW - gap, cyY + 60 + mBH - fH, cx - gap, cyY + 60 + mBH), bW / 2f, bW / 2f, pt)
                }
                if (sH > 0) {
                    pt.color = Color.parseColor("#F59E0B")
                    cv.drawRoundRect(RectF(cx + gap, cyY + 60 + mBH - sH, cx + gap + bW, cyY + 60 + mBH), bW / 2f, bW / 2f, pt)
                }
                pt.color = themeColors[3]
                pt.textSize = if (isWeekly) 35f else 24f
                pt.textAlign = Paint.Align.CENTER
                pt.typeface = appFonts[0]
                cv.drawText(dL[i], cx, cyY + cyH - 40, pt)
            }

            pt.color = themeColors[3]
            pt.textAlign = Paint.Align.CENTER
            pt.textSize = 45f
            cv.drawText(if (isBn) "My Salah Tracker অ্যাপের মাধ্যমে তৈরি" else "Generated by My Salah Tracker", w / 2f, h - 80f, pt)

            val dir = activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
            if (dir != null && !dir.exists()) dir.mkdirs()
            val file = File(dir, "Salah_Report_${System.currentTimeMillis()}.png")
            FileOutputStream(file).use { fos ->
                bm.compress(Bitmap.CompressFormat.PNG, 100, fos)
                fos.flush()
            }

            StrictMode.setVmPolicy(StrictMode.VmPolicy.Builder().build())
            val intent = Intent(Intent.ACTION_SEND).apply {
                type = "image/png"
                putExtra(Intent.EXTRA_STREAM, Uri.fromFile(file))
                putExtra(Intent.EXTRA_TEXT, "Alhamdulillah! Check out my Salah progress.")
            }
            activity.startActivity(Intent.createChooser(intent, "Share via"))
        } catch (_: Exception) {
            ui.showSmartBanner(
                activity.findViewById(android.R.id.content),
                lang.get("Share Failed"),
                lang.get("Storage permission required."),
                "img_warning",
                colorAccent,
                null
            )
        }
    }

    private fun drawReportCard(
        canvas: Canvas,
        paint: Paint,
        x: Float,
        y: Float,
        w: Float,
        h: Float,
        accentColor: Int,
        title: String,
        value: String
    ) {
        paint.color = themeColors[1]
        canvas.drawRoundRect(RectF(x, y, x + w, y + h), 50f, 50f, paint)
        paint.color = accentColor
        canvas.drawRoundRect(RectF(x, y, x + 40, y + h), 50f, 50f, paint)
        canvas.drawRect(x + 20, y, x + 40, y + h, paint)
        paint.color = themeColors[3]
        paint.textAlign = Paint.Align.LEFT
        paint.textSize = 50f
        paint.typeface = appFonts[0]
        canvas.drawText(title, x + 90, y + 110, paint)
        paint.color = accentColor
        paint.textSize = 110f
        paint.typeface = appFonts[1]
        canvas.drawText(value, x + 90, y + 230, paint)
    }

    fun syncDate(d: Date?) {
        if (d != null) statsCalPointer.time = d
    }

    fun exportPdf() {
        val isBn = sp.getString("app_lang", "en") == "bn"
        try {
            val pw = 650
            val ph = 2500
            val doc = PdfDocument()
            val pi = PdfDocument.PageInfo.Builder(pw, ph, 1).create()
            val pg = doc.startPage(pi)
            val cv = pg.canvas
            val pt = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                color = Color.WHITE
            }
            cv.drawRect(0f, 0f, pw.toFloat(), ph.toFloat(), pt)
            pt.color = colorAccent

            val hp = Path().apply {
                moveTo(0f, 0f)
                lineTo(pw.toFloat(), 0f)
                lineTo(pw.toFloat(), 180f)
                cubicTo(pw / 2f, 220f, 0f, 180f, 0f, 180f)
                close()
            }
            cv.drawPath(hp, pt)

            pt.color = Color.WHITE
            pt.textSize = 38f
            pt.typeface = Typeface.create(appFonts[1], Typeface.BOLD)
            pt.textAlign = Paint.Align.CENTER
            cv.drawText("My Salah Tracker", pw / 2f, 65f, pt)

            val em = sp.getString("user_email", "guest@salah.com") ?: "guest@salah.com"
            pt.textSize = 16f
            pt.typeface = appFonts[0]
            cv.drawText(em, pw / 2f, 95f, pt)

            var mNm = SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.time)
            if (isBn) {
                mNm = "${lang.get(SimpleDateFormat("MMMM", Locale.US).format(statsCalPointer.time))} ${lang.bnNum(statsCalPointer.get(Calendar.YEAR))}"
            }
            pt.textSize = 18f
            pt.alpha = 220
            cv.drawText("${if (isBn) "মাসিক রিপোর্ট • " else "Monthly Report • "}$mNm", pw / 2f, 135f, pt)
            pt.alpha = 255

            val cal = statsCalPointer.clone() as Calendar
            cal.set(Calendar.DAY_OF_MONTH, 1)
            val tD = cal.getActualMaximum(Calendar.DAY_OF_MONTH)
            var dP = 0
            var tDn = 0
            var tM = 0
            var tE = 0
            var tQ = 0
            val now = Calendar.getInstance()
            val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.US)

            for (i in 1..tD) {
                cal.set(Calendar.DAY_OF_MONTH, i)
                val dK = sdf.format(cal.time)
                if (cal.after(now) && dK != sdf.format(now.time)) continue
                dP++
                val r = getRoomRecord(dK)
                if (r != null) {
                    for (p in prayers) {
                        val st = r.getFardStat(p)
                        val isQ = r.getQazaStat(p)
                        when (st) {
                            "yes" -> tDn++
                            "excused" -> tE++
                            else -> {
                                if (isQ) tQ++ else tM++
                            }
                        }
                    }
                }
            }

            val sY = 200f
            val pd = 30f
            val cW = (pw - (pd * 4)) / 3f
            val cH = 75f

            drawPdfCardBig(cv, pt, pd, sY, cW, cH, colorAccent, if (isBn) "মোট দিন" else "Total Days", lang.bnNum(dP))
            drawPdfCardBig(cv, pt, pd * 2 + cW, sY, cW, cH, Color.parseColor("#3B82F6"), if (isBn) "আদায়কৃত" else "Prayers Done", lang.bnNum(tDn))
            drawPdfCardBig(cv, pt, pd * 3 + cW * 2, sY, cW, cH, Color.parseColor("#FF5252"), if (isBn) "কাজা হয়েছে" else "Missed", lang.bnNum(tM))
            drawPdfCardBig(cv, pt, pd, sY + cH + 20, cW, cH, Color.parseColor("#FF9500"), if (isBn) "অপেক্ষমান কাজা" else "Pending Qaza", lang.bnNum(tQ))
            drawPdfCardBig(cv, pt, pd * 2 + cW, sY + cH + 20, cW, cH, Color.parseColor("#FF4081"), if (isBn) "পিরিয়ড/ছুটি" else "Excused Mode", lang.bnNum(tE))
            drawPdfCardBig(cv, pt, pd * 3 + cW * 2, sY + cH + 20, cW, cH, Color.parseColor("#9B59B6"), if (isBn) "বর্তমান স্ট্রিক" else "Current Streak", lang.bnNum(ui.calculateStreak(sp, prayers)))

            val cSY = sY + (cH * 2) + 70
            pt.color = Color.parseColor("#333333")
            pt.textSize = 22f
            pt.typeface = Typeface.create(appFonts[1], Typeface.BOLD)
            pt.textAlign = Paint.Align.LEFT
            cv.drawText(if (isBn) "মাসিক ক্যালেন্ডার ওভারভিউ" else "Monthly Calendar Overview", pd, cSY, pt)

            val ds = if (isBn) arrayOf("রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি") else arrayOf("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
            val clW = 460f
            val clCol = clW / 7f
            val clX = (pw - clW) / 2f
            val rH = 50f
            pt.textSize = 14f
            pt.typeface = appFonts[0]
            pt.color = Color.parseColor("#888888")
            pt.textAlign = Paint.Align.CENTER
            for (i in 0 until 7) {
                cv.drawText(ds[i], clX + (i * clCol) + (clCol / 2f), cSY + 45, pt)
            }

            cal.set(Calendar.DAY_OF_MONTH, 1)
            val off = cal.get(Calendar.DAY_OF_WEEK) - 1
            val gY = cSY + 75
            for (i in 1..tD) {
                val r = (off + i - 1) / 7
                val c = (off + i - 1) % 7
                val cx = clX + (c * clCol) + (clCol / 2f)
                val cy = gY + (r * rH)
                cal.set(Calendar.DAY_OF_MONTH, i)
                val dK = sdf.format(cal.time)
                val rec = getRoomRecord(dK)
                var cArc = 0
                var hEx = false
                if (rec != null) {
                    for (p in prayers) {
                        val st = rec.getFardStat(p)
                        if (st == "yes") cArc++
                        else if (st == "excused") {
                            cArc++
                            hEx = true
                        }
                    }
                }
                pt.style = Paint.Style.STROKE
                pt.strokeWidth = 2f
                pt.color = Color.parseColor("#F1F5F9")
                cv.drawCircle(cx, cy, 18f, pt)
                if (cArc > 0 && !(cal.after(now) && dK != sdf.format(now.time))) {
                    pt.color = if (cArc == 6) Color.parseColor("#22C55E") else if (hEx) Color.parseColor("#8B5CF6") else Color.parseColor("#10B981")
                    cv.drawArc(RectF(cx - 18f, cy - 18f, cx + 18f, cy + 18f), -90f, 360f * (cArc / 6f), false, pt)
                }
                pt.style = Paint.Style.FILL
                pt.color = Color.parseColor("#333333")
                pt.textSize = 14f
                pt.typeface = Typeface.create(appFonts[1], Typeface.BOLD)
                cv.drawText(lang.bnNum(i), cx, cy + 5, pt)
            }

            val tR = Math.ceil((tD + off) / 7.0).toInt()
            val wSY = gY + (tR * rH) + 40
            pt.color = Color.parseColor("#333333")
            pt.textSize = 22f
            pt.typeface = Typeface.create(appFonts[1], Typeface.BOLD)
            pt.textAlign = Paint.Align.LEFT
            cv.drawText(if (isBn) "সাপ্তাহিক বিস্তারিত (ফজর থেকে বিতর)" else "Weekly Detail (Fard & Sunnah)", pd, wSY, pt)

            var wY = wSY + 30
            val wCH = 170f
            val bG = 20f

            for (w in 1..tR) {
                val sD = if (w == 1) 1 else (w - 1) * 7 - off + 1
                val eD = Math.min(w * 7 - off, tD)
                if (sD > tD) break

                val tmpS = statsCalPointer.clone() as Calendar
                tmpS.set(Calendar.DAY_OF_MONTH, sD)
                val tmpE = statsCalPointer.clone() as Calendar
                tmpE.set(Calendar.DAY_OF_MONTH, eD)

                val sm = SimpleDateFormat("MMM", Locale.US)
                val sDS = if (isBn) "${lang.bnNum(sD)} ${lang.get(sm.format(tmpS.time))}" else "${sm.format(tmpS.time)} ${String.format(Locale.US, "%02d", sD)}"
                val eDS = if (isBn) "${lang.bnNum(eD)} ${lang.get(sm.format(tmpE.time))}" else "${sm.format(tmpE.time)} ${String.format(Locale.US, "%02d", eD)}"
                val wT = "${if (isBn) "সপ্তাহ " else "Week "}${lang.bnNum(w)} ($sDS - $eDS)"

                pt.color = Color.parseColor("#FAFAFC")
                cv.drawRoundRect(RectF(pd, wY, pw - pd, wY + wCH), 15f, 15f, pt)
                pt.color = Color.parseColor("#555555")
                pt.textSize = 14f
                pt.typeface = Typeface.create(appFonts[1], Typeface.BOLD)
                pt.textAlign = Paint.Align.LEFT
                cv.drawText(wT, pd + 20, wY + 30, pt)

                val cAW = pw - (pd * 2) - 40
                val cCW = cAW / 7f
                val cXS = pd + 20
                for (d in sD..eD) {
                    cal.set(Calendar.DAY_OF_MONTH, d)
                    val dw = cal.get(Calendar.DAY_OF_WEEK) - 1
                    val dK = sdf.format(cal.time)
                    val cx = cXS + (dw * cCW) + (cCW / 2f)
                    var fD = 0
                    var sD_cnt = 0
                    var hB = false
                    if (cal.before(now) || dK == sdf.format(now.time)) {
                        val rec = getRoomRecord(dK)
                        if (rec != null) {
                            for (p in prayers) {
                                val fS = rec.getFardStat(p)
                                when (fS) {
                                    "yes" -> fD++
                                    "excused" -> {
                                        fD++
                                        hB = true
                                    }
                                }
                            }
                            sD_cnt += getTotalExtras(dK)
                        }
                    }
                    val mBH = 90f
                    val lH = (fD / 6f) * mBH
                    val rH_b = (sD_cnt / 12f) * mBH
                    val bY = wY + 135f
                    if (!(cal.after(now) && dK != sdf.format(now.time))) {
                        if (fD > 0) {
                            pt.color = if (hB) Color.parseColor("#8B5CF6") else Color.parseColor("#22C55E")
                            cv.drawRoundRect(RectF(cx - 10, bY - lH, cx - 1, bY), 4.5f, 4.5f, pt)
                        }
                        if (sD_cnt > 0) {
                            pt.color = Color.parseColor("#F59E0B")
                            cv.drawRoundRect(RectF(cx + 1, bY - rH_b, cx + 10, bY), 4.5f, 4.5f, pt)
                        }
                    }
                    pt.color = Color.parseColor("#AAAAAA")
                    pt.textSize = 10f
                    pt.typeface = appFonts[0]
                    pt.textAlign = Paint.Align.CENTER
                    cv.drawText("${ds[dw]} ${lang.bnNum(d)}", cx, bY + 18, pt)
                }
                wY += wCH + bG
            }

            pt.color = Color.parseColor("#AAAAAA")
            pt.textSize = 12f
            pt.typeface = appFonts[0]
            pt.textAlign = Paint.Align.CENTER
            cv.drawText(if (isBn) "My Salah Tracker অ্যাপের মাধ্যমে তৈরি" else "Generated by My Salah Tracker", pw / 2f, ph - 40f, pt)
            doc.finishPage(pg)

            val dir = activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
            if (dir != null && !dir.exists()) dir.mkdirs()
            val file = File(dir, "Salah_Report_${System.currentTimeMillis()}.pdf")
            doc.writeTo(FileOutputStream(file))
            doc.close()

            val r: FrameLayout? = activity.findViewById(android.R.id.content)
            if (r != null) {
                ui.showSmartBanner(
                    r,
                    if (isBn) "সফল" else "Success",
                    if (isBn) "পিডিএফ সেভ হয়েছে (দেখতে ক্লিক করুন)" else "PDF Saved (Click to view)",
                    "img_tick",
                    colorAccent
                ) {
                    val intent = Intent(Intent.ACTION_VIEW).apply {
                        val u = FileProvider.getUriForFile(activity, "${activity.packageName}.provider", file)
                        setDataAndType(u, "application/pdf")
                        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
                    }
                    try {
                        activity.startActivity(intent)
                    } catch (_: Exception) {}
                }
            }
        } catch (_: Exception) {
            val r: FrameLayout? = activity.findViewById(android.R.id.content)
            if (r != null) {
                ui.showSmartBanner(r, "Error", "Storage permission required.", "img_warning", colorAccent, null)
            }
        }
    }

    private fun drawPdfCardBig(
        canvas: Canvas,
        paint: Paint,
        x: Float,
        y: Float,
        w: Float,
        h: Float,
        accent: Int,
        title: String,
        valStr: String
    ) {
        paint.color = Color.parseColor("#F8F9F9")
        canvas.drawRoundRect(RectF(x, y, x + w, y + h), 14f, 14f, paint)
        paint.color = accent
        canvas.drawRoundRect(RectF(x, y, x + 8, y + h), 14f, 14f, paint)
        canvas.drawRect(x + 4, y, x + 8, y + h, paint)
        paint.color = Color.parseColor("#7F8C8D")
        paint.textSize = 14f
        paint.typeface = appFonts[0]
        paint.textAlign = Paint.Align.LEFT
        canvas.drawText(title, x + 22, y + 30, paint)
        paint.color = accent
        paint.textSize = 26f
        paint.typeface = appFonts[1]
        canvas.drawText(valStr, x + 22, y + 60, paint)
    }

    fun showStats(isWeekly: Boolean) {
        val wrap = LinearLayout(activity).apply {
            gravity = Gravity.CENTER
            val pad = (20 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
        }
        val card = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (25 * DENSITY).toInt()
            val padV = (30 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            gravity = Gravity.CENTER_HORIZONTAL
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 30f * DENSITY
            }
        }
        wrap.addView(card, LinearLayout.LayoutParams(-1, -2))

        val dialog = AlertDialog.Builder(activity).setView(wrap).create().apply {
            window?.setBackgroundDrawableResource(android.R.color.transparent)
            window?.setGravity(Gravity.CENTER)
        }
        renderStats(card, dialog, isWeekly)
        if (!activity.isFinishing) {
            dialog.show()
        }
    }

    private fun renderStats(card: LinearLayout, dialog: AlertDialog, isWeekly: Boolean) {
        card.removeAllViews()
        val isBn = sp.getString("app_lang", "en") == "bn"

        val nav = LinearLayout(activity).apply {
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, (25 * DENSITY).toInt())
        }
        val prev = TextView(activity).apply {
            text = "❮"
            textSize = 22f
            val padH = (15 * DENSITY).toInt()
            val padV = (10 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            setTextColor(colorAccent)
            ui.addClickFeedback(this)
            setOnClickListener {
                val check = statsCalPointer.clone() as Calendar
                if (isWeekly) check.add(Calendar.DATE, -7) else check.add(Calendar.MONTH, -1)
                if (check.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) {
                    if (isWeekly) statsCalPointer.add(Calendar.DATE, -7) else statsCalPointer.add(Calendar.MONTH, -1)
                    renderStats(card, dialog, isWeekly)
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

        val temp = statsCalPointer.clone() as Calendar
        val totalDays = if (isWeekly) 7 else temp.getActualMaximum(Calendar.DAY_OF_MONTH)
        if (isWeekly) {
            while (temp.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) temp.add(Calendar.DATE, -1)
        } else {
            temp.set(Calendar.DAY_OF_MONTH, 1)
        }
        val startCal = temp.clone() as Calendar
        val endCal = startCal.clone() as Calendar
        endCal.add(Calendar.DATE, totalDays - 1)

        val title = TextView(activity).apply {
            val mF = SimpleDateFormat("MMMM", Locale.US)
            text = if (isWeekly) {
                "📊 ${lang.getShortGreg(startCal.time)} - ${lang.getShortGreg(endCal.time)}"
            } else {
                "📊 ${lang.get(mF.format(statsCalPointer.time))} ${lang.bnNum(statsCalPointer.get(Calendar.YEAR))}"
            }
            setTextColor(themeColors[2])
            textSize = 16f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
        }

        val next = TextView(activity).apply {
            text = "❯"
            textSize = 22f
            val padH = (15 * DENSITY).toInt()
            val padV = (10 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            val now = Calendar.getInstance()
            val isFuture = if (isWeekly) {
                startCal.after(now)
            } else {
                (statsCalPointer.get(Calendar.YEAR) > now.get(Calendar.YEAR)) ||
                    (statsCalPointer.get(Calendar.YEAR) == now.get(Calendar.YEAR) && statsCalPointer.get(Calendar.MONTH) >= now.get(Calendar.MONTH))
            }
            setTextColor(if (isFuture) themeColors[4] else colorAccent)
            ui.addClickFeedback(this)
            setOnClickListener {
                if (!isFuture) {
                    if (isWeekly) statsCalPointer.add(Calendar.DATE, 7) else statsCalPointer.add(Calendar.MONTH, 1)
                    renderStats(card, dialog, isWeekly)
                } else {
                    ui.showPremiumLocked(colorAccent)
                }
            }
        }
        nav.addView(prev)
        nav.addView(title)
        nav.addView(next)
        card.addView(nav)

        val fE = ArrayList<BarEntry>()
        val sE = ArrayList<BarEntry>()
        val fC = ArrayList<Int>()
        val lbls = arrayOfNulls<String>(totalDays)
        val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.US)
        var tDone = 0
        var tExc = 0
        var tSun = 0
        var daysPassed = 0
        val now = Calendar.getInstance()

        for (i in 0 until totalDays) {
            val dK = sdf.format(startCal.time)
            var d = 0
            var e = 0
            var s = 0
            val sR = getRoomRecord(dK)
            if (startCal.before(now) || dK == sdf.format(now.time)) {
                daysPassed++
                if (sR != null) {
                    for (j in 0 until 6) {
                        val st = sR.getFardStat(prayers[j])
                        if (st == "yes") d++ else if (st == "excused") e++
                    }
                    if (isWeekly) s += getTotalExtras(dK)
                }
                tDone += d
                tExc += e
                tSun += s
            }
            val fVal = (d + e).toFloat()
            val sunnahNorm = Math.min(6f, s * (6f / 10f))
            fE.add(BarEntry(if (sunnahNorm == 0f) i.toFloat() else i - 0.2f, fVal))
            sE.add(BarEntry(i + 0.2f, sunnahNorm))

            val statusCol = (activity as MainActivity).getStatusColor(dK)
            fC.add(if (fVal == 0f) Color.TRANSPARENT else statusCol)

            lbls[i] = if (isWeekly) {
                if (isBn) {
                    arrayOf("র", "সো", "ম", "বু", "বৃ", "শু", "শ")[startCal.get(Calendar.DAY_OF_WEEK) - 1]
                } else {
                    SimpleDateFormat("E", Locale.US).format(startCal.time).substring(0, 1)
                }
            } else {
                if (isBn) lang.bnNum(i + 1) else "${i + 1}"
            }
            startCal.add(Calendar.DATE, 1)
        }

        val bc = BarChart(activity).apply {
            layoutParams = LinearLayout.LayoutParams(-1, (180 * DENSITY).toInt())
        }
        val fs = BarDataSet(fE, "Fard").apply {
            colors = fC
            setDrawValues(false)
        }
        val ss = BarDataSet(sE, "Sunnah").apply {
            color = Color.parseColor("#F59E0B")
            setDrawValues(false)
        }
        val bd = BarData(fs, ss).apply {
            barWidth = 0.3f
        }
        bc.xAxis.axisMinimum = -0.5f
        bc.xAxis.axisMaximum = totalDays - 0.5f
        bc.data = bd

        bc.renderer = object : BarChartRenderer(bc, bc.animator, bc.viewPortHandler) {
            override fun drawDataSet(c: Canvas, dataSet: IBarDataSet, index: Int) {
                for (j in 0 until dataSet.entryCount) {
                    val e = dataSet.getEntryForIndex(j)
                    if (e.y <= 0f) continue
                    val pos = floatArrayOf(e.x - 0.15f, e.y, e.x + 0.15f, 0f)
                    mChart.getTransformer(dataSet.axisDependency).pointValuesToPixel(pos)
                    mRenderPaint.color = dataSet.getColor(j)
                    c.drawRoundRect(RectF(pos[0], pos[1], pos[2], pos[3]), 8f * DENSITY, 8f * DENSITY, mRenderPaint)
                }
            }
        }
        bc.axisLeft.apply {
            axisMinimum = 0f
            axisMaximum = 6.2f
            granularity = 1f
        }
        bc.xAxis.apply {
            position = XAxis.XAxisPosition.BOTTOM
            setDrawGridLines(false)
            textColor = themeColors[3]
            valueFormatter = object : ValueFormatter() {
                override fun getFormattedValue(v: Float): String {
                    val idx = Math.round(v)
                    return if (idx in lbls.indices) lbls[idx] ?: "" else ""
                }
            }
        }
        bc.legend.isEnabled = false
        bc.description.isEnabled = false
        bc.axisRight.isEnabled = false

        val sCalClick = temp.clone() as Calendar
        if (isWeekly) {
            while (sCalClick.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) sCalClick.add(Calendar.DATE, -1)
        } else {
            sCalClick.set(Calendar.DAY_OF_MONTH, 1)
        }

        bc.setOnChartValueSelectedListener(object : OnChartValueSelectedListener {
            override fun onValueSelected(e: Entry, h: Highlight) {
                val idx = Math.round(e.x)
                val tCal = sCalClick.clone() as Calendar
                tCal.add(Calendar.DATE, idx)
                val n = Calendar.getInstance()
                if (tCal.after(n) && sdf.format(tCal.time) != sdf.format(n.time)) {
                    ui.showPremiumLocked(colorAccent)
                } else if (tCal.get(Calendar.YEAR) < n.get(Calendar.YEAR) - 100) {
                    val r: FrameLayout? = activity.findViewById(android.R.id.content)
                    if (r != null) {
                        ui.showSmartBanner(r, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null)
                    }
                } else {
                    Handler(Looper.getMainLooper()).postDelayed({
                        dialog.dismiss()
                        if (activity is MainActivity) {
                            activity.selectedDate[0] = sdf.format(tCal.time)
                            activity.loadTodayPage()
                        }
                    }, 150)
                }
            }

            override fun onNothingSelected() {}
        })
        card.addView(bc)

        // Legend Row
        val legBox = LinearLayout(activity).apply {
            gravity = Gravity.CENTER
            setPadding(0, (15 * DENSITY).toInt(), 0, (5 * DENSITY).toInt())
        }
        val lN = if (isBn) arrayOf("ফরজ", "সুন্নাহ", "ছুটি") else arrayOf("Fard", "Sunnah", "Excused")
        val lC = intArrayOf(Color.parseColor("#22C55E"), Color.parseColor("#F59E0B"), Color.parseColor("#8B5CF6"))
        for (i in lN.indices) {
            val item = LinearLayout(activity).apply {
                gravity = Gravity.CENTER
                val pad = (10 * DENSITY).toInt()
                setPadding(pad, 0, pad, 0)
            }
            val dot = View(activity).apply {
                layoutParams = LinearLayout.LayoutParams((12 * DENSITY).toInt(), (12 * DENSITY).toInt())
                background = GradientDrawable().apply {
                    setColor(lC[i])
                    cornerRadius = 6f * DENSITY
                }
            }
            val txt = TextView(activity).apply {
                text = lN[i]
                setTextColor(themeColors[3])
                textSize = 12f
                setPadding((5 * DENSITY).toInt(), 0, 0, 0)
            }
            item.addView(dot)
            item.addView(txt)
            legBox.addView(item)
        }
        card.addView(legBox)

        var tMiss = (daysPassed * 6) - tDone - tExc
        if (tMiss < 0) tMiss = 0

        val dRow = LinearLayout(activity).apply {
            setPadding(0, (25 * DENSITY).toInt(), 0, (10 * DENSITY).toInt())
        }

        val b1 = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
        }
        val t1 = TextView(activity).apply {
            text = lang.bnNum(tDone)
            textSize = 24f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.parseColor("#22C55E"))
        }
        val l1 = TextView(activity).apply {
            text = if (isBn) "ফরজ" else "Fard"
            textSize = 11f
            setTextColor(themeColors[3])
        }
        b1.addView(t1)
        b1.addView(l1)
        dRow.addView(b1)

        val b3 = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
        }
        val t3 = TextView(activity).apply {
            text = lang.bnNum(tSun)
            textSize = 24f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.parseColor("#F59E0B"))
            gravity = Gravity.CENTER
        }
        val l3 = TextView(activity).apply {
            text = if (isBn) "সুন্নাহ" else "Sunnah"
            textSize = 11f
            setTextColor(themeColors[3])
            gravity = Gravity.CENTER
        }
        b3.addView(t3)
        b3.addView(l3)
        dRow.addView(b3)

        val b2 = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.END
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
        }
        val t2 = TextView(activity).apply {
            text = lang.bnNum(tMiss)
            textSize = 24f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.parseColor("#FF5252"))
            gravity = Gravity.END
        }
        val l2 = TextView(activity).apply {
            text = lang.get("Missed")
            textSize = 11f
            setTextColor(themeColors[3])
            gravity = Gravity.END
        }
        b2.addView(t2)
        b2.addView(l2)
        dRow.addView(b2)
        card.addView(dRow)

        val close = TextView(activity).apply {
            text = lang.get("CLOSE")
            setTextColor(themeColors[3])
            val padH = (15 * DENSITY).toInt()
            setPadding(padH, padH, padH, (5 * DENSITY).toInt())
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            ui.addClickFeedback(this)
            setOnClickListener { dialog.dismiss() }
        }
        card.addView(close)
        card.applyFont(appFonts[0], appFonts[1])
    }
}
