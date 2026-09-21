package com.my.salah.tracker.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.graphics.Typeface
import android.icu.util.IslamicCalendar
import android.os.Build
import android.widget.RemoteViews
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class SalahWidget : AppWidgetProvider() {

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

                val record = dao.getRecordByDate(todayKey) ?: SalahRecord(todayKey).also {
                    dao.insertRecord(it)
                }

                val current = record.getFardStat(prayerName)
                val newStat = if (current == "no") "yes" else "no"
                record.setFardStat(prayerName, newStat)

                if (newStat == "yes") {
                    record.setQazaStat(prayerName, false)
                    context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
                        .edit()
                        .putBoolean("${todayKey}_${prayerName}_qaza", false)
                        .apply()
                }

                dao.updateRecord(record)

                val appWidgetManager = AppWidgetManager.getInstance(context)
                onUpdate(
                    context,
                    appWidgetManager,
                    appWidgetManager.getAppWidgetIds(ComponentName(context, SalahWidget::class.java))
                )
            }
        }
    }

    companion object {
        private const val ACTION_TOGGLE = "com.my.salah.tracker.app.TOGGLE_PRAYER"
        private const val EXTRA_PRAYER_NAME = "prayer_name"

        @JvmStatic
        fun buildTextBitmap(ctx: Context, text: String, color: Int, sizeSp: Float, tf: Typeface): Bitmap {
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                textSize = sizeSp * ctx.resources.displayMetrics.scaledDensity
                this.color = color
                typeface = tf
                textAlign = Paint.Align.LEFT
            }
            val fm = paint.fontMetrics
            val w = Math.max(1f, paint.measureText(text))
            val h = fm.descent - fm.ascent
            val bmp = Bitmap.createBitmap((w + 4).toInt(), (h + 4).toInt(), Bitmap.Config.ARGB_8888)
            val canvas = Canvas(bmp)
            canvas.drawText(text, 2f, -fm.ascent + 2f, paint)
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

        @JvmStatic
        fun updateAppWidget(context: Context, appWidgetManager: AppWidgetManager, appWidgetId: Int) {
            val sp = context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
            val lang = LanguageEngine(sp.getString("app_lang", "en") ?: "en")
            val views = RemoteViews(
                context.packageName,
                context.resources.getIdentifier("salah_widget", "layout", context.packageName)
            )

            val systemDark = (context.resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES
            val isDarkTheme = sp.getBoolean("is_dark_mode", systemDark)
            val isBn = sp.getString("app_lang", "en") == "bn"

            val mainBgColor = if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#FFFFFF")
            val cardEmptyBorderColor = if (isDarkTheme) Color.parseColor("#38383A") else Color.parseColor("#E2E8F0")
            val mainTextColor = if (isDarkTheme) Color.WHITE else Color.parseColor("#141416")
            val subTextColor = if (isDarkTheme) Color.parseColor("#A0A0A5") else Color.parseColor("#64748B")
            val progressBgColor = if (isDarkTheme) Color.parseColor("#2C2C2E") else Color.parseColor("#E2E8F0")

            val activeTheme = sp.getInt("app_theme", 0).coerceIn(0, 5)
            val themeAccents = arrayOf("#00BFA5", "#3B82F6", "#FF9559", "#D81B60", "#A67BFF", "#3BCC75")
            val colorAccent = Color.parseColor(themeAccents[activeTheme])

            views.setInt(
                context.resources.getIdentifier("widget_outer_border", "id", context.packageName),
                "setColorFilter", colorAccent
            )
            views.setInt(
                context.resources.getIdentifier("widget_inner_bg", "id", context.packageName),
                "setColorFilter", mainBgColor
            )

            val appFontBold = try {
                if (isBn) {
                    Typeface.createFromAsset(context.assets, "fonts/hind_bold.ttf")
                } else {
                    Typeface.createFromAsset(context.assets, "fonts/poppins_bold.ttf")
                }
            } catch (_: Exception) {
                Typeface.SANS_SERIF
            }

            val todayKey = SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date())

            var hijriText = ""
            try {
                if (Build.VERSION.SDK_INT >= 24) {
                    val hijriCal = IslamicCalendar().apply {
                        add(IslamicCalendar.DATE, sp.getInt("hijri_offset", 0))
                    }
                    val hMonths = arrayOf(
                        "Muharram", "Safar", "Rabi I", "Rabi II", "Jumada I",
                        "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal",
                        "Dhu al-Qi'dah", "Dhu al-Hijjah"
                    )
                    val hD = hijriCal.get(IslamicCalendar.DAY_OF_MONTH)
                    hijriText = "${lang.bnNum(hD)}${if (isBn) getBnSuffix(hD) else ""} ${lang.get(hMonths[hijriCal.get(IslamicCalendar.MONTH)])} ${lang.bnNum(hijriCal.get(IslamicCalendar.YEAR))} ${lang.get("AH")}"
                } else {
                    hijriText = "${lang.bnNum(16)}${if (isBn) "ই " else " "}${lang.get("Ramadan")} ${lang.bnNum(1447)} ${lang.get("AH")}"
                }
            } catch (_: Exception) {}

            val gregText: String
            val c = Calendar.getInstance()
            if (isBn) {
                val bnDays = arrayOf("রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার")
                val bnMonths = arrayOf(
                    "জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন",
                    "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"
                )
                val gD = c.get(Calendar.DAY_OF_MONTH)
                gregText = "${bnDays[c.get(Calendar.DAY_OF_WEEK) - 1]}, ${lang.bnNum(gD)}${getBnSuffix(gD)} ${bnMonths[c.get(Calendar.MONTH)]} ${lang.bnNum(c.get(Calendar.YEAR))}"
            } else {
                gregText = SimpleDateFormat("EEEE, MMM dd, yyyy", Locale.US).format(Date())
            }

            views.setImageViewBitmap(
                context.resources.getIdentifier("widget_hijri_date_img", "id", context.packageName),
                buildTextBitmap(context, hijriText, subTextColor, 13f, appFontBold)
            )
            views.setInt(
                context.resources.getIdentifier("widget_hijri_icon", "id", context.packageName),
                "setColorFilter", subTextColor
            )
            views.setImageViewBitmap(
                context.resources.getIdentifier("widget_greg_date_img", "id", context.packageName),
                buildTextBitmap(context, gregText, mainTextColor, 18f, appFontBold)
            )

            views.setInt(
                context.resources.getIdentifier("widget_percent_border", "id", context.packageName),
                "setColorFilter", colorAccent
            )
            views.setInt(
                context.resources.getIdentifier("widget_percent_inner", "id", context.packageName),
                "setColorFilter", mainBgColor
            )

            val dao = SalahDatabase.getDatabase(context).salahDao()
            val todayRecord = dao.getRecordByDate(todayKey)

            var countCompleted = 0
            val pNames = AppConstants.PRAYERS
            val pImgs = arrayOf("img_fajr", "img_dhuhr", "img_asr", "img_maghrib", "img_isha", "img_witr")
            val boxIds = arrayOf("box_fajr", "box_dhuhr", "box_asr", "box_maghrib", "box_isha", "box_witr")

            for (i in 0 until 6) {
                val stat = todayRecord?.getFardStat(pNames[i]) ?: "no"
                val isDone = stat == "yes" || stat == "excused"
                if (isDone) countCompleted++

                val boxId = context.resources.getIdentifier(boxIds[i], "id", context.packageName)
                val iconId = context.resources.getIdentifier("w_icon", "id", context.packageName)
                val textId = context.resources.getIdentifier("w_name_img", "id", context.packageName)
                val borderId = context.resources.getIdentifier("card_border", "id", context.packageName)
                val innerId = context.resources.getIdentifier("card_inner", "id", context.packageName)

                val prayerBox = RemoteViews(
                    context.packageName,
                    context.resources.getIdentifier("widget_prayer_item", "layout", context.packageName)
                )

                prayerBox.setImageViewBitmap(
                    textId,
                    buildTextBitmap(context, lang.get(pNames[i]), mainTextColor, 14f, appFontBold)
                )
                prayerBox.setInt(innerId, "setColorFilter", mainBgColor)
                prayerBox.setInt(borderId, "setColorFilter", if (isDone) colorAccent else cardEmptyBorderColor)

                prayerBox.setImageViewResource(
                    iconId,
                    context.resources.getIdentifier(pImgs[i], "drawable", context.packageName)
                )
                prayerBox.setInt(iconId, "setColorFilter", if (isDone) colorAccent else subTextColor)

                val toggleIntent = Intent(context, SalahWidget::class.java).apply {
                    action = ACTION_TOGGLE
                    putExtra(EXTRA_PRAYER_NAME, pNames[i])
                }
                val pendingFlags = PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= 23) PendingIntent.FLAG_IMMUTABLE else 0)
                val pendingIntent = PendingIntent.getBroadcast(context, i, toggleIntent, pendingFlags)

                prayerBox.setOnClickPendingIntent(
                    context.resources.getIdentifier("content_box", "id", context.packageName),
                    pendingIntent
                )
                views.removeAllViews(boxId)
                views.addView(boxId, prayerBox)
                views.setOnClickPendingIntent(boxId, pendingIntent)
            }

            val percent = Math.min(100, ((countCompleted / 6f) * 100).toInt())
            views.setImageViewBitmap(
                context.resources.getIdentifier("widget_percent_badge_img", "id", context.packageName),
                buildTextBitmap(context, "${lang.bnNum(percent)}%", mainTextColor, 14f, appFontBold)
            )

            try {
                val progressBmp = Bitmap.createBitmap(1000, 30, Bitmap.Config.ARGB_8888)
                val canvas = Canvas(progressBmp)
                val p = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                    color = progressBgColor
                }
                canvas.drawRoundRect(RectF(0f, 0f, 1000f, 30f), 15f, 15f, p)
                if (countCompleted > 0) {
                    p.color = colorAccent
                    canvas.drawRoundRect(RectF(0f, 0f, (countCompleted / 6f) * 1000f, 30f), 15f, 15f, p)
                }
                views.setImageViewBitmap(
                    context.resources.getIdentifier("widget_progress_img", "id", context.packageName),
                    progressBmp
                )
            } catch (_: Exception) {}

            val appIntent = Intent(context, MainActivity::class.java)
            val pendingAppFlags = PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= 23) PendingIntent.FLAG_IMMUTABLE else 0)
            val appPendingIntent = PendingIntent.getActivity(context, 0, appIntent, pendingAppFlags)
            views.setOnClickPendingIntent(
                context.resources.getIdentifier("widget_content", "id", context.packageName),
                appPendingIntent
            )

            appWidgetManager.updateAppWidget(appWidgetId, views)
        }
    }
}
