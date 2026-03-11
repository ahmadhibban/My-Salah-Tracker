import os

kotlin_code = """package com.my.salah.tracker.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.graphics.Typeface
import android.os.Build
import android.widget.RemoteViews
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class SalahWidget : AppWidgetProvider() {

    companion object {
        private const val ACTION_TOGGLE = "com.my.salah.tracker.app.TOGGLE_PRAYER"
        private const val EXTRA_PRAYER_NAME = "prayer_name"

        @JvmStatic
        fun buildTextBitmap(ctx: Context, text: String, color: Int, sizeSp: Float, tf: Typeface?): Bitmap {
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                textSize = sizeSp * ctx.resources.displayMetrics.scaledDensity
                this.color = color
                typeface = tf
                textAlign = Paint.Align.LEFT
            }
            val fm = paint.fontMetrics
            var w = paint.measureText(text)
            val h = fm.descent - fm.ascent
            if (w <= 0) w = 1f
            val bmp = Bitmap.createBitmap((w + 4).toInt(), (h + 4).toInt(), Bitmap.Config.ARGB_8888)
            val canvas = Canvas(bmp)
            canvas.drawText(text, 2f, -fm.ascent + 2, paint)
            return bmp
        }

        @JvmStatic
        fun getBnSuffix(d: Int): String {
            return when (d) {
                1 -> "লা"
                2, 3 -> "রা"
                4 -> "ঠা"
                in 5..18 -> "ই"
                in 19..31 -> "এ"
                else -> "শে"
            }
        }
    }

    private fun toggleStatInRoom(record: SalahRecord, prayerName: String) {
        when (prayerName) {
            "Fajr" -> record.fajr = if (record.fajr == "no") "yes" else "no"
            "Dhuhr" -> record.dhuhr = if (record.dhuhr == "no") "yes" else "no"
            "Asr" -> record.asr = if (record.asr == "no") "yes" else "no"
            "Maghrib" -> record.maghrib = if (record.maghrib == "no") "yes" else "no"
            "Isha" -> record.isha = if (record.isha == "no") "yes" else "no"
            "Witr" -> record.witr = if (record.witr == "no") "yes" else "no"
        }
    }

    private fun getStatFromRoom(record: SalahRecord?, prayerName: String): String {
        if (record == null) return "no"
        return when (prayerName) {
            "Fajr" -> record.fajr
            "Dhuhr" -> record.dhuhr
            "Asr" -> record.asr
            "Maghrib" -> record.maghrib
            "Isha" -> record.isha
            "Witr" -> record.witr
            else -> "no"
        }
    }

    override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {
        for (appWidgetId in appWidgetIds) {
            updateAppWidget(context, appWidgetManager, appWidgetId)
        }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        if (ACTION_TOGGLE == intent.action) {
            val prayerName = intent.getStringExtra(EXTRA_PRAYER_NAME)
            if (prayerName != null) {
                val todayKey = SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date())
                val dao = SalahDatabase.getDatabase(context).salahDao()
                var record = dao.getRecordByDate(todayKey)
                
                if (record == null) {
                    record = SalahRecord(todayKey)
                    dao.insertRecord(record)
                }

                toggleStatInRoom(record, prayerName)

                if (getStatFromRoom(record, prayerName) == "yes") {
                    when (prayerName) {
                        "Fajr" -> record.fajr_qaza = false
                        "Dhuhr" -> record.dhuhr_qaza = false
                        "Asr" -> record.asr_qaza = false
                        "Maghrib" -> record.maghrib_qaza = false
                        "Isha" -> record.isha_qaza = false
                        "Witr" -> record.witr_qaza = false
                    }
                    context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
                        .edit()
                        .putBoolean("${todayKey}_${prayerName}_qaza", false)
                        .apply()
                }

                dao.updateRecord(record)
                val appWidgetManager = AppWidgetManager.getInstance(context)
                onUpdate(context, appWidgetManager, appWidgetManager.getAppWidgetIds(ComponentName(context, SalahWidget::class.java)))
            }
        }
    }

    private fun updateAppWidget(context: Context, appWidgetManager: AppWidgetManager, appWidgetId: Int) {
        val sp = context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
        val lang = LanguageEngine(sp.getString("app_lang", "en") ?: "en")
        val views = RemoteViews(context.packageName, context.resources.getIdentifier("salah_widget", "layout", context.packageName))

        val systemDark = (context.resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES
        val isDarkTheme = sp.getBoolean("is_dark_mode", systemDark)
        val isBn = sp.getString("app_lang", "en") == "bn"

        val mainBgColor = if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#FFFFFF")
        val cardEmptyBorderColor = if (isDarkTheme) Color.parseColor("#38383A") else Color.parseColor("#E2E8F0")
        val mainTextColor = if (isDarkTheme) Color.WHITE else Color.parseColor("#141416")
        val subTextColor = if (isDarkTheme) Color.parseColor("#A0A0A5") else Color.parseColor("#64748B")
        val progressBgColor = if (isDarkTheme) Color.parseColor("#2C2C2E") else Color.parseColor("#E2E8F0")

        val activeTheme = sp.getInt("app_theme", 0)
        val themeAccents = arrayOf("#00BFA5", "#3B82F6", "#FF9559", "#D81B60", "#A67BFF", "#3BCC75")
        val colorAccent = Color.parseColor(themeAccents[activeTheme])

        views.setInt(context.resources.getIdentifier("widget_outer_border", "id", context.packageName), "setColorFilter", colorAccent)
        views.setInt(context.resources.getIdentifier("widget_inner_bg", "id", context.packageName), "setColorFilter", mainBgColor)

        var appFontBold: Typeface = Typeface.SANS_SERIF
        try {
            appFontBold = if (isBn) Typeface.createFromAsset(context.assets, "fonts/hind_bold.ttf")
            else Typeface.createFromAsset(context.assets, "fonts/poppins_bold.ttf")
        } catch (e: Exception) { }

        val sdfKey = SimpleDateFormat("yyyy-MM-dd", Locale.US)
        val todayKey = sdfKey.format(Date())
        var hijriText = ""

        try {
            if (Build.VERSION.SDK_INT >= 24) {
                val hijriCal = android.icu.util.IslamicCalendar()
                hijriCal.add(android.icu.util.IslamicCalendar.DATE, sp.getInt("hijri_offset", 0))
                val hMonths = arrayOf("Muharram", "Safar", "Rabi I", "Rabi II", "Jumada I", "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah")
                val hD = hijriCal.get(android.icu.util.IslamicCalendar.DAY_OF_MONTH)
                hijriText = "${lang.bnNum(hD)}${if (isBn) getBnSuffix(hD) else ""} ${lang.get(hMonths[hijriCal.get(android.icu.util.IslamicCalendar.MONTH)])} ${lang.bnNum(hijriCal.get(android.icu.util.IslamicCalendar.YEAR))} ${lang.get("AH")}"
            } else {
                hijriText = "${lang.bnNum(16)}${if (isBn) "ই " else " "}${lang.get("Ramadan")} ${lang.bnNum(1447)} ${lang.get("AH")}"
            }
        } catch (e: Exception) { }

        val c = Calendar.getInstance()
        val gregText: String = if (isBn) {
            val bnDays = arrayOf("রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার")
            val bnMonths = arrayOf("জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর")
            val gD = c.get(Calendar.DAY_OF_MONTH)
            "${bnDays[c.get(Calendar.DAY_OF_WEEK) - 1]}, ${lang.bnNum(gD)}${getBnSuffix(gD)} ${bnMonths[c.get(Calendar.MONTH)]} ${lang.bnNum(c.get(Calendar.YEAR))}"
        } else {
            SimpleDateFormat("EEEE, MMM dd, yyyy", Locale.US).format(Date())
        }

        views.setImageViewBitmap(context.resources.getIdentifier("widget_hijri_date_img", "id", context.packageName), buildTextBitmap(context, hijriText, subTextColor, 13f, appFontBold))
        views.setInt(context.resources.getIdentifier("widget_hijri_icon", "id", context.packageName), "setColorFilter", subTextColor)
        views.setImageViewBitmap(context.resources.getIdentifier("widget_greg_date_img", "id", context.packageName), buildTextBitmap(context, gregText, mainTextColor, 18f, appFontBold))
        views.setInt(context.resources.getIdentifier("widget_percent_border", "id", context.packageName), "setColorFilter", colorAccent)
        views.setInt(context.resources.getIdentifier("widget_percent_inner", "id", context.packageName), "setColorFilter", mainBgColor)

        val dao = SalahDatabase.getDatabase(context).salahDao()
        val todayRecord = dao.getRecordByDate(todayKey)
        var countCompleted = 0

        val pNames = AppConstants.PRAYERS
        val pImgs = arrayOf("img_fajr", "img_dhuhr", "img_asr", "img_maghrib", "img_isha", "img_witr")
        val boxIds = arrayOf("box_fajr", "box_dhuhr", "box_asr", "box_maghrib", "box_isha", "box_witr")

        for (i in 0 until 6) {
            val stat = getStatFromRoom(todayRecord, pNames[i])
            val isDone = stat == "yes" || stat == "excused"
            if (isDone) countCompleted++

            val boxId = context.resources.getIdentifier(boxIds[i], "id", context.packageName)
            val iconId = context.resources.getIdentifier("w_icon", "id", context.packageName)
            val textId = context.resources.getIdentifier("w_name_img", "id", context.packageName)
            val borderId = context.resources.getIdentifier("card_border", "id", context.packageName)
            val innerId = context.resources.getIdentifier("card_inner", "id", context.packageName)

            val prayerBox = RemoteViews(context.packageName, context.resources.getIdentifier("widget_prayer_item", "layout", context.packageName))
            prayerBox.setImageViewBitmap(textId, buildTextBitmap(context, lang.get(pNames[i]), mainTextColor, 14f, appFontBold))
            prayerBox.setInt(innerId, "setColorFilter", mainBgColor)

            if (isDone) prayerBox.setInt(borderId, "setColorFilter", colorAccent)
            else prayerBox.setInt(borderId, "setColorFilter", cardEmptyBorderColor)

            prayerBox.setImageViewResource(iconId, context.resources.getIdentifier(pImgs[i], "drawable", context.packageName))
            
            if (isDone) prayerBox.setInt(iconId, "setColorFilter", colorAccent)
            else prayerBox.setInt(iconId, "setColorFilter", subTextColor)

            val toggleIntent = Intent(context, SalahWidget::class.java).apply {
                action = ACTION_TOGGLE
                putExtra(EXTRA_PRAYER_NAME, pNames[i])
            }

            val pendingIntent = PendingIntent.getBroadcast(
                context, i, toggleIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= 23) PendingIntent.FLAG_IMMUTABLE else 0)
            )

            prayerBox.setOnClickPendingIntent(context.resources.getIdentifier("content_box", "id", context.packageName), pendingIntent)
            views.removeAllViews(boxId)
            views.addView(boxId, prayerBox)
            views.setOnClickPendingIntent(boxId, pendingIntent)
        }

        val percent = Math.min(100, ((countCompleted / 6f) * 100).toInt())
        views.setImageViewBitmap(context.resources.getIdentifier("widget_percent_badge_img", "id", context.packageName), buildTextBitmap(context, "${lang.bnNum(percent)}%", mainTextColor, 14f, appFontBold))

        try {
            val progressBmp = Bitmap.createBitmap(1000, 30, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(progressBmp)
            val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = progressBgColor }
            canvas.drawRoundRect(RectF(0f, 0f, 1000f, 30f), 15f, 15f, p)
            
            if (countCompleted > 0) {
                p.color = colorAccent
                canvas.drawRoundRect(RectF(0f, 0f, (countCompleted / 6f) * 1000f, 30f), 15f, 15f, p)
            }
            views.setImageViewBitmap(context.resources.getIdentifier("widget_progress_img", "id", context.packageName), progressBmp)
        } catch (e: Exception) { }

        val appIntent = Intent(context, MainActivity::class.java)
        val appPendingIntent = PendingIntent.getActivity(
            context, 0, appIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= 23) PendingIntent.FLAG_IMMUTABLE else 0)
        )
        views.setOnClickPendingIntent(context.resources.getIdentifier("widget_content", "id", context.packageName), appPendingIntent)

        appWidgetManager.updateAppWidget(appWidgetId, views)
    }
}
"""

found = False
for root_dir, dirs, files in os.walk('.'):
    if 'SalahWidget.kt' in files:
        file_path = os.path.join(root_dir, 'SalahWidget.kt')
        with open(file_path, 'w') as f:
            f.write(kotlin_code)
        print(f"✅ Successfully wrote Kotlin code to {file_path}")
        found = True

if not found:
    print("❌ SalahWidget.kt not found! Please check file tree.")
