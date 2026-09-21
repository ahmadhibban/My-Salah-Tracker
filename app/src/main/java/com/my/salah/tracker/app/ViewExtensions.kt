package com.my.salah.tracker.app

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.ColorStateList
import android.content.res.Resources
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.animation.OvershootInterpolator
import android.widget.Button
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.TextView
import soup.neumorphism.NeumorphCardView
import soup.neumorphism.NeumorphShapeAppearanceModel
import soup.neumorphism.NeumorphShapeDrawable
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Common extension helpers to keep code clean, concise, high performance, and easy to maintain.
 */
val Number.dp: Int
    get() = (this.toFloat() * Resources.getSystem().displayMetrics.density + 0.5f).toInt()

fun Context.dp(value: Number): Int =
    (value.toFloat() * resources.displayMetrics.density + 0.5f).toInt()

fun View.dp(value: Number): Int =
    (value.toFloat() * resources.displayMetrics.density + 0.5f).toInt()

fun createDrawable(
    color: Int,
    radius: Float = 0f,
    strokeWidth: Int = 0,
    strokeColor: Int = 0,
    shape: Int = GradientDrawable.RECTANGLE
): GradientDrawable = GradientDrawable().apply {
    this.shape = shape
    setColor(color)
    if (radius > 0f) cornerRadius = radius
    if (strokeWidth > 0 && strokeColor != 0) setStroke(strokeWidth, strokeColor)
}

fun View.applyFont(reg: Typeface?, bold: Typeface?) {
    if (reg == null || bold == null) return
    if (this is TextView) {
        val isBold = typeface != null && typeface.isBold
        typeface = if (isBold) bold else reg
    } else if (this is ViewGroup) {
        for (i in 0 until childCount) {
            getChildAt(i).applyFont(reg, bold)
        }
    }
}

/**
 * Fast single-pass converter from ASCII digits to Bengali digits.
 */
fun String.toBnDigits(): String {
    val sb = StringBuilder(length)
    for (i in 0 until length) {
        val c = this[i]
        if (c in '0'..'9') {
            sb.append(('০'.code + (c - '0')).toChar())
        } else {
            sb.append(c)
        }
    }
    return sb.toString()
}

fun Int.toBnDigits(): String = this.toString().toBnDigits()
fun Long.toBnDigits(): String = this.toString().toBnDigits()

fun View.bounceClick(scaleDown: Float = 0.95f, duration: Long = 35L, action: (() -> Unit)? = null) {
    animate()
        .scaleX(scaleDown)
        .scaleY(scaleDown)
        .alpha(0.8f)
        .setDuration(duration)
        .withEndAction {
            animate()
                .scaleX(1f)
                .scaleY(1f)
                .alpha(1f)
                .setDuration(120)
                .setInterpolator(OvershootInterpolator())
                .withEndAction { action?.invoke() }
                .start()
        }
        .start()
}

/**
 * Reusable Neumorphic Card Builder to eliminate repetitive 20-line boilerplate.
 */
fun Context.createNeoCard(
    shapeType: Int = 0,
    radiusDp: Float = 16f,
    elevationDp: Float = 3f,
    isDark: Boolean,
    bgColor: Int? = null
): NeumorphCardView {
    val density = resources.displayMetrics.density
    return NeumorphCardView(this).apply {
        setShapeType(shapeType)
        setShadowColorLight(if (isDark) Color.parseColor("#333336") else Color.parseColor("#F1F5F9"))
        setShadowColorDark(if (isDark) Color.parseColor("#0A0A0C") else Color.parseColor("#cbd5e0"))
        setShadowElevation(elevationDp * density)
        setShapeAppearanceModel(
            NeumorphShapeAppearanceModel.Builder()
                .setAllCorners(0, radiusDp * density)
                .build()
        )
        setBackgroundColor(bgColor ?: (if (isDark) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0")))
    }
}

/**
 * Container returned by createCustomDialog.
 */
class CustomDialogContainer(
    val dialog: AlertDialog,
    val contentLayout: LinearLayout
)

/**
 * Reusable Modern Dialog Wrapper replacing ~30 lines of boilerplate per dialog.
 */
fun Activity.createCustomDialog(
    bgColor: Int,
    radiusDp: Float = 25f,
    widthDp: Int = 320,
    padHDp: Int = 25,
    padVDp: Int = 30
): CustomDialogContainer {
    val d = resources.displayMetrics.density
    val wrap = FrameLayout(this).apply {
        layoutParams = FrameLayout.LayoutParams(-1, -1)
    }
    val content = LinearLayout(this).apply {
        orientation = LinearLayout.VERTICAL
        val pH = (padHDp * d).toInt()
        val pV = (padVDp * d).toInt()
        setPadding(pH, pV, pH, pV)
        background = createDrawable(bgColor, radiusDp * d)
    }
    val flp = FrameLayout.LayoutParams((widthDp * d).toInt(), -2).apply {
        gravity = Gravity.CENTER
    }
    wrap.addView(content, flp)

    val ad = AlertDialog.Builder(this).setView(wrap).create()
    ad.window?.setBackgroundDrawableResource(android.R.color.transparent)
    ad.window?.setGravity(Gravity.CENTER)
    return CustomDialogContainer(ad, content)
}

/**
 * Fast cached DateFormatter singleton to eliminate garbage collection & parsing overhead.
 */
object AppDateUtils {
    val ymdFormat = SimpleDateFormat("yyyy-MM-dd", Locale.US)
    val monthFormatEn = SimpleDateFormat("MMMM", Locale.US)

    @Synchronized
    fun formatYmd(date: Date): String = ymdFormat.format(date)

    @Synchronized
    fun parseYmd(str: String): Date? = try {
        ymdFormat.parse(str)
    } catch (e: Exception) {
        null
    }
}
