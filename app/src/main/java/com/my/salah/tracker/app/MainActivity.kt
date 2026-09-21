package com.my.salah.tracker.app

import android.app.Activity
import android.app.AlertDialog
import android.appwidget.AppWidgetManager
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.ActivityInfo
import android.content.res.ColorStateList
import android.content.res.Configuration
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.Typeface
import android.graphics.drawable.Drawable
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.LayerDrawable
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.Html
import android.util.Log
import android.view.Gravity
import android.view.HapticFeedbackConstants
import android.view.View
import android.view.ViewGroup
import android.view.Window
import android.view.WindowManager
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import soup.neumorphism.NeumorphCardView
import soup.neumorphism.NeumorphShapeAppearanceModel
import soup.neumorphism.NeumorphShapeDrawable
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale
import java.util.Stack

class MainActivity : Activity() {

    companion object {
        @JvmStatic
        fun getBnDateStr(dateStr: String, sp: SharedPreferences): String {
            return BengaliCalendarHelper.getBnDateStr(dateStr, sp)
        }
    }

    class WaterWaveView(context: Context) : View(context) {
        private val path = Path()
        private val paint = Paint().apply {
            style = Paint.Style.FILL
            isAntiAlias = true
        }
        private var phase = 0f
        private var progress = 0

        fun setProgressAndColor(p: Int, c: Int) {
            this.progress = p
            paint.color = c
            invalidate()
        }

        override fun onDraw(canvas: Canvas) {
            super.onDraw(canvas)
            val w = width
            val h = height
            if (w == 0 || h == 0) return

            path.reset()
            val baseHeight = h - (h * progress / 100f)
            val amplitude = h * 0.05f
            path.moveTo(0f, h.toFloat())
            path.lineTo(0f, baseHeight)

            var i = 0
            while (i <= w) {
                val y = (Math.sin((i * 3 * Math.PI / w) + phase) * amplitude).toFloat() + baseHeight
                path.lineTo(i.toFloat(), y)
                i += 10
            }
            path.lineTo(w.toFloat(), h.toFloat())
            path.close()
            canvas.drawPath(path, paint)

            phase += 0.15f
            postInvalidateDelayed(20)
        }
    }

    private lateinit var sp: SharedPreferences
    private var DENSITY: Float = 0f
    private var isDarkTheme: Boolean = false
    private var activeTheme: Int = 0
    val themeColors = IntArray(6)
    var colorAccent: Int = 0
    val selectedDate = Array(1) { "" }
    private var calendarViewPointer: Calendar = Calendar.getInstance()

    private lateinit var lang: LanguageEngine
    private lateinit var ui: UIComponents
    private lateinit var fbHelper: FirebaseManager
    private lateinit var statsHelper: StatsHelper
    private lateinit var backupHelper: BackupHelper
    private lateinit var calHelper: CalendarHelper
    val appFonts = arrayOfNulls<Typeface>(2)

