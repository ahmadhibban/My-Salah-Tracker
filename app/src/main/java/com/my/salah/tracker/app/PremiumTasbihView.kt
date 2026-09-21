package com.my.salah.tracker.app

import android.content.Context
import android.content.SharedPreferences
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.LinearGradient
import android.graphics.Paint
import android.graphics.Path
import android.graphics.Shader
import android.graphics.Typeface
import android.graphics.drawable.Drawable
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.LayerDrawable
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.util.TypedValue
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.animation.OvershootInterpolator
import android.widget.LinearLayout
import android.widget.TextView

class PremiumTasbihView(
    ctx: Context,
    isDark: Boolean,
    private val accentColor: Int
) : LinearLayout(ctx) {

    private var count = 0
    private val display: TextView
    private val tapButton: View
    private val prefs: SharedPreferences = ctx.getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE)

    init {
        orientation = VERTICAL
        gravity = Gravity.CENTER
        setWillNotDraw(false)

        // Top padding 45 as designed
        setPadding(60, 45, 20, 20)

        count = prefs.getInt("pt_count", 0)

        // 1. Sleek Engraved Display
        display = TextView(ctx).apply {
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.BOLD)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 20f)
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.argb(35, 0, 0, 0))
                cornerRadius = 15f
                setStroke(2, Color.argb(40, 255, 255, 255))
            }
            setPadding(30, 8, 30, 8)
            gravity = Gravity.CENTER
        }
        updateDisplay()
        addView(display)

        // Spacer
        val sp = View(ctx).apply {
            layoutParams = LayoutParams(1, (12 * ctx.resources.displayMetrics.density).toInt())
        }
        addView(sp)

        // 2. Ultra Premium Jewel Button
        val den = ctx.resources.displayMetrics.density
        val unpressed = createPremiumButton(false)
        val pressed = createPremiumButton(true)

        tapButton = View(ctx).apply {
            layoutParams = LayoutParams((55 * den).toInt(), (55 * den).toInt())
            background = unpressed
            isClickable = true
            isFocusable = true

            setOnTouchListener { _, e ->
                when (e.action) {
                    MotionEvent.ACTION_DOWN -> {
                        background = pressed
                        scaleX = 0.92f
                        scaleY = 0.92f
                    }
                    MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                        background = unpressed
                        animate()
                            .scaleX(1f)
                            .scaleY(1f)
                            .setDuration(100)
                            .setInterpolator(OvershootInterpolator())
                            .start()
                    }
                }
                false
            }

            setOnClickListener {
                count++
                if (count > 99999) count = 0
                updateDisplay()
                vibrate(ctx, 20)
                prefs.edit().putInt("pt_count", count).apply()
            }

            setOnLongClickListener {
                count = 0
                updateDisplay()
                vibrate(ctx, 80)
                prefs.edit().putInt("pt_count", count).apply()
                true
            }
        }
        addView(tapButton)
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            style = Paint.Style.STROKE
            strokeWidth = 4f
            shader = LinearGradient(
                0f, 0f, 0f, height.toFloat(),
                intArrayOf(Color.TRANSPARENT, Color.argb(120, 255, 255, 255), Color.TRANSPARENT),
                null,
                Shader.TileMode.CLAMP
            )
        }
        val path = Path().apply {
            moveTo(15f, 30f)
            quadTo(45f, height / 2f, 15f, height - 30f)
        }
        canvas.drawPath(path, p)
    }

    private fun createPremiumButton(isPressed: Boolean): LayerDrawable {
        val light = Color.argb(
            255,
            Math.min(255, (Color.red(accentColor) * 1.2).toInt()),
            Math.min(255, (Color.green(accentColor) * 1.2).toInt()),
            Math.min(255, (Color.blue(accentColor) * 1.2).toInt())
        )
        val dark = Color.argb(
            255,
            (Color.red(accentColor) * 0.7).toInt(),
            (Color.green(accentColor) * 0.7).toInt(),
            (Color.blue(accentColor) * 0.7).toInt()
        )
        val shadow = GradientDrawable().apply {
            shape = GradientDrawable.OVAL
            setColor(Color.argb(80, 0, 0, 0))
        }
        val face = GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            if (isPressed) intArrayOf(dark, light) else intArrayOf(light, dark)
        ).apply {
            shape = GradientDrawable.OVAL
            setStroke(2, Color.argb(60, 255, 255, 255))
        }

        val ld = LayerDrawable(arrayOf<Drawable>(shadow, face))
        if (isPressed) {
            ld.setLayerInset(0, 2, 2, 0, 0)
            ld.setLayerInset(1, 4, 4, 2, 2)
        } else {
            ld.setLayerInset(0, 0, 0, 6, 6)
            ld.setLayerInset(1, 0, 0, 6, 6)
        }
        return ld
    }

    private fun updateDisplay() {
        var numStr = String.format("%04d", count)
        try {
            val sp = context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
            if (sp.getString("app_lang", "en") == "bn") {
                numStr = numStr.toBnDigits()
            }
        } catch (_: Exception) {}
        display.text = numStr
    }

    private fun vibrate(c: Context, ms: Long) {
        try {
            val v = c.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                v?.vibrate(VibrationEffect.createOneShot(ms, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                v?.vibrate(ms)
            }
        } catch (_: Exception) {}
    }
}
