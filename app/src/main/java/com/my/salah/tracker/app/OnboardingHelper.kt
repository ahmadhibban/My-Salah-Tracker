package com.my.salah.tracker.app

import android.app.Activity
import android.content.SharedPreferences
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.view.Gravity
import android.widget.Button
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.TextView

class OnboardingHelper(
    private val activity: Activity,
    private val DENSITY: Float,
    private val themeColors: IntArray,
    private val colorAccent: Int,
    private val lang: LanguageEngine,
    private val ui: UIComponents,
    private val sp: SharedPreferences,
    private val root: FrameLayout,
    private val appFonts: Array<Typeface?>
) {
    private var currentPage = 0

    fun showOnboarding() {
        val overlay = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
            setBackgroundColor(themeColors[0])
            isClickable = true
        }

        val main = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            val pad = (30 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
        }

        val iconContainer = FrameLayout(activity).apply {
            layoutParams = LinearLayout.LayoutParams((120 * DENSITY).toInt(), (120 * DENSITY).toInt()).apply {
                setMargins(0, 0, 0, (30 * DENSITY).toInt())
            }
        }

        val title = TextView(activity).apply {
            setTextColor(themeColors[2])
            textSize = 24f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, (15 * DENSITY).toInt())
        }

        val desc = TextView(activity).apply {
            setTextColor(themeColors[3])
            textSize = 14f
            gravity = Gravity.CENTER
            setLineSpacing(0f, 1.3f)
            setPadding(0, 0, 0, (40 * DENSITY).toInt())
        }

        val nextBtn = Button(activity).apply {
            text = if (sp.getString("app_lang", "en") == "bn") "পরবর্তী" else "Next"
            setTextColor(Color.WHITE)
            isAllCaps = false
            textSize = 16f
            typeface = Typeface.DEFAULT_BOLD
            background = GradientDrawable().apply {
                setColor(colorAccent)
                cornerRadius = 25f * DENSITY
            }
            layoutParams = LinearLayout.LayoutParams(-1, (55 * DENSITY).toInt()).apply {
                setMargins(0, (20 * DENSITY).toInt(), 0, 0)
            }
        }

        main.addView(iconContainer)
        main.addView(title)
        main.addView(desc)
        main.addView(nextBtn)
        overlay.addView(main)
        root.addView(overlay)

        val skipBtn = TextView(activity).apply {
            text = lang.get("Skip")
            setTextColor(themeColors[3])
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            val pad = (20 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
            layoutParams = FrameLayout.LayoutParams(-2, -2).apply {
                gravity = Gravity.TOP or Gravity.END
                setMargins(0, (30 * DENSITY).toInt(), 0, 0)
            }
        }
        overlay.addView(skipBtn)

        val dismissOverlay = {
            sp.edit().putBoolean("is_first_run_tutorial", false).apply()
            overlay.animate()
                .alpha(0f)
                .setDuration(300)
                .withEndAction {
                    if (overlay.parent != null) root.removeView(overlay)
                }
                .start()
        }

        skipBtn.setOnClickListener { dismissOverlay() }

        val isBn = sp.getString("app_lang", "en") == "bn"
        val pages = arrayOf(
            arrayOf("img_moon", if (isBn) "স্বাগতম" else "Welcome", if (isBn) "আপনার ব্যক্তিগত বিজ্ঞাপন-মুক্ত সালাহ ট্র্যাকার।" else "Your personal ad-free Salah companion."),
            arrayOf("img_calender", if (isBn) "সহজ ট্র্যাকিং" else "Easy Tracking", if (isBn) "প্রতিদিনের নামাজ ও কাজা নামাজের হিসাব রাখুন সহজে।" else "Track daily prayers and Qaza with ease."),
            arrayOf("img_cloud", if (isBn) "ক্লাউড ব্যাকআপ" else "Cloud Sync", if (isBn) "আপনার ডাটা কখনোই হারাবে না, গুগল ক্লাউডে সেভ থাকবে।" else "Never lose data; sync securely with Google Cloud."),
            arrayOf("img_stats", if (isBn) "বিস্তারিত রিপোর্ট" else "Advanced Stats", if (isBn) "সাপ্তাহিক ও মাসিক প্রগতি দেখুন আকর্ষণীয় চার্টে।" else "Analyze your progress with weekly & monthly charts."),
            arrayOf("img_settings", if (isBn) "কাস্টমাইজেশন" else "Customization", if (isBn) "ডার্ক মোড, একাধিক থিম এবং বাংলা ভাষা ব্যবহারের সুবিধা।" else "Dark mode, multiple themes, and Bengali support.")
        )

        fun updatePage() {
            iconContainer.removeAllViews()
            val icon = ui.getRoundImage(pages[currentPage][0], 0, Color.TRANSPARENT, colorAccent)
            iconContainer.addView(icon)
            title.text = pages[currentPage][1]
            desc.text = pages[currentPage][2]
            if (currentPage == pages.size - 1) {
                nextBtn.text = if (isBn) "শুরু করুন" else "Get Started"
            }
        }

        updatePage()

        nextBtn.setOnClickListener {
            if (currentPage < pages.size - 1) {
                currentPage++
                updatePage()
            } else {
                dismissOverlay()
            }
        }

        main.applyFont(appFonts[0], appFonts[1])
    }
}