    private lateinit var root: FrameLayout
    private lateinit var contentArea: LinearLayout
    private val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.US)

    private fun applyNeo(v: View, type: Int, radius: Float, elev: Float, bgColor: Int, isDark: Boolean) {
        var finalBgColor = bgColor
        var finalElev = elev
        val model = NeumorphShapeAppearanceModel.Builder()
            .setAllCorners(0, radius * DENSITY)
            .build()
        val d = NeumorphShapeDrawable(v.context).apply {
            setShapeAppearanceModel(model)
            setShapeType(type)
        }

        if (type == 1 && !isDark && finalBgColor != colorAccent) {
            finalBgColor = Color.parseColor("#E2E8F0")
            d.setShadowColorDark(Color.parseColor("#A0AEC0"))
            d.setShadowColorLight(Color.parseColor("#FFFFFF"))
            finalElev *= 1.5f
        }

        d.setShadowColorLight(if (isDark) Color.parseColor("#333336") else Color.parseColor("#F1F5F9"))
        d.setShadowColorDark(if (isDark) Color.parseColor("#0A0A0C") else Color.parseColor("#cbd5e0"))
        d.setShadowElevation(finalElev * DENSITY)
        d.setFillColor(ColorStateList.valueOf(finalBgColor))
        v.background = d

        v.post {
            val p1 = v.parent
            if (p1 is ViewGroup) {
                p1.clipChildren = false
                p1.clipToPadding = false
                val p2 = p1.parent
                if (p2 is ViewGroup) {
                    p2.clipChildren = false
                    p2.clipToPadding = false
                }
            }
        }
    }

    private fun getNeoCheckbox(status: String, accentColor: Int): View {
        val isChk = status == "yes" || status == "excused"
        val nd = NeumorphCardView(this).apply {
            val size = (52 * DENSITY).toInt()
            layoutParams = LinearLayout.LayoutParams(size, size)
            setShapeType(if (isChk) 0 else 1)
            setShadowColorLight(if (isDarkTheme) Color.parseColor("#333336") else Color.parseColor("#F1F5F9"))
            setShadowColorDark(if (isDarkTheme) Color.parseColor("#0A0A0C") else Color.parseColor("#cbd5e0"))
            setShadowElevation((if (isChk) 2f else 5.5f) * DENSITY)
            setShapeAppearanceModel(
                NeumorphShapeAppearanceModel.Builder()
                    .setAllCorners(0, 26f * DENSITY)
                    .build()
            )
            setBackgroundColor(if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"))
            val pad = (14 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
        }

        if (isChk) {
            val inner = TextView(this).apply {
                text = if (status == "yes") "✓" else "🌸"
                setTextColor(accentColor)
                textSize = 18f
                setTypeface(null, Typeface.BOLD)
                gravity = Gravity.CENTER
                layoutParams = FrameLayout.LayoutParams(-1, -1)
            }
            nd.addView(inner)
        }
        return nd
    }

    fun getUltra3D(surfaceColor: Int, shadowColor: Int, radius: Float, depthDp: Float): Drawable {
        val d = resources.displayMetrics.density
        val shadow = GradientDrawable().apply {
            setColor(shadowColor)
            cornerRadius = radius
        }
        val surface = GradientDrawable().apply {
            setColor(surfaceColor)
            cornerRadius = radius
            setStroke((1.0f * d).toInt(), shadowColor)
        }
        val ld = LayerDrawable(arrayOf(shadow, surface))
        val offX = ((depthDp / 2.0f) * d).toInt()
        val offY = (depthDp * d).toInt()
        ld.setLayerInset(0, offX, offY, 0, 0)
        ld.setLayerInset(1, 0, 0, offX, offY)
        return ld
    }

    fun getPremium3D(c1: Int, r: Float, dp: Float, isDark: Boolean, accent: Int): Drawable {
        val d = resources.displayMetrics.density
        val red = Color.red(accent)
        val grn = Color.green(accent)
        val blu = Color.blue(accent)
        val shadow = if (isDark) {
            Color.rgb((red * 0.4f).toInt(), (grn * 0.4f).toInt(), (blu * 0.4f).toInt())
        } else {
            Color.argb(80, red, grn, blu)
        }

        val sh = GradientDrawable().apply {
            setColor(shadow)
            cornerRadius = r
        }
        val su = GradientDrawable().apply {
            setColor(c1)
            cornerRadius = r
            setStroke((1.5f * d).toInt(), shadow)
        }

        val ld = LayerDrawable(arrayOf(sh, su))
        val ox = ((dp / 1.5f) * d).toInt()
        val oy = (dp * d).toInt()
        ld.setLayerInset(0, ox, oy, 0, 0)
        ld.setLayerInset(1, 0, 0, ox, oy)
        return ld
    }

    fun getSafe3D(c1: Int, c2: Int, r: Float, dp: Float): Drawable {
        val d = resources.displayMetrics.density
        val sh = GradientDrawable().apply {
            setColor(c2)
            cornerRadius = r
        }
        val su = GradientDrawable().apply {
            setColor(c1)
            cornerRadius = r
        }
        val ld = LayerDrawable(arrayOf(sh, su))
        val o = (dp * d).toInt()
        ld.setLayerInset(0, 0, o, 0, 0)
        ld.setLayerInset(1, 0, 0, 0, o)
        return ld
    }

    private fun getRoomRecord(date: String): SalahRecord {
        val dao = SalahDatabase.getInstance(this).salahDao()
        var r = dao.getRecordByDate(date)
        if (r == null) {
            r = SalahRecord(date)
            dao.insertRecord(r)
        }
        return r
    }

    private fun updateRoomRecord(r: SalahRecord) {
        SalahDatabase.getInstance(this).salahDao().updateRecord(r)
    }

    private fun getFardStat(r: SalahRecord?, p: String): String {
        return r?.getFardStat(p) ?: "no"
    }

    private fun setFardStat(r: SalahRecord, p: String, s: String) {
        r.setFardStat(p, s)
    }

    private fun getQazaStat(r: SalahRecord?, p: String): Boolean {
        return r?.getQazaStat(p) ?: false
    }

    private fun setQazaStat(r: SalahRecord, p: String, q: Boolean) {
        r.setQazaStat(p, q)
    }

    override fun onResume() {
        super.onResume()
        if (::sp.isInitialized && sp.getString("user_email", "").orEmpty().isNotEmpty()
            && sp.getString("offline_q", "").orEmpty().isEmpty()) {
            fbHelper.fetchAndLoad(null, Runnable {
                loadTodayPage()
                refreshWidget()
            }, null)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            requestWindowFeature(Window.FEATURE_NO_TITLE)
            window.setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN)
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                or (if (!isDarkTheme && Build.VERSION.SDK_INT >= 23) View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR else 0))

            val conf = resources.configuration
            if (conf.fontScale != 1.0f) {
                conf.fontScale = 1.0f
                val metrics = resources.displayMetrics
                val wm = getSystemService(Context.WINDOW_SERVICE) as WindowManager
                @Suppress("DEPRECATION")
                wm.defaultDisplay.getMetrics(metrics)
                metrics.scaledDensity = conf.fontScale * metrics.density
                @Suppress("DEPRECATION")
                baseContext.resources.updateConfiguration(conf, metrics)
            }
        } catch (e: Exception) {
            Log.e("SalahTracker", "Error", e)
        }

        DENSITY = resources.displayMetrics.density
        sp = getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)

        DataMigrationHelper.migrateOldDataToRoom(this)
        selectedDate[0] = sdf.format(Date())
        calendarViewPointer = Calendar.getInstance()

        val savedDate = intent.getLongExtra("RESTORE_DATE", -1L)
        if (savedDate != -1L) {
            selectedDate[0] = sdf.format(Date(savedDate))
            calendarViewPointer.timeInMillis = savedDate
        }

        val systemDark = (resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES
        isDarkTheme = sp.getBoolean("is_dark_mode", systemDark)
        activeTheme = sp.getInt("app_theme", 0)
        val themeAccents = arrayOf("#00BFA5", "#3B82F6", "#FF9559", "#D81B60", "#A67BFF", "#3BCC75")

        if (isDarkTheme) {
            themeColors[0] = Color.parseColor("#1C1C1E")
            themeColors[1] = Color.parseColor("#1C1C1E")
            themeColors[2] = Color.parseColor("#FFFFFF")
            themeColors[3] = Color.parseColor("#A0A0A5")
            themeColors[4] = Color.parseColor("#2C2C2E")
        } else {
            themeColors[0] = Color.parseColor("#E2E8F0")
            themeColors[1] = Color.parseColor("#FFFFFF")
            themeColors[2] = Color.parseColor("#141416")
            themeColors[3] = Color.parseColor("#64748B")
            themeColors[4] = Color.parseColor("#E2E8F0")
        }
        colorAccent = Color.parseColor(themeAccents[activeTheme % themeAccents.size])
        themeColors[5] = Color.argb(40, Color.red(colorAccent), Color.green(colorAccent), Color.blue(colorAccent))

        if (Build.VERSION.SDK_INT >= 21) {
            window.statusBarColor = if (!isDarkTheme && Build.VERSION.SDK_INT < 23) Color.parseColor("#40000000") else Color.TRANSPARENT
            window.navigationBarColor = themeColors[0]
        }
        actionBar?.hide()

        lang = LanguageEngine(sp.getString("app_lang", "en") ?: "en")
        ui = UIComponents(this, DENSITY, themeColors, lang)
        fbHelper = FirebaseManager(this, sp)

        root = FrameLayout(this)
        if (Build.VERSION.SDK_INT >= 17) {
            root.layoutDirection = View.LAYOUT_DIRECTION_LTR
        }
        val scrollView = ScrollView(this).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
            isFillViewport = true
            overScrollMode = View.OVER_SCROLL_NEVER
        }
        contentArea = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }
        scrollView.addView(contentArea, FrameLayout.LayoutParams(-1, -1))
        root.addView(scrollView)
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        setContentView(root)

        // Dynamic scanner to adjust arrow buttons
        window.decorView.post {
            try {
                val decor = window.decorView
                val stack = Stack<View>()
                stack.push(decor)
                var prevArrow: View? = null
                var nextArrow: View? = null

                while (!stack.isEmpty()) {
                    val v = stack.pop()
                    if (v is TextView) {
                        val txt = v.text.toString()
                        if (txt == "<" || txt == "❮") {
                            if (v.parent is NeumorphCardView) prevArrow = v.parent as View
                        }
                        if (txt == ">" || txt == "❯") {
                            if (v.parent is NeumorphCardView) nextArrow = v.parent as View
                        }
                    }
                    if (v is ViewGroup) {
                        for (i in 0 until v.childCount) stack.push(v.getChildAt(i))
                    }
                }

                val den = resources.displayMetrics.density
                if (prevArrow != null) {
                    val lp = prevArrow.layoutParams
                    lp.width = (52 * den).toInt()
                    lp.height = (52 * den).toInt()
                    prevArrow.layoutParams = lp
                }
                if (nextArrow != null) {
                    val lp = nextArrow.layoutParams
                    lp.width = (52 * den).toInt()
                    lp.height = (52 * den).toInt()
                    nextArrow.layoutParams = lp
                }
            } catch (e: Exception) {
            }
        }

        appFonts[0] = Typeface.DEFAULT
        appFonts[1] = Typeface.DEFAULT_BOLD
        try {
            if (sp.getString("app_lang", "en") == "bn") {
                appFonts[0] = Typeface.createFromAsset(assets, "fonts/hind_reg.ttf")
                appFonts[1] = Typeface.createFromAsset(assets, "fonts/hind_bold.ttf")
            } else {
                appFonts[0] = Typeface.createFromAsset(assets, "fonts/poppins_reg.ttf")
                appFonts[1] = Typeface.createFromAsset(assets, "fonts/poppins_bold.ttf")
            }
        } catch (e: Exception) {
            Log.e("SalahTracker", "Error", e)
        }

        root.viewTreeObserver.addOnGlobalLayoutListener {
            applyFont(root, appFonts[0], appFonts[1])
        }

        val reloadTask = Runnable {
            loadTodayPage()
            refreshWidget()
        }
        statsHelper = StatsHelper(this, DENSITY, themeColors, colorAccent, lang, ui, sp, AppConstants.PRAYERS, appFonts)
        backupHelper = BackupHelper(this, sp, ui, lang, fbHelper, DENSITY, themeColors, colorAccent, root)
        calHelper = CalendarHelper(this, DENSITY, themeColors, colorAccent, lang, ui, sp, AppConstants.PRAYERS, selectedDate, calendarViewPointer, reloadTask)

        fbHelper.processOfflineQueue(
            Runnable {
                ui.showSmartBanner(root, lang.get("Syncing Data"), lang.get("Connecting to cloud..."), "img_cloud", colorAccent, null)
            },
            Runnable {
                ui.showSmartBanner(root, lang.get("Sync Complete"), lang.get("Progress updated."), "img_tick", colorAccent, null)
                loadTodayPage()
                refreshWidget()
            },
            Runnable {
                ui.hideLoadingBanner(root)
            }
        )

        loadTodayPage()
        refreshWidget()
        setupMidnightRefresh()
        MidnightWorker.scheduleNextMidnight(this)

        if (sp.getBoolean("is_first_run_tutorial", true)) {
            OnboardingHelper(this, DENSITY, themeColors, colorAccent, lang, ui, sp, root, appFonts).showOnboarding()
        }
    }

    private fun applyFont(v: View, reg: Typeface?, bold: Typeface?) {
        if (v is TextView) {
            if (v.typeface != null && v.typeface.isBold) {
                v.typeface = bold
            } else {
                v.typeface = reg
            }
        } else if (v is ViewGroup) {
            for (i in 0 until v.childCount) {
                applyFont(v.getChildAt(i), reg, bold)
            }
        }
    }

    private fun refreshWidget() {
        try {
            val intent = Intent(this, SalahWidget::class.java).apply {
                action = AppWidgetManager.ACTION_APPWIDGET_UPDATE
                val ids = AppWidgetManager.getInstance(this@MainActivity)
                    .getAppWidgetIds(ComponentName(this@MainActivity, SalahWidget::class.java))
                putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, ids)
            }
            sendBroadcast(intent)
        } catch (e: Exception) {
            Log.e("SalahTracker", "Error", e)
        }
    }

    private fun setupMidnightRefresh() {
        val c = Calendar.getInstance().apply {
            add(Calendar.DAY_OF_MONTH, 1)
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 500)
        }
        var delay = c.timeInMillis - System.currentTimeMillis()
        if (delay < 0) delay = 86400000L

        Handler(Looper.getMainLooper()).postDelayed({
            selectedDate[0] = sdf.format(Date())
            calendarViewPointer.time = Date()
            loadTodayPage()
            refreshWidget()
            setupMidnightRefresh()
            MidnightWorker.scheduleNextMidnight(this@MainActivity)
        }, delay)
    }

    fun getStatusColor(k: String?): Int {
        if (k == null) return themeColors[4]
        val r = getRoomRecord(k)
        var d = 0
        var e = 0
        for (p in AppConstants.PRAYERS) {
            val s = getFardStat(r, p)
            if ("yes" == s) d++
            else if ("excused" == s) e++
        }
        if (d + e == 0) return Color.TRANSPARENT
        if (e == 6) return Color.parseColor("#8B5CF6")
        return if (d == 6) Color.parseColor("#22C55E") else Color.parseColor("#10B981")
    }

    fun getProgressBorder(k: String?, s: Boolean): Drawable {
        val c = getStatusColor(k)
        var d = 0
        if (k != null) {
            val r = getRoomRecord(k)
            for (p in AppConstants.PRAYERS) {
                val st = getFardStat(r, p)
                if ("yes" == st || "excused" == st) d++
            }
        }
        if (s) {
            return GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(colorAccent)
            }
        }
        return UIComponents.ProgressDrawable(d, 6, if (c == 0) themeColors[4] else c, themeColors[4], DENSITY)
    }

    private fun updateLivePercentage(dK: String) {
        try {
            var nC = 0
            val currR = SalahDatabase.getInstance(this).salahDao().getRecordByDate(dK)
            if (currR != null) {
                for (pr in AppConstants.PRAYERS) {
                    val s = getFardStat(currR, pr)
                    if (s == "yes" || s == "excused") nC++
                }
            }
            val pT = window.decorView.findViewWithTag<TextView>("PERCENT_TEXT")
            val subBtm = window.decorView.findViewWithTag<TextView>("SUB_TEXT")
            pT?.text = "${lang.bnNum(nC * 100 / 6)}%"

            val statusMsgs = arrayOf(
                lang.get("Start your journey"),
                lang.get("Great start!"),
                lang.get("Keep going"),
                lang.get("Good progress!"),
                lang.get("Almost done!"),
                lang.get(if (sp.getString("app_lang", "en") == "bn") "আর মাত্র ১টি বাকি!" else "Just one more!"),
                lang.get("Purity Achieved!")
            )
            subBtm?.text = statusMsgs[nC]
        } catch (e: Exception) {
        }
    }

    // --- DIALOG DELEGATES ---
    private fun showJamaatDialog(jKey: String) {
        MainDialogs.showJamaatDialog(this, jKey, themeColors, colorAccent, lang, ui, sp, appFonts) {
            loadTodayPage()
            refreshWidget()
        }
    }

    private fun showRakatEditDialog(globKey: String, titleStr: String, currentRakat: Int) {
        MainDialogs.showRakatEditDialog(this, globKey, titleStr, currentRakat, themeColors, colorAccent, appFonts, sp) {
            loadTodayPage()
            refreshWidget()
        }
    }

    private fun showExcuseDialog() {
        MainDialogs.showExcuseDialog(
            this, selectedDate[0], themeColors, colorAccent, isDarkTheme,
            lang, ui, sp, appFonts, fbHelper
        ) {
            loadTodayPage()
            refreshWidget()
        }
    }

    private fun showSettingsMenu() {
        MainDialogs.showSettingsMenu(
            this, selectedDate[0], themeColors, colorAccent, activeTheme, isDarkTheme,
            lang, ui, sp, appFonts, statsHelper, backupHelper,
            onReload = {
                val intent = Intent(this, MainActivity::class.java).apply {
                    addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                startActivity(intent)
                finish()
            },
            onShowQazaList = {
                showQazaListDialog()
            }
        )
    }

    private fun showQazaListDialog() {
        MainDialogs.showQazaListDialog(this, themeColors, colorAccent, lang, ui, sp, appFonts) {
            loadTodayPage()
            refreshWidget()
        }
    }

    private fun showMarkOptions() {
        MainDialogs.showMarkOptions(
            this, selectedDate[0], themeColors, appFonts, sp, fbHelper, lang,
            onDone = {
                loadTodayPage()
                refreshWidget()
            },
            onShowSuccess = {
                showSuccessSequence()
            }
        )
    }

    private fun showUnmarkOptions() {
        MainDialogs.showUnmarkOptions(
            this, selectedDate[0], themeColors, appFonts, sp, fbHelper, lang
        ) {
            loadTodayPage()
            refreshWidget()
        }
    }

    private fun showSuccessSequence() {
        MainDialogs.showSuccessSequence(this, root, selectedDate[0], colorAccent, lang, appFonts, sp)
    }

    private fun showRozaCategoryDialog() {
        MainDialogs.showRozaCategoryDialog(this, selectedDate[0], themeColors, colorAccent, lang, ui, sp, appFonts) {
            loadTodayPage()
            refreshWidget()
        }
    }

    private fun showBengaliCalendar() {
        BengaliCalendarHelper.showBengaliCalendar(
            this, selectedDate[0], themeColors, colorAccent, isDarkTheme, lang, ui, sp, appFonts
        ) { dateKey ->
            selectedDate[0] = dateKey
            loadTodayPage()
            refreshWidget()
        }
    }

    // --- MAIN UI RENDERER ---
    fun loadTodayPage() {
        val savedScrollPos = (contentArea.parent as? ScrollView)?.scrollY ?: 0
        contentArea.removeAllViews()
        contentArea.post {
            (contentArea.parent as? ScrollView)?.scrollTo(0, savedScrollPos)
        }

        root.setBackgroundColor(themeColors[0])
        val isLandscape = resources.configuration.orientation == Configuration.ORIENTATION_LANDSCAPE
        val todayRec = getRoomRecord(selectedDate[0])

        contentArea.addView(buildHeader())
        contentArea.addView(buildProgressCard(todayRec))
        contentArea.addView(buildWeekNavigator())
        contentArea.addView(buildActionRow(todayRec))
        contentArea.addView(buildCardsContainer(todayRec, isLandscape))

        if (appFonts[0] != null) applyFont(root, appFonts[0], appFonts[1])
    }

    private fun buildHeader(): View {
        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(20), dp(15), dp(20), dp(10))
        }

        val leftHeader = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            gravity = Gravity.CENTER_VERTICAL
        }

        val dEn = TextView(this).apply {
            try {
                val dt = sdf.parse(selectedDate[0]) ?: Date()
                val gc = Calendar.getInstance().apply { time = dt }
                val dNum = gc.get(Calendar.DAY_OF_MONTH)
                val isBnLang = sp.getString("app_lang", "en") == "bn"

                if (isBnLang) {
                    val gsuf = when {
                        dNum == 1 -> "লা"
                        dNum in 2..3 -> "রা"
                        dNum == 4 -> "ঠা"
                        dNum in 5..18 -> "ই"
                        else -> "শে"
                    }
                    val gMs = arrayOf("জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর")
                    val mStr = gMs[gc.get(Calendar.MONTH)]
                    val dStr = dNum.toString().toBnDigits()
                    val yStr = gc.get(Calendar.YEAR).toString().toBnDigits()
                    text = "$dStr$gsuf $mStr, $yStr"
                } else {
                    val gsuf = if (dNum in 11..13) "th"
                    else when (dNum % 10) {
                        1 -> "st"
                        2 -> "nd"
                        3 -> "rd"
                        else -> "th"
                    }
                    val mStr = SimpleDateFormat("MMMM", Locale.US).format(dt)
                    text = "$dNum$gsuf $mStr, ${gc.get(Calendar.YEAR)}"
                }
            } catch (e: Exception) {
            }
            setTextColor(themeColors[3])
            textSize = 14f
            setTypeface(appFonts[0], Typeface.BOLD)
            setPadding(0, 0, 0, dp(2))
            setOnClickListener { calHelper.showGregorian() }
        }
        leftHeader.addView(dEn)

        val dBn = TextView(this).apply {
            try {
                text = getBnDateStr(selectedDate[0], sp)
            } catch (e: Exception) {
            }
            setTextColor(themeColors[2])
            textSize = 14f
            setTypeface(appFonts[0], Typeface.BOLD)
            setPadding(0, 0, 0, dp(4))
            setOnClickListener { showBengaliCalendar() }
        }
        leftHeader.addView(dBn)

        val hRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setOnClickListener { calHelper.showHijri() }
        }
        val moon = ui.getRoundImage("img_moon", 0, Color.TRANSPARENT, colorAccent).apply {
            layoutParams = LinearLayout.LayoutParams(dp(16), dp(16)).apply {
                setMargins(0, 0, dp(8), 0)
            }
        }
        hRow.addView(moon)

        val dHijri = TextView(this).apply {
            try {
                text = ui.getHijriDate(sdf.parse(selectedDate[0]) ?: Date(), sp.getInt("hijri_offset", 0))
            } catch (e: Exception) {
            }
            setTextColor(colorAccent)
            textSize = 14f
            setTypeface(appFonts[1], Typeface.BOLD)
        }
        hRow.addView(dHijri)
        leftHeader.addView(hRow)

        val rightHeader = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.END or Gravity.CENTER_VERTICAL
        }

        val streakCount = ui.calculateStreak(sp, AppConstants.PRAYERS)
        val isBn = sp.getString("app_lang", "en") == "bn"

        val stBadge = TextView(this).apply {
            textSize = 12f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(colorAccent)
            text = if (streakCount >= 365) {
                if (isBn) "১ বছর" else "1 YEAR"
            } else {
                if (isBn) "${lang.bnNum(streakCount)} দিন" else "$streakCount DAYS"
            }
            applyNeo(this, 0, 15f, 3f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            setPadding(dp(12), dp(6), dp(12), dp(6))
        }
        rightHeader.addView(stBadge, LinearLayout.LayoutParams(-2, -2).apply {
            setMargins(0, 0, dp(10), 0)
        })

        val periodBtn = ui.getRoundImage("img_period", 6, Color.TRANSPARENT, colorAccent).apply {
            applyNeo(this, 0, 20f, 3f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            layoutParams = LinearLayout.LayoutParams(dp(34), dp(34)).apply {
                setMargins(0, 0, dp(8), 0)
            }
            setOnClickListener { showExcuseDialog() }
        }
        rightHeader.addView(periodBtn)

        val settingsBtn = ui.getRoundImage("img_settings", 6, Color.TRANSPARENT, colorAccent).apply {
            applyNeo(this, 0, 20f, 3f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            layoutParams = LinearLayout.LayoutParams(dp(34), dp(34))
            setOnClickListener { showSettingsMenu() }
        }
        rightHeader.addView(settingsBtn)

        header.addView(leftHeader)
        header.addView(rightHeader)
        return header
    }

    private fun buildProgressCard(todayRec: SalahRecord): View {
        val hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY)
        val greetingStr = when (hour) {
            in 4..11 -> lang.get("Good Morning")
            in 12..16 -> lang.get("Good Afternoon")
            in 17..19 -> lang.get("Good Evening")
            else -> lang.get("Good Night")
        }

        val pCard = LinearLayout(this).apply {
            setPadding(dp(15), dp(2), dp(15), dp(2))
            layoutParams = FrameLayout.LayoutParams(-1, -2)
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }

        val baseR = Color.red(colorAccent)
        val baseG = Color.green(colorAccent)
        val baseB = Color.blue(colorAccent)
        pCard.background = GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            intArrayOf(
                Color.argb(220, baseR, baseG, baseB),
                Color.argb(120, baseR, baseG, baseB),
                Color.argb(190, baseR, baseG, baseB)
            )
        ).apply {
            cornerRadius = 20f * DENSITY
            setStroke(dp(1.5f), Color.argb(150, 255, 255, 255))
        }

        val pNeo = createNeoCard(0, 20f, 8f, isDarkTheme).apply {
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(dp(10), 0, dp(10), dp(4))
            }
            addView(pCard)
        }

        var countCompleted = 0
        for (p in AppConstants.PRAYERS) {
            val status = getFardStat(todayRec, p)
            if (status == "yes" || status == "excused") countCompleted++
        }
        val statusMsgs = arrayOf(
            lang.get("Start your journey"),
            lang.get("Great start!"),
            lang.get("Keep going"),
            lang.get("Good progress!"),
            lang.get("Almost done!"),
            lang.get(if (sp.getString("app_lang", "en") == "bn") "আর মাত্র ১টি বাকি!" else "Just one more!"),
            lang.get("Purity Achieved!")
        )

        val left = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, -2, 1.2f)
        }
        left.addView(TextView(this).apply {
            text = greetingStr
            setTextColor(Color.WHITE)
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
        })
        left.addView(TextView(this).apply {
            text = "${lang.bnNum(countCompleted * 100 / 6)}%"
            tag = "PERCENT_TEXT"
            setTextColor(Color.WHITE)
            textSize = 36f
            typeface = Typeface.DEFAULT_BOLD
        })
        left.addView(TextView(this).apply {
            text = statusMsgs[countCompleted]
            tag = "SUB_TEXT"
            setTextColor(Color.WHITE)
            textSize = 12f
            alpha = 0.9f
        })

        val tasbihView = PremiumTasbihView(this, isDarkTheme, colorAccent).apply {
            layoutParams = LinearLayout.LayoutParams(0, -2, 0.8f)
        }

        if (!isDarkTheme) {
            val color1 = Color.rgb((baseR * 0.9).toInt(), (baseG * 0.9).toInt(), (baseB * 0.9).toInt())
            val color2 = Color.rgb((baseR * 0.75).toInt(), (baseG * 0.75).toInt(), (baseB * 0.75).toInt())
            pCard.background = GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                intArrayOf(color1, color2)
            ).apply {
                cornerRadius = 30f
            }
        }

        pCard.addView(left)
        pCard.addView(tasbihView)
        return pNeo
    }

    private fun buildWeekNavigator(): View {
        val now = Calendar.getInstance()
        val selectedCalArr = arrayOf(Calendar.getInstance())
        try {
            selectedCalArr[0].time = sdf.parse(selectedDate[0]) ?: Date()
        } catch (e: Exception) {
            Log.e("SalahTracker", "Error", e)
        }

        val weekNavBox = LinearLayout(this).apply {
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(15), 0, dp(15), 0)
        }

        val prevW = TextView(this).apply {
            text = "❮"
            textSize = 16f
            setTextColor(themeColors[2])
            gravity = Gravity.CENTER
            applyNeo(this, 1, 15f, 3f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            layoutParams = LinearLayout.LayoutParams(dp(34), dp(34))
            setPadding(5, 2, 5, 2)
            setOnClickListener {
                val chk = selectedCalArr[0].clone() as Calendar
                chk.add(Calendar.DATE, -7)
                if (chk.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) {
                    selectedCalArr[0].add(Calendar.DATE, -7)
                    selectedDate[0] = sdf.format(selectedCalArr[0].time)
                    loadTodayPage()
                } else {
                    ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null)
                }
            }
        }

        val weekBox = LinearLayout(this).apply {
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            gravity = Gravity.CENTER
        }
        val cal = selectedCalArr[0].clone() as Calendar
        while (cal.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) {
            cal.add(Calendar.DATE, -1)
        }

        for (i in 0 until 7) {
            val dKey = sdf.format(cal.time)
            val isTooOld = cal.get(Calendar.YEAR) < now.get(Calendar.YEAR) - 100
            val isSel = dKey == selectedDate[0]
            val isFuture = cal.after(now)

            var dLabel = SimpleDateFormat("EEEE", Locale.US).format(cal.time).substring(0, 1)
            if (sp.getString("app_lang", "en") == "bn") {
                val bnD = arrayOf("র", "সো", "ম", "বু", "বৃ", "শু", "শ")
                dLabel = bnD[cal.get(Calendar.DAY_OF_WEEK) - 1]
            }

            val cell = FrameLayout(this).apply {
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            }
            val neoW = createNeoCard(
                shapeType = 1,
                radiusDp = 26f,
                elevationDp = 6f,
                isDark = isDarkTheme,
                bgColor = if (isSel) colorAccent else if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0")
            ).apply {
                val neoPad = dp(8)
                setPadding(neoPad, neoPad, neoPad, neoPad)
                layoutParams = FrameLayout.LayoutParams(dp(52), dp(52)).apply {
                    gravity = Gravity.CENTER
                }
            }

            val t = TextView(this).apply {
                text = dLabel
                typeface = Typeface.DEFAULT_BOLD
                textSize = 13f
                gravity = Gravity.CENTER
                setTextColor(
                    if (isSel) Color.parseColor("#F1F5F9")
                    else if (isFuture) Color.parseColor("#94A3B8")
                    else themeColors[3]
                )
                layoutParams = FrameLayout.LayoutParams(-1, -1)
            }

            neoW.addView(t)
            cell.addView(neoW)
            cell.setOnClickListener {
                when {
                    isFuture -> ui.showPremiumLocked(colorAccent)
                    isTooOld -> ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null)
                    else -> {
                        selectedDate[0] = dKey
                        loadTodayPage()
                    }
                }
            }
            weekBox.addView(cell)
            cal.add(Calendar.DATE, 1)
        }

        val nextW = TextView(this).apply {
            text = "❯"
            textSize = 16f
            setTextColor(themeColors[2])
            gravity = Gravity.CENTER
            applyNeo(this, 1, 15f, 3f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            layoutParams = LinearLayout.LayoutParams(dp(34), dp(34))
            setPadding(5, 2, 5, 2)
        }

        val weekStartNow = now.clone() as Calendar
        while (weekStartNow.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) {
            weekStartNow.add(Calendar.DATE, -1)
        }
        val isCurrentWeekArr = !selectedCalArr[0].before(weekStartNow)
        nextW.alpha = if (isCurrentWeekArr) 0.3f else 1.0f

        nextW.setOnClickListener {
            if (!isCurrentWeekArr) {
                selectedCalArr[0].add(Calendar.DATE, 7)
                if (selectedCalArr[0].after(Calendar.getInstance())) {
                    selectedCalArr[0].time = Calendar.getInstance().time
                }
                selectedDate[0] = sdf.format(selectedCalArr[0].time)
                loadTodayPage()
            }
        }

        weekNavBox.addView(prevW)
        weekNavBox.addView(weekBox)
        weekNavBox.addView(nextW)
        return weekNavBox
    }

    private fun buildActionRow(todayRec: SalahRecord): View {
        var countCompleted = 0
        for (p in AppConstants.PRAYERS) {
            val status = getFardStat(todayRec, p)
            if (status == "yes" || status == "excused") countCompleted++
        }

        val actionRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(dp(20), 0, dp(20), 0)
            weightSum = 2f
        }

        val markAllBtn = LinearLayout(this).apply {
            gravity = Gravity.CENTER
            layoutParams = LinearLayout.LayoutParams(0, -1, 1f).apply {
                setMargins(dp(16), dp(4), dp(8), dp(4))
            }
            applyNeo(this, 0, 12f, 4f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            setPadding(dp(16), dp(10), dp(16), dp(10))
        }

        val markAllTxt = TextView(this).apply {
            textSize = 13f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(themeColors[2])
        }

        val isAllDone = countCompleted >= 6
        markAllTxt.text = lang.get(if (isAllDone) "All Done" else "Mark All")

        val mIcon = ui.getRoundImage(if (isAllDone) "img_trophy" else "img_tick", 4, Color.TRANSPARENT, colorAccent).apply {
            layoutParams = FrameLayout.LayoutParams(dp(22), dp(22)).apply { gravity = Gravity.CENTER }
            setBackgroundColor(Color.TRANSPARENT)
        }
        val mIconFrame = FrameLayout(this).apply {
            layoutParams = LinearLayout.LayoutParams(dp(30), dp(30)).apply {
                setMargins(0, 0, dp(10), 0)
            }
            applyNeo(this, 0, 12f, 3f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            addView(mIcon)
        }
        markAllBtn.addView(mIconFrame)
        markAllBtn.addView(markAllTxt)
        markAllBtn.setOnClickListener {
            if (isAllDone) showUnmarkOptions() else showMarkOptions()
        }
        markAllBtn.setOnLongClickListener { v ->
            v.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS)
            val r = getRoomRecord(selectedDate[0])
            for (p in AppConstants.PRAYERS) {
                setQazaStat(r, p, true)
                setFardStat(r, p, "no")
                sp.edit().putBoolean("${selectedDate[0]}_${p}_qaza", true).putString("${selectedDate[0]}_$p", "no").apply()
                fbHelper.save(selectedDate[0], p, "no")
            }
            updateRoomRecord(r)
            ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null)
            loadTodayPage()
            refreshWidget()
            true
        }
        actionRow.addView(markAllBtn)

        val todayBtn = LinearLayout(this).apply {
            gravity = Gravity.CENTER
            layoutParams = LinearLayout.LayoutParams(0, -1, 1f).apply {
                setMargins(dp(8), dp(4), dp(16), dp(4))
            }
            applyNeo(this, 0, 12f, 4f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            setPadding(dp(16), dp(10), dp(16), dp(10))
        }

        val todayTxt = TextView(this).apply {
            textSize = 13f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(themeColors[2])
        }

        if (selectedDate[0] != sdf.format(Date())) {
            todayTxt.text = lang.get("Today")
            todayBtn.setOnClickListener {
                selectedDate[0] = sdf.format(Date())
                calendarViewPointer.time = Date()
                loadTodayPage()
            }
        } else {
            todayTxt.text = lang.get("This Week")
            todayBtn.setOnClickListener {
                try {
                    statsHelper.syncDate(sdf.parse(selectedDate[0]) ?: Date())
                } catch (e: Exception) {
                    Log.e("SalahTracker", "Error", e)
                }
                statsHelper.showStats(true)
            }
        }

        val tIcon = ui.getRoundImage("img_calender", 4, Color.TRANSPARENT, colorAccent).apply {
            layoutParams = FrameLayout.LayoutParams(dp(22), dp(22)).apply { gravity = Gravity.CENTER }
            setBackgroundColor(Color.TRANSPARENT)
        }
        val tIconFrame = FrameLayout(this).apply {
            layoutParams = LinearLayout.LayoutParams(dp(30), dp(30)).apply {
                setMargins(0, 0, dp(10), 0)
            }
            applyNeo(this, 0, 12f, 3f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            addView(tIcon)
        }
        todayBtn.addView(tIconFrame)
        todayBtn.addView(todayTxt)
        actionRow.addView(todayBtn)

        return actionRow
    }

    private fun buildCardsContainer(todayRec: SalahRecord, isLandscape: Boolean): View {
        val cardsContainer = LinearLayout(this).apply {
            orientation = if (isLandscape) LinearLayout.HORIZONTAL else LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(-1, 0, 1f)
            setPadding(dp(20), 0, dp(20), dp(30))
        }

        var col1: LinearLayout? = null
        var col2: LinearLayout? = null
        if (isLandscape) {
            col1 = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = LinearLayout.LayoutParams(0, -1, 1f)
                setPadding(0, 0, dp(8), 0)
                weightSum = 3f
            }
            col2 = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = LinearLayout.LayoutParams(0, -1, 1f)
                setPadding(dp(8), 0, 0, 0)
                weightSum = 3f
            }
            cardsContainer.addView(col1)
            cardsContainer.addView(col2)
        } else {
            cardsContainer.weightSum = 6f
        }

        val isBn = sp.getString("app_lang", "en") == "bn"
        val pImgs = arrayOf("img_fajr", "img_dhuhr", "img_asr", "img_maghrib", "img_isha", "img_witr")

        // 6 FARD CARDS
        for (i in 0 until 6) {
            val name = AppConstants.PRAYERS[i]
            val key = "${selectedDate[0]}_$name"
            val stat = getFardStat(todayRec, name)
            val isQaza = getQazaStat(todayRec, name)

            val card = createNeoCard(0, 16f, 3f, isDarkTheme).apply {
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, if (i == 5) dp(15) else 0)
                }
            }

            val innerCard = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                setPadding(dp(20), dp(18), dp(20), dp(18))
            }
            card.addView(innerCard)

            val iconView = ui.getRoundImage(pImgs[i], 8, Color.TRANSPARENT, colorAccent).apply {
                setBackgroundColor(Color.TRANSPARENT)
                setPadding(5, 2, 5, 2)
                layoutParams = FrameLayout.LayoutParams(dp(34), dp(34)).apply { gravity = Gravity.CENTER }
            }
            val iconFrame = FrameLayout(this).apply {
                layoutParams = LinearLayout.LayoutParams(dp(30), dp(30)).apply {
                    setMargins(0, 0, dp(15), 0)
                }
                applyNeo(this, 0, 12f, 2.5f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
                addView(iconView)
            }
            innerCard.addView(iconFrame)

            val textContainer = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            }
            val titleRow = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
            }
            val tv = TextView(this).apply {
                text = lang.get(name)
                setTextColor(if (stat == "excused") Color.parseColor("#FF4081") else themeColors[2])
                typeface = Typeface.DEFAULT_BOLD
                textSize = 16f
                isSingleLine = true
            }
            titleRow.addView(tv)

            if (isQaza && stat == "no") {
                val qBadge = TextView(this).apply {
                    text = lang.get("QAZA")
                    setTextColor(themeColors[2])
                    textSize = 10f
                    typeface = Typeface.DEFAULT_BOLD
                    setPadding(dp(8), dp(3), dp(8), dp(3))
                    background = GradientDrawable().apply {
                        setColor(themeColors[5])
                        cornerRadius = 10f * DENSITY
                    }
                    layoutParams = LinearLayout.LayoutParams(-2, -2).apply {
                        setMargins(dp(10), 0, 0, 0)
                    }
                }
                titleRow.addView(qBadge)
            }
            textContainer.addView(titleRow)
            innerCard.addView(textContainer)

            if (stat != "excused") {
                val jKey = "${selectedDate[0]}_${name}_jamaat"
                val jStat = sp.getString(jKey, if (name == "Witr") "alone" else "jamaat") ?: "jamaat"
                val isDone = stat == "yes"
                val sText = if (jStat == "jamaat") (if (isBn) "জামাতের সাথে" else "Jamaat")
                else (if (isBn) "একাকী" else "Alone")

                val jamaatBtn = TextView(this).apply {
                    text = sText
                    textSize = 11f
                    isSingleLine = true
                    setTextColor(if (isDone) Color.WHITE else themeColors[2])
                    applyNeo(this, 1, 10f, 2f,
                        if (isDone) colorAccent
                        else if (isDarkTheme) Color.parseColor("#1C1C1E")
                        else Color.parseColor("#E2E8F0"),
                        isDarkTheme
                    )
                    setPadding(dp(12), dp(6), dp(12), dp(8))
                    layoutParams = LinearLayout.LayoutParams(-2, -2).apply {
                        setMargins(0, 0, dp(15), 0)
                    }
                    setOnClickListener { v ->
                        if (stat != "yes") return@setOnClickListener
                        v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        showJamaatDialog(jKey)
                    }
                }
                innerCard.addView(jamaatBtn)
            }

            val chk = getNeoCheckbox(stat, colorAccent)
            innerCard.addView(chk)

            card.setOnClickListener { v ->
                if (stat == "excused") {
                    val r = getRoomRecord(selectedDate[0])
                    setFardStat(r, name, "no")
                    updateRoomRecord(r)
                    sp.edit().putString(key, "no").apply()
                    fbHelper.save(selectedDate[0], name, "no")
                    loadTodayPage()
                    refreshWidget()
                    return@setOnClickListener
                }
                v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                val currentStatus = stat == "yes"
                val newVal = if (!currentStatus) "yes" else "no"

                val r = getRoomRecord(selectedDate[0])
                if (newVal == "yes" && getQazaStat(r, name)) {
                    setQazaStat(r, name, false)
                    sp.edit().putBoolean("${key}_qaza", false).apply()
                }
                setFardStat(r, name, newVal)
                updateRoomRecord(r)
                sp.edit().putString(key, newVal).apply()
                fbHelper.save(selectedDate[0], name, newVal)

                v.bounceClick {
                    if (!currentStatus) {
                        var count = 0
                        for (p in AppConstants.PRAYERS) {
                            val s = getFardStat(r, p)
                            if (s == "yes" || s == "excused") count++
                        }
                        if (count == 6) showSuccessSequence()
                    }
                    loadTodayPage()
                    refreshWidget()
                }
            }

            card.setOnLongClickListener { v ->
                v.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS)
                val r = getRoomRecord(selectedDate[0])
                val wasQaza = getQazaStat(r, name)
                if (!wasQaza) {
                    setQazaStat(r, name, true)
                    setFardStat(r, name, "no")
                    updateRoomRecord(r)
                    sp.edit().putBoolean("${key}_qaza", true).putString(key, "no").apply()
                    fbHelper.save(selectedDate[0], name, "no")
                    ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null)
                } else {
                    setQazaStat(r, name, false)
                    updateRoomRecord(r)
                    sp.edit().putBoolean("${key}_qaza", false).apply()
                    ui.showSmartBanner(root, lang.get("Qaza Removed"), lang.get("Name removed from Qaza list."), "img_tick", colorAccent, null)
                }
                loadTodayPage()
                refreshWidget()
                true
            }

            if (isLandscape) {
                if (i < 3) col1?.addView(card) else col2?.addView(card)
            } else {
                cardsContainer.addView(card)
            }
        }

        // --- SUNNAH & NAFIL TRACKER ---
        val sHdr = TextView(this).apply {
            text = if (isBn) "সুন্নত ও নফল" else "Sunnah & Nafil"
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
        }
        val sHdrLp = LinearLayout.LayoutParams(-2, -2).apply {
            setMargins(0, dp(15), 0, dp(10))
        }
        if (isLandscape) col2?.addView(sHdr, sHdrLp) else cardsContainer.addView(sHdr, sHdrLp)

        for (sIdx in AppConstants.EXTRA_DB_KEYS.indices) {
            val sDbKey = "${selectedDate[0]}_${AppConstants.EXTRA_DB_KEYS[sIdx]}"
            val sTitleBn = AppConstants.EXTRA_PRAYERS_BN[sIdx]
            val sTitleEn = AppConstants.EXTRA_PRAYERS_EN[sIdx]
            val sDefRak = AppConstants.EXTRA_DEF_RAKAT[sIdx]
            val globRakatKey = "glob_rakat_${AppConstants.EXTRA_DB_KEYS[sIdx]}"

            val cardTitle = if (isBn) sTitleBn else sTitleEn
            @Suppress("DEPRECATION")
            val formattedTitle = Html.fromHtml(cardTitle.replace("\n", "<br>").replace("(", "<small>(").replace(")", ")</small>"))
            val stat2 = sp.getString(sDbKey, "no") ?: "no"
            val checked2 = stat2 == "yes"

            val curRakat = sp.getInt(globRakatKey, sDefRak)
            var rakStr = curRakat.toString()
            if (isBn) rakStr = rakStr.toBnDigits()
            val rakatLabel = "$rakStr " + (if (isBn) "রাকাত" else "Rakat")

            val sCard = buildTrackerCard(
                iconRes = "img_custom_nafl",
                title = formattedTitle,
                statusText = rakatLabel,
                isStatusActive = checked2,
                isChecked = checked2,
                marginBottom = if (sIdx == AppConstants.EXTRA_DB_KEYS.size - 1) dp(15) else 0,
                onStatusClick = {
                    showRakatEditDialog(globRakatKey, cardTitle, curRakat)
                },
                onCardClick = { v ->
                    val newVal = if (checked2) "no" else "yes"
                    sp.edit().putString(sDbKey, newVal).apply()
                    fbHelper.save(selectedDate[0], AppConstants.EXTRA_DB_KEYS[sIdx], newVal)
                    v.bounceClick { loadTodayPage() }
                }
            )

            if (isLandscape) col2?.addView(sCard) else cardsContainer.addView(sCard)
        }

        // --- ROZA TRACKER ---
        val rozaDbKey = "${selectedDate[0]}_roza_stat"
        val rozaHdr = TextView(this).apply {
            text = if (isBn) "অন্যান্য ইবাদত" else "Other Trackers"
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
        }
        val rozaHdrLp = LinearLayout.LayoutParams(-2, -2).apply {
            setMargins(0, dp(5), 0, dp(10))
        }

        val rozaType = sp.getString("${selectedDate[0]}_roza_type", "nafil") ?: "nafil"
        val isRozaDone = sp.getString(rozaDbKey, "no") == "yes"
        val catLabel = when (rozaType) {
            "fard" -> if (isBn) "ফরজ" else "Fard"
            "qaza" -> if (isBn) "কাজা" else "Qaza"
            else -> if (isBn) "নফল" else "Nafil"
        }

        val rCard = buildTrackerCard(
            iconRes = "img_roza",
            title = if (isBn) "রোজা" else "Fasting",
            statusText = catLabel,
            isStatusActive = isRozaDone,
            isChecked = isRozaDone,
            onStatusClick = { showRozaCategoryDialog() },
            onCardClick = { v ->
                sp.edit().putString(rozaDbKey, if (!isRozaDone) "yes" else "no").apply()
                v.bounceClick { loadTodayPage() }
            }
        )

        if (isLandscape) {
            col2?.addView(rozaHdr, rozaHdrLp)
            col2?.addView(rCard)
        } else {
            cardsContainer.addView(rozaHdr, rozaHdrLp)
            cardsContainer.addView(rCard)
        }

        // --- QURAN TRACKER ---
        val quranDbKey = "${selectedDate[0]}_quran_stat"
        val quranParaKey = "${selectedDate[0]}_quran_para"
        val quranPageKey = "${selectedDate[0]}_quran_page"

        val qHdr = TextView(this).apply {
            text = if (isBn) "কুরআন তেলাওয়াত" else "Quran Recitation"
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
        }
        val qHdrLp = LinearLayout.LayoutParams(-2, -2).apply {
            setMargins(0, dp(5), 0, dp(10))
        }

        val isQuranDone = sp.getString(quranDbKey, "no") == "yes"
        val paraCount = sp.getInt(quranParaKey, 0)
        val pageCount = sp.getInt(quranPageKey, 0)

        var qLabel = if (isBn) "পড়িনি" else "Not Read"
        if (paraCount > 0 && pageCount > 0) {
            qLabel = "$paraCount" + (if (isBn) " পারা " else " Para ") + "$pageCount" + (if (isBn) " পৃষ্ঠা" else " Page")
        } else if (paraCount > 0) {
            qLabel = "$paraCount" + (if (isBn) " পারা" else " Para")
        } else if (pageCount > 0) {
            qLabel = "$pageCount" + (if (isBn) " পৃষ্ঠা" else " Page")
        } else if (isQuranDone) {
            qLabel = if (isBn) "পড়েছি" else "Read"
        }
        if (isBn) qLabel = qLabel.toBnDigits()

        val qCard = buildTrackerCard(
            iconRes = "img_habit_quran",
            title = if (isBn) "আল কুরআন" else "Al Quran",
            statusText = qLabel,
            isStatusActive = isQuranDone,
            isChecked = isQuranDone,
            onStatusClick = {
                MainDialogs.showQuranDialog(this@MainActivity, selectedDate[0], themeColors, colorAccent, sp, appFonts) {
                    loadTodayPage()
                }
            },
            onCardClick = { v ->
                sp.edit().putString(quranDbKey, if (!isQuranDone) "yes" else "no").apply()
                v.bounceClick { loadTodayPage() }
            }
        )

        if (isLandscape) {
            col2?.addView(qHdr, qHdrLp)
            col2?.addView(qCard)
        } else {
            cardsContainer.addView(qHdr, qHdrLp)
            cardsContainer.addView(qCard)
        }

        return cardsContainer
    }

    private fun buildTrackerCard(
        iconRes: String,
        title: CharSequence,
        statusText: String?,
        isStatusActive: Boolean,
        isChecked: Boolean,
        marginBottom: Int = 0,
        onStatusClick: (() -> Unit)? = null,
        onCardClick: (View) -> Unit
    ): View {
        val card = createNeoCard(0, 16f, 3f, isDarkTheme).apply {
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, 0, 0, marginBottom)
            }
        }
        val inner = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(20), dp(18), dp(20), dp(18))
        }
        card.addView(inner)

        val icon = ui.getRoundImage(iconRes, 8, Color.TRANSPARENT, colorAccent).apply {
            setBackgroundColor(Color.TRANSPARENT)
            setPadding(5, 2, 5, 2)
            layoutParams = FrameLayout.LayoutParams(dp(34), dp(34)).apply { gravity = Gravity.CENTER }
        }
        val iconFrame = FrameLayout(this).apply {
            layoutParams = LinearLayout.LayoutParams(dp(30), dp(30)).apply {
                setMargins(0, 0, dp(15), 0)
            }
            applyNeo(this, 0, 12f, 2.5f, if (isDarkTheme) Color.parseColor("#1C1C1E") else Color.parseColor("#E2E8F0"), isDarkTheme)
            addView(icon)
        }
        inner.addView(iconFrame)

        val txtCon = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
        }
        txtCon.addView(TextView(this).apply {
            text = title
            setTextColor(themeColors[2])
            typeface = Typeface.DEFAULT_BOLD
            textSize = 16f
            maxLines = 2
        })
        inner.addView(txtCon)

        if (statusText != null) {
            val sBtn = TextView(this).apply {
                text = statusText
                textSize = 11f
                isSingleLine = true
                setTextColor(if (isStatusActive) Color.WHITE else themeColors[2])
                applyNeo(this, 1, 10f, 2f,
                    if (isStatusActive) colorAccent
                    else if (isDarkTheme) Color.parseColor("#1C1C1E")
                    else Color.parseColor("#E2E8F0"),
                    isDarkTheme
                )
                setPadding(dp(12), dp(6), dp(12), dp(8))
                layoutParams = LinearLayout.LayoutParams(-2, -2).apply {
                    setMargins(0, 0, dp(15), 0)
                }
                setOnClickListener { v ->
                    v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    onStatusClick?.invoke()
                }
            }
            inner.addView(sBtn)
        }

        val chk = getNeoCheckbox(if (isChecked) "yes" else "no", colorAccent)
        inner.addView(chk)

        card.setOnClickListener { v ->
            v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
            onCardClick(v)
        }
        return card
    }
}
