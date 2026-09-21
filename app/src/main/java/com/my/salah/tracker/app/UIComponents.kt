package com.my.salah.tracker.app

import android.animation.ObjectAnimator
import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.SharedPreferences
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.ColorFilter
import android.graphics.Paint
import android.graphics.PorterDuff
import android.graphics.Rect
import android.graphics.RectF
import android.graphics.Typeface
import android.graphics.drawable.Drawable
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.ShapeDrawable
import android.graphics.drawable.shapes.OvalShape
import android.icu.util.IslamicCalendar
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.animation.AnticipateInterpolator
import android.view.animation.OvershootInterpolator
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class UIComponents(
    private val activity: Activity,
    private val DENSITY: Float,
    private val themeColors: IntArray,
    private val lang: LanguageEngine
) {
    private var activeBanner: LinearLayout? = null

    class ProgressDrawable(
        private val d: Int,
        private val t: Int,
        private val c: Int,
        private val bg: Int,
        private val dens: Float
    ) : Drawable() {
        override fun draw(canvas: Canvas) {
            val b = bounds
            val p = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                style = Paint.Style.STROKE
                strokeWidth = 2.5f * dens
                strokeCap = Paint.Cap.ROUND
            }
            val r = Math.min(b.width(), b.height()) / 2f - (2.5f * dens)
            p.color = bg
            canvas.drawCircle(b.exactCenterX(), b.exactCenterY(), r, p)
            if (d > 0) {
                p.color = c
                canvas.drawArc(
                    RectF(
                        b.exactCenterX() - r, b.exactCenterY() - r,
                        b.exactCenterX() + r, b.exactCenterY() + r
                    ),
                    -90f, 360f * (d / t.toFloat()), false, p
                )
            }
        }

        override fun setAlpha(a: Int) {}
        override fun setColorFilter(f: ColorFilter?) {}
        @Deprecated("Deprecated in Java", ReplaceWith("android.graphics.PixelFormat.TRANSLUCENT"))
        override fun getOpacity(): Int = android.graphics.PixelFormat.TRANSLUCENT
    }

    fun getPremiumIcon(emoji: String, colorStart: Int, colorEnd: Int, sizeDp: Int): View {
        return TextView(activity).apply {
            text = emoji
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            textSize = sizeDp / 2.5f
            gravity = Gravity.CENTER
            background = GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                intArrayOf(colorStart, colorEnd)
            ).apply { shape = GradientDrawable.OVAL }
            layoutParams = LinearLayout.LayoutParams((sizeDp * DENSITY).toInt(), (sizeDp * DENSITY).toInt())
        }
    }

    fun getRoundImage(resName: String, paddingDp: Int, bgHex: Int, tintHex: Int): View {
        val wrap = FrameLayout(activity).apply {
            background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(bgHex)
            }
        }
        val iv = ImageView(activity).apply {
            val resId = activity.resources.getIdentifier(resName, "drawable", activity.packageName)
            if (resId != 0) setImageResource(resId)
            scaleType = ImageView.ScaleType.FIT_CENTER
            if (tintHex != 0) setColorFilter(tintHex, PorterDuff.Mode.SRC_IN)
            val pad = (paddingDp * DENSITY).toInt()
            layoutParams = FrameLayout.LayoutParams(-1, -1).apply {
                setMargins(pad, pad, pad, pad)
            }
        }
        wrap.addView(iv)
        return wrap
    }

    fun getHijriDate(date: Date, offsetDays: Int): String {
        return try {
            if (Build.VERSION.SDK_INT >= 24) {
                val hijriCal = IslamicCalendar().apply {
                    time = date
                    add(IslamicCalendar.DATE, offsetDays)
                }
                val hMonths = arrayOf(
                    "Muharram", "Safar", "Rabi I", "Rabi II", "Jumada I",
                    "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal",
                    "Dhu al-Qi'dah", "Dhu al-Hijjah"
                )
                val hd = hijriCal.get(IslamicCalendar.DAY_OF_MONTH)
                val day = lang.bnNum(hd) + lang.getBnSuffix(hd)
                val month = lang.get(hMonths[hijriCal.get(IslamicCalendar.MONTH)])
                val year = lang.bnNum(hijriCal.get(IslamicCalendar.YEAR))
                val ah = lang.get("AH")
                "$day $month $year $ah"
            } else {
                ""
            }
        } catch (_: Exception) {
            "Error Date"
        }
    }

    fun getPremiumCheckbox(status: String, activeColorHex: Int): View {
        val tv = TextView(activity).apply {
            gravity = Gravity.CENTER
            textSize = 14f
            layoutParams = LinearLayout.LayoutParams((26 * DENSITY).toInt(), (26 * DENSITY).toInt())
        }
        val gd = GradientDrawable().apply { shape = GradientDrawable.OVAL }
        when (status) {
            "yes" -> {
                gd.setColor(activeColorHex)
                tv.text = "✓"
                tv.setTextColor(Color.WHITE)
            }
            "excused" -> {
                gd.setColor(activeColorHex)
                tv.text = "🌸"
                gd.cornerRadius = 100f
                tv.setTextColor(Color.WHITE)
            }
            else -> {
                gd.setColor(Color.TRANSPARENT)
                gd.setStroke((2 * DENSITY).toInt(), themeColors[4])
                tv.text = ""
            }
        }
        tv.background = gd
        return tv
    }

    fun calculateStreak(prefs: SharedPreferences, prayerArray: Array<String>): Int {
        val format = SimpleDateFormat("yyyy-MM-dd", Locale.US)
        val c = Calendar.getInstance()
        var streak = 0
        for (i in 0 until 3650) {
            val dKey = format.format(c.time)
            var done = true
            for (p in prayerArray) {
                val stat = prefs.getString("${dKey}_$p", "no") ?: "no"
                if (stat != "yes" && stat != "excused") {
                    done = false
                    break
                }
            }
            if (done) {
                streak++
                c.add(Calendar.DATE, -1)
            } else {
                break
            }
        }
        return streak
    }

    fun getRainbowBorder(dateKey: String, strokeWidthDp: Int): Drawable {
        return object : ShapeDrawable(OvalShape()) {
            override fun draw(canvas: Canvas) {
                val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                    style = Paint.Style.FILL
                    color = themeColors[1]
                }
                canvas.drawOval(
                    RectF(0f, 0f, bounds.width().toFloat(), bounds.height().toFloat()),
                    paint
                )
            }
        }
    }

    fun showSmartBanner(
        root: FrameLayout,
        titleStr: String,
        msg: String,
        imgName: String,
        colorAccent: Int,
        onClick: Runnable?
    ) {
        activity.runOnUiThread {
            activeBanner?.let {
                if (it.parent != null) root.removeView(it)
                activeBanner = null
            }
            val banner = LinearLayout(activity).apply {
                orientation = LinearLayout.VERTICAL
                background = GradientDrawable().apply {
                    setColor(themeColors[1])
                    cornerRadius = 25f * DENSITY
                    setStroke((1.5f * DENSITY).toInt(), colorAccent)
                }
                if (Build.VERSION.SDK_INT >= 21) elevation = 40f
            }
            activeBanner = banner

            val topRow = LinearLayout(activity).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                setPadding(
                    (20 * DENSITY).toInt(), (15 * DENSITY).toInt(),
                    (20 * DENSITY).toInt(), (15 * DENSITY).toInt()
                )
            }

            val icon = getRoundImage(imgName, 2, Color.TRANSPARENT, colorAccent).apply {
                layoutParams = LinearLayout.LayoutParams((26 * DENSITY).toInt(), (26 * DENSITY).toInt()).apply {
                    setMargins(0, 0, (12 * DENSITY).toInt(), 0)
                }
            }

            val textCol = LinearLayout(activity).apply {
                orientation = LinearLayout.VERTICAL
            }
            val titleTv = TextView(activity).apply {
                text = lang.get(titleStr)
                setTextColor(themeColors[2])
                textSize = 14f
                typeface = Typeface.DEFAULT_BOLD
            }
            val subTv = TextView(activity).apply {
                text = lang.get(msg)
                setTextColor(themeColors[3])
                textSize = 11f
            }
            textCol.addView(titleTv)
            textCol.addView(subTv)

            topRow.addView(icon)
            topRow.addView(textCol)
            banner.addView(topRow)

            if (onClick != null) {
                banner.setOnClickListener {
                    onClick.run()
                    hideLoadingBanner(root)
                }
            }

            val lp = FrameLayout.LayoutParams(-1, -2).apply {
                gravity = Gravity.TOP
                setMargins((20 * DENSITY).toInt(), (50 * DENSITY).toInt(), (20 * DENSITY).toInt(), 0)
            }
            root.addView(banner, lp)

            banner.translationY = -250f * DENSITY
            banner.alpha = 0f
            banner.animate()
                .translationY(0f)
                .alpha(1f)
                .setDuration(500)
                .setInterpolator(OvershootInterpolator())
                .start()

            if (onClick == null) {
                Handler(Looper.getMainLooper()).postDelayed({
                    hideLoadingBanner(root)
                }, 2500)
            }
        }
    }

    fun addClickFeedback(v: View) {
        v.setOnTouchListener { view, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    view.animate().scaleX(0.92f).scaleY(0.92f).alpha(0.7f).setDuration(100).start()
                }
                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    view.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(100).start()
                }
            }
            false
        }
    }

    fun hideLoadingBanner(root: FrameLayout) {
        activity.runOnUiThread {
            activeBanner?.let { banner ->
                banner.animate()
                    .translationY(-250f * DENSITY)
                    .alpha(0f)
                    .setDuration(400)
                    .setInterpolator(AnticipateInterpolator())
                    .withEndAction {
                        if (banner.parent != null) root.removeView(banner)
                        if (activeBanner === banner) activeBanner = null
                    }
                    .start()
            }
        }
    }

    fun showPremiumLocked(colorAccent: Int) {
        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val main = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(
                (25 * DENSITY).toInt(), (35 * DENSITY).toInt(),
                (25 * DENSITY).toInt(), (35 * DENSITY).toInt()
            )
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 30f * DENSITY
            }
        }

        val iconView = TextView(activity).apply {
            text = "⏳"
            textSize = 50f
            gravity = Gravity.CENTER
        }
        main.addView(iconView)
        ObjectAnimator.ofFloat(iconView, "rotation", 0f, 15f, -15f, 15f, -15f, 0f).apply {
            duration = 500
            start()
        }

        var tfReg = Typeface.DEFAULT
        var tfBold = Typeface.DEFAULT_BOLD
        try {
            val uiSp = activity.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
            if (uiSp.getString("app_lang", "en") == "bn") {
                tfReg = Typeface.createFromAsset(activity.assets, "fonts/hind_reg.ttf")
                tfBold = Typeface.createFromAsset(activity.assets, "fonts/hind_bold.ttf")
            } else {
                tfReg = Typeface.createFromAsset(activity.assets, "fonts/poppins_reg.ttf")
                tfBold = Typeface.createFromAsset(activity.assets, "fonts/poppins_bold.ttf")
            }
        } catch (_: Exception) {}

        val title = TextView(activity).apply {
            text = lang.get("Patience is Virtue")
            setTextColor(themeColors[2])
            textSize = 20f
            typeface = tfBold
            gravity = Gravity.CENTER
            setPadding(0, (15 * DENSITY).toInt(), 0, (5 * DENSITY).toInt())
        }
        main.addView(title)

        val sub = TextView(activity).apply {
            text = lang.get("You cannot mark future prayers.")
            setTextColor(themeColors[3])
            textSize = 14f
            gravity = Gravity.CENTER
            typeface = tfReg
        }
        main.addView(sub)

        val flp = FrameLayout.LayoutParams((280 * DENSITY).toInt(), -2).apply {
            gravity = Gravity.CENTER
        }
        wrap.addView(main, flp)

        val ad = AlertDialog.Builder(activity).setView(wrap).create()
        ad.window?.setBackgroundDrawableResource(android.R.color.transparent)
        ad.window?.setGravity(Gravity.CENTER)
        if (!activity.isFinishing) {
            ad.show()
        }
    }
}
