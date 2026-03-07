package com.my.salah.tracker.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.DisplayMetrics;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.view.ViewTreeObserver;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends Activity {
    
    private SharedPreferences sp;
    private float DENSITY;
    private boolean isDarkTheme;
    private int activeTheme;
    private int[] themeColors = new int[6];
    private int colorAccent;
    private String[] selectedDate = new String[1];
    private Calendar calendarViewPointer;

    private LanguageEngine lang;
    private UIComponents ui;
    private FirebaseManager fbHelper;
    private StatsHelper statsHelper;
    private BackupHelper backupHelper;
    private CalendarHelper calHelper;
    private Typeface[] appFonts = new Typeface[2];

    private FrameLayout root;
    private LinearLayout contentArea;
    private SimpleDateFormat sdf;

    private SalahRecord getRoomRecord(String date) {
        SalahDao dao = SalahDatabase.getDatabase(this).salahDao();
        SalahRecord r = dao.getRecordByDate(date);
        if (r == null) { r = new SalahRecord(date); dao.insertRecord(r); }
        return r;
    }
    
    private void updateRoomRecord(SalahRecord r) {
        SalahDatabase.getDatabase(this).salahDao().updateRecord(r);
    }
    
    private String getFardStat(SalahRecord r, String p) {
        if(r==null) return "no";
        switch(p){ case "Fajr":return r.fajr; case "Dhuhr":return r.dhuhr; case "Asr":return r.asr; case "Maghrib":return r.maghrib; case "Isha":return r.isha; case "Witr":return r.witr;
        default:return "no";}
    }
    
    private void setFardStat(SalahRecord r, String p, String s) {
        switch(p){ case "Fajr":r.fajr=s;break;
        case "Dhuhr":r.dhuhr=s;break; case "Asr":r.asr=s;break; case "Maghrib":r.maghrib=s;break; case "Isha":r.isha=s;break; case "Witr":r.witr=s;break;
        }
    }
    
    private boolean getQazaStat(SalahRecord r, String p) {
        if(r==null) return false;
        switch(p){ case "Fajr":return r.fajr_qaza; case "Dhuhr":return r.dhuhr_qaza; case "Asr":return r.asr_qaza; case "Maghrib":return r.maghrib_qaza; case "Isha":return r.isha_qaza; case "Witr":return r.witr_qaza;
        default:return false;}
    }
    
    private void setQazaStat(SalahRecord r, String p, boolean q) {
        switch(p){ case "Fajr":r.fajr_qaza=q;break;
        case "Dhuhr":r.dhuhr_qaza=q;break; case "Asr":r.asr_qaza=q;break; case "Maghrib":r.maghrib_qaza=q;break; case "Isha":r.isha_qaza=q;break; case "Witr":r.witr_qaza=q;break;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            requestWindowFeature(android.view.Window.FEATURE_NO_TITLE);
            getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);
            if (Build.VERSION.SDK_INT >= 21) { getWindow().setStatusBarColor(Color.TRANSPARENT); getWindow().setNavigationBarColor(themeColors[0]); }
            if (getActionBar() != null) getActionBar().hide();
            
            Configuration conf = getResources().getConfiguration();
            if(conf.fontScale != 1.0f) {
                conf.fontScale = 1.0f;
                DisplayMetrics metrics = getResources().getDisplayMetrics();
                WindowManager wm = (WindowManager) getSystemService(android.content.Context.WINDOW_SERVICE);
                wm.getDefaultDisplay().getMetrics(metrics);
                metrics.scaledDensity = conf.fontScale * metrics.density;
                getBaseContext().getResources().updateConfiguration(conf, metrics);
            }
        } catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }

        DENSITY = getResources().getDisplayMetrics().density;
        sp = getSharedPreferences("salah_pro_final", MODE_PRIVATE);
        
        DataMigrationHelper.migrateOldDataToRoom(this);
        sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
        selectedDate[0] = sdf.format(new Date());
        calendarViewPointer = Calendar.getInstance();

        boolean systemDark = (getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;
        isDarkTheme = sp.getBoolean("is_dark_mode", systemDark); 
        activeTheme = sp.getInt("app_theme", 0); 
        String[] themeAccents = {"#00BFA5", "#3B82F6", "#FF9559", "#D81B60", "#A67BFF", "#3BCC75"};
        if (isDarkTheme) {
            themeColors[0] = Color.parseColor("#0A0A0C"); 
            themeColors[1] = Color.parseColor("#1C1C1E");
            themeColors[2] = Color.parseColor("#FFFFFF"); 
            themeColors[3] = Color.parseColor("#A0A0A5"); 
            themeColors[4] = Color.parseColor("#2C2C2E"); 
        } else {
            themeColors[0] = Color.parseColor("#F8FAFC");
            themeColors[1] = Color.parseColor("#FFFFFF"); 
            themeColors[2] = Color.parseColor("#141416"); 
            themeColors[3] = Color.parseColor("#64748B"); 
            themeColors[4] = Color.parseColor("#E2E8F0");
        }
        colorAccent = Color.parseColor(themeAccents[activeTheme]);
        themeColors[5] = Color.argb(40, Color.red(colorAccent), Color.green(colorAccent), Color.blue(colorAccent));
        lang = new LanguageEngine(sp.getString("app_lang", "en"));
        ui = new UIComponents(this, DENSITY, themeColors, lang);
        fbHelper = new FirebaseManager(this, sp);
        root = new FrameLayout(this);
        if (Build.VERSION.SDK_INT >= 17) { root.setLayoutDirection(View.LAYOUT_DIRECTION_LTR);
        }
        ScrollView scrollView = new ScrollView(this); scrollView.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); scrollView.setFillViewport(true); scrollView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        contentArea = new LinearLayout(this); contentArea.setOrientation(LinearLayout.VERTICAL); scrollView.addView(contentArea, new FrameLayout.LayoutParams(-1, -1)); root.addView(scrollView);
        setContentView(root);

        appFonts[0] = Typeface.DEFAULT; appFonts[1] = Typeface.DEFAULT_BOLD;
        try {
            if (sp.getString("app_lang", "en").equals("bn")) { appFonts[0] = Typeface.createFromAsset(getAssets(), "fonts/hind_reg.ttf");
            appFonts[1] = Typeface.createFromAsset(getAssets(), "fonts/hind_bold.ttf"); } 
            else { appFonts[0] = Typeface.createFromAsset(getAssets(), "fonts/poppins_reg.ttf");
            appFonts[1] = Typeface.createFromAsset(getAssets(), "fonts/poppins_bold.ttf"); }
        } catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }
        
        root.getViewTreeObserver().addOnGlobalLayoutListener(new ViewTreeObserver.OnGlobalLayoutListener() { 
            @Override public void onGlobalLayout() { applyFont(root, appFonts[0], appFonts[1]); } 
        });
        Runnable reloadTask = new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); } };
        statsHelper = new StatsHelper(this, DENSITY, themeColors, colorAccent, lang, ui, sp, AppConstants.PRAYERS, appFonts);
        backupHelper = new BackupHelper(this, sp, ui, lang, fbHelper, DENSITY, themeColors, colorAccent, root);
        calHelper = new CalendarHelper(this, DENSITY, themeColors, colorAccent, lang, ui, sp, AppConstants.PRAYERS, selectedDate, calendarViewPointer, reloadTask);
        fbHelper.processOfflineQueue(
            new Runnable() { @Override public void run() { ui.showSmartBanner(root, lang.get("Syncing Data"), lang.get("Connecting to cloud..."), "img_cloud", colorAccent, null); }},
            new Runnable() { @Override public void run() { ui.showSmartBanner(root, lang.get("Sync Complete"), lang.get("Progress updated."), "img_tick", colorAccent, null); loadTodayPage(); refreshWidget(); }},
            new Runnable() { @Override public void run() { ui.hideLoadingBanner(root); }}
        );
        loadTodayPage();
        refreshWidget();
        setupMidnightRefresh();
        MidnightWorker.scheduleNextMidnight(MainActivity.this);
        
        if (sp.getBoolean("is_first_run_tutorial", true)) { 
            new OnboardingHelper(this, DENSITY, themeColors, colorAccent, lang, ui, sp, root, appFonts).showOnboarding();
        }
    }

    private void applyFont(View v, Typeface reg, Typeface bold) {
        if (v instanceof TextView) { 
            TextView tv = (TextView) v;
            if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(bold); 
            else tv.setTypeface(reg); 
        } else if (v instanceof ViewGroup) { 
            ViewGroup vg = (ViewGroup) v;
            for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i), reg, bold);
        }
    }

    private void refreshWidget() {
        try { 
            Intent intent = new Intent(MainActivity.this, com.my.salah.tracker.app.SalahWidget.class);
            intent.setAction(android.appwidget.AppWidgetManager.ACTION_APPWIDGET_UPDATE); 
            int[] ids = android.appwidget.AppWidgetManager.getInstance(MainActivity.this).getAppWidgetIds(new android.content.ComponentName(MainActivity.this, com.my.salah.tracker.app.SalahWidget.class)); 
            intent.putExtra(android.appwidget.AppWidgetManager.EXTRA_APPWIDGET_IDS, ids); 
            sendBroadcast(intent);
        } catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); } 
    }

    private void setupMidnightRefresh() {
        Calendar c = Calendar.getInstance();
        c.add(Calendar.DAY_OF_MONTH, 1); c.set(Calendar.HOUR_OF_DAY, 0); c.set(Calendar.MINUTE, 0); c.set(Calendar.SECOND, 0); c.set(Calendar.MILLISECOND, 500); 
        long delay = c.getTimeInMillis() - System.currentTimeMillis();
        if(delay < 0) delay = 86400000; 
        new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
            @Override public void run() {
                selectedDate[0] = sdf.format(new Date()); 
                calendarViewPointer.setTime(new Date());
                loadTodayPage(); refreshWidget(); setupMidnightRefresh();
        MidnightWorker.scheduleNextMidnight(MainActivity.this); 
            }
        }, delay);
    }

    public int getStatusColor(String k) {
        if(k==null) return themeColors[4]; SalahRecord r = getRoomRecord(k); int d=0, e=0;
        for(String p : AppConstants.PRAYERS){ String s=getFardStat(r, p); if("yes".equals(s)) d++; else if("excused".equals(s)) e++; }
        if(d+e==0) return android.graphics.Color.TRANSPARENT; if(e==6) return android.graphics.Color.parseColor("#8B5CF6");
        return d==6 ? android.graphics.Color.parseColor("#22C55E") : android.graphics.Color.parseColor("#10B981");
    }
    public android.graphics.drawable.Drawable getProgressBorder(String k, boolean s) {
        int c = getStatusColor(k); int d=0; SalahRecord r = getRoomRecord(k);
        for(String p : AppConstants.PRAYERS){ String st=getFardStat(r, p); if("yes".equals(st)||"excused".equals(st)) d++; }
        if(s){ android.graphics.drawable.GradientDrawable gd=new android.graphics.drawable.GradientDrawable(); gd.setShape(android.graphics.drawable.GradientDrawable.OVAL); gd.setColor(colorAccent); return gd; }
        return new UIComponents.ProgressDrawable(d, 6, c==0?themeColors[4]:c, themeColors[4], DENSITY);
    }

    private void loadTodayPage() {
        contentArea.removeAllViews();
        root.setBackgroundColor(themeColors[0]);
        int hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY); 
        final boolean isDayTime = (hour >= 6 && hour < 18); 
        String greetingStr = lang.get("Good Evening");
        if(hour >= 4 && hour < 12) greetingStr = lang.get("Good Morning");
        else if(hour >= 12 && hour < 17) greetingStr = lang.get("Good Afternoon");
        else if(hour >= 17 && hour < 20) greetingStr = lang.get("Good Evening"); else greetingStr = lang.get("Good Night");
        boolean isLandscape = getResources().getConfiguration().orientation == Configuration.ORIENTATION_LANDSCAPE;
        int headPadT = 15; int pCardPadV = 18; int pCardMarB = 10;
        int weekNavPadB = 8; int actionMarB = 10; int cardPadV = 12; int cardMarB = 8;
        SalahRecord todayRec = getRoomRecord(selectedDate[0]);
        LinearLayout header = new LinearLayout(this); header.setOrientation(LinearLayout.HORIZONTAL); header.setGravity(Gravity.CENTER_VERTICAL); header.setPadding((int)(20*DENSITY), (int)(headPadT*DENSITY), (int)(20*DENSITY), (int)(5*DENSITY));
        
        LinearLayout leftHeader = new LinearLayout(this); leftHeader.setOrientation(LinearLayout.VERTICAL);
        leftHeader.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f)); leftHeader.setGravity(Gravity.CENTER_VERTICAL);
        int streakCount = ui.calculateStreak(sp, AppConstants.PRAYERS);
        TextView streakBadge = new TextView(this); streakBadge.setTextSize(11); streakBadge.setTypeface(Typeface.DEFAULT_BOLD);
        streakBadge.setPadding((int)(10*DENSITY), (int)(4*DENSITY), (int)(10*DENSITY), (int)(4*DENSITY));
        GradientDrawable badgeBg = new GradientDrawable(); badgeBg.setCornerRadius(15f * DENSITY); badgeBg.setColor(colorAccent); badgeBg.setStroke(0, android.graphics.Color.TRANSPARENT);
        streakBadge.setTextColor(android.graphics.Color.WHITE);
        streakBadge.setText(streakCount >= 365 ? lang.get("1 YEAR STREAK") : lang.bnNum(streakCount) + " " + lang.get("DAYS STREAK"));
        LinearLayout.LayoutParams badgeLp = new LinearLayout.LayoutParams(-2, -2); badgeLp.setMargins(0, 0, 0, (int)(10*DENSITY)); streakBadge.setLayoutParams(badgeLp); streakBadge.setBackground(badgeBg); leftHeader.addView(streakBadge);
        
        LinearLayout hijriRow = new LinearLayout(this); hijriRow.setOrientation(LinearLayout.HORIZONTAL); hijriRow.setGravity(Gravity.CENTER_VERTICAL);
        View moonImg = ui.getRoundImage("img_moon", 0, Color.TRANSPARENT, themeColors[3]); LinearLayout.LayoutParams mOp = new LinearLayout.LayoutParams((int)(14*DENSITY), (int)(14*DENSITY)); mOp.setMargins(0,0,(int)(6*DENSITY),0); moonImg.setLayoutParams(mOp); hijriRow.addView(moonImg);
        TextView dHijri = new TextView(this); 
        try { dHijri.setText(ui.getHijriDate(sdf.parse(selectedDate[0]), sp.getInt("hijri_offset", 0))); } catch(Exception e) { dHijri.setText("Error Date");
        }
        dHijri.setTextColor(themeColors[3]); dHijri.setTextSize(14); dHijri.setTypeface(Typeface.DEFAULT_BOLD); hijriRow.addView(dHijri);
        LinearLayout.LayoutParams hLp = new LinearLayout.LayoutParams(-2, -2); hLp.setMargins(0,0,0,(int)(2*DENSITY)); hijriRow.setLayoutParams(hLp);
        leftHeader.addView(hijriRow); hijriRow.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { calHelper.showHijri(); } });

        TextView dMain = new TextView(this);
        try { dMain.setText(lang.getGregorian(sdf.parse(selectedDate[0]))); } catch(Exception e) {} 
        dMain.setTextColor(themeColors[2]); dMain.setTextSize(16); dMain.setTypeface(Typeface.DEFAULT_BOLD); leftHeader.addView(dMain);
        dMain.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { calHelper.showGregorian(); }}); 
        
        LinearLayout rightHeader = new LinearLayout(this); rightHeader.setOrientation(LinearLayout.HORIZONTAL); rightHeader.setGravity(Gravity.CENTER_VERTICAL);
        TextView themeToggleBtn = new TextView(this); themeToggleBtn.setText(isDarkTheme ? "🌙" : "☀️"); themeToggleBtn.setGravity(Gravity.CENTER); themeToggleBtn.setTextSize(16);
        GradientDrawable tBg = new GradientDrawable(GradientDrawable.Orientation.BR_TL, isDarkTheme ? new int[]{Color.parseColor("#1A2980"), Color.parseColor("#26D0CE")} : new int[]{Color.parseColor("#FF9500"), Color.parseColor("#FFCC00")}); tBg.setCornerRadius(100f); themeToggleBtn.setBackground(tBg);
        LinearLayout.LayoutParams tLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY)); tLp.setMargins(0,0,(int)(8*DENSITY),0); themeToggleBtn.setLayoutParams(tLp);
        themeToggleBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); finish(); overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out); startActivity(getIntent()); } }); rightHeader.addView(themeToggleBtn);
        View periodBtn = ui.getRoundImage("img_period", 6, themeColors[5], colorAccent); LinearLayout.LayoutParams pLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY)); pLp.setMargins(0,0,(int)(8*DENSITY),0); periodBtn.setLayoutParams(pLp);
        periodBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showExcuseDialog(); } }); rightHeader.addView(periodBtn); 

        View settingsBtn = ui.getRoundImage("img_settings", 6, themeColors[5], colorAccent);
        LinearLayout.LayoutParams sLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY)); settingsBtn.setLayoutParams(sLp);
        settingsBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showSettingsMenu(); } }); rightHeader.addView(settingsBtn); 
        
        header.addView(leftHeader); header.addView(rightHeader); contentArea.addView(header);
        LinearLayout pCard = new LinearLayout(this); pCard.setPadding((int)(20*DENSITY), (int)(pCardPadV*DENSITY), (int)(20*DENSITY), (int)(pCardPadV*DENSITY)); LinearLayout.LayoutParams pcLp = new LinearLayout.LayoutParams(-1, -2); pcLp.setMargins((int)(20*DENSITY), 0, (int)(20*DENSITY), (int)(pCardMarB*DENSITY)); pCard.setLayoutParams(pcLp);
        pCard.setOrientation(LinearLayout.HORIZONTAL); pCard.setGravity(Gravity.CENTER_VERTICAL);
        int[] pColors = isDayTime ? new int[]{Color.parseColor("#FF9500"), Color.parseColor("#FFCC00")} : new int[]{Color.parseColor("#1A2980"), Color.parseColor("#26D0CE")};
        GradientDrawable pcBg = new GradientDrawable(GradientDrawable.Orientation.BR_TL, pColors);
        pcBg.setCornerRadius(20f * DENSITY); pCard.setBackground(pcBg);
        
        int countCompleted = 0; 
        for(String p : AppConstants.PRAYERS) {
            String status = getFardStat(todayRec, p);
            if(status.equals("yes") || status.equals("excused")) countCompleted++;
        }
        String[] statusMsgs = {lang.get("Start your journey"), lang.get("Great start!"), lang.get("Keep going"), lang.get("Halfway there!"), lang.get("Almost done!"), lang.get("Almost done!"), lang.get("Purity Achieved!")};
        LinearLayout left = new LinearLayout(this); left.setOrientation(LinearLayout.VERTICAL); left.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1.2f)); 
        TextView gText = new TextView(this); gText.setText(greetingStr); gText.setTextColor(Color.WHITE); gText.setTextSize(14); gText.setTypeface(Typeface.DEFAULT_BOLD); gText.setAlpha(0.9f);
        TextView pT = new TextView(this); pT.setText(lang.bnNum(countCompleted*100/6) + "%"); pT.setTextColor(Color.WHITE); pT.setTextSize(36); pT.setTypeface(Typeface.DEFAULT_BOLD); 
        TextView subBtm = new TextView(this); subBtm.setText(statusMsgs[countCompleted]); subBtm.setTextColor(Color.WHITE); subBtm.setTextSize(12); subBtm.setAlpha(0.9f);
        left.addView(gText); left.addView(pT); left.addView(subBtm);
        TextView artDisplay = new TextView(this); artDisplay.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 0.8f)); artDisplay.setGravity(Gravity.RIGHT | Gravity.CENTER_VERTICAL); artDisplay.setTextSize(40);
        artDisplay.setText(isDayTime ? "☀️" : "🌙"); 
        pCard.addView(left); pCard.addView(artDisplay); contentArea.addView(pCard);

        final Calendar now = Calendar.getInstance(); final Calendar[] selectedCalArr = { Calendar.getInstance() };
        try { selectedCalArr[0].setTime(sdf.parse(selectedDate[0])); } catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }
        LinearLayout weekNavBox = new LinearLayout(this); weekNavBox.setGravity(Gravity.CENTER_VERTICAL);
        weekNavBox.setPadding((int)(15*DENSITY), (int)(5*DENSITY), (int)(15*DENSITY), (int)(weekNavPadB*DENSITY));
        TextView prevW = new TextView(this); prevW.setText("❮"); prevW.setTextSize(16); prevW.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(6*DENSITY)); prevW.setTextColor(themeColors[2]); prevW.setGravity(Gravity.CENTER);
        GradientDrawable navBg = new GradientDrawable(); navBg.setColor(themeColors[1]); navBg.setCornerRadius(12f * DENSITY); navBg.setStroke((int)(1.5f*DENSITY), themeColors[4]); prevW.setBackground(navBg);
        prevW.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { Calendar chk = (Calendar) selectedCalArr[0].clone(); chk.add(Calendar.DATE, -7); if(chk.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { selectedCalArr[0].add(Calendar.DATE, -7); selectedDate[0] = sdf.format(selectedCalArr[0].getTime()); loadTodayPage(); } else { ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } } });
        LinearLayout weekBox = new LinearLayout(this); weekBox.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f)); weekBox.setGravity(Gravity.CENTER);
        Calendar cal = (Calendar) selectedCalArr[0].clone();
        while (cal.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) { cal.add(Calendar.DATE, -1); }
        int circleSize = (int)(36 * DENSITY);
        SalahDao dDao = SalahDatabase.getDatabase(this).salahDao();
        for(int i=0; i<7; i++) {
            final String dKey = sdf.format(cal.getTime()); final boolean isTooOld = cal.get(Calendar.YEAR) < now.get(Calendar.YEAR) - 100;
            final boolean isSel = dKey.equals(selectedDate[0]); final boolean isFuture = cal.after(now);
            String dLabel = new SimpleDateFormat("EEEE", Locale.US).format(cal.getTime()).substring(0,1);
            if (sp.getString("app_lang", "en").equals("bn")) { String[] bnD = {"র", "সো", "ম", "বু", "বৃ", "শু", "শ"}; dLabel = bnD[cal.get(Calendar.DAY_OF_WEEK) - 1];
            }
            
            SalahRecord dRec = dDao.getRecordByDate(dKey);
            boolean isAllDone = true; 
            for(String p : AppConstants.PRAYERS) { 
                String s = getFardStat(dRec, p);
                if(!s.equals("yes") && !s.equals("excused")) { isAllDone = false; break; } 
            }
            
            FrameLayout cell = new FrameLayout(this);
            cell.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
            TextView t = new TextView(this); t.setText(dLabel); t.setTypeface(Typeface.DEFAULT_BOLD); t.setTextSize(13); t.setGravity(Gravity.CENTER); FrameLayout.LayoutParams textLp = new FrameLayout.LayoutParams(circleSize, circleSize);
            textLp.gravity = Gravity.CENTER; t.setLayoutParams(textLp);
            t.setTextColor(isSel ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : themeColors[3]));
            t.setBackground(getProgressBorder(dKey, isSel));
            cell.addView(t);
            cell.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { if(isFuture) { ui.showPremiumLocked(colorAccent); } else if(isTooOld) { ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } else { selectedDate[0] = dKey; loadTodayPage(); } } });
            weekBox.addView(cell); cal.add(Calendar.DATE, 1);
        }
        
        TextView nextW = new TextView(this);
        nextW.setText("❯"); nextW.setTextSize(16); nextW.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(6*DENSITY)); nextW.setTextColor(themeColors[2]); nextW.setGravity(Gravity.CENTER); nextW.setBackground(navBg); 
        Calendar weekStartNow = (Calendar) now.clone();
        while (weekStartNow.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) { weekStartNow.add(Calendar.DATE, -1); }
        final boolean isCurrentWeekArr = !selectedCalArr[0].before(weekStartNow);
        nextW.setAlpha(isCurrentWeekArr ? 0.3f : 1.0f);
        nextW.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { if(!isCurrentWeekArr) { selectedCalArr[0].add(Calendar.DATE, 7); if(selectedCalArr[0].after(Calendar.getInstance())) { selectedCalArr[0].setTime(Calendar.getInstance().getTime()); } selectedDate[0] = sdf.format(selectedCalArr[0].getTime()); loadTodayPage(); } } });
        weekNavBox.addView(prevW); weekNavBox.addView(weekBox); weekNavBox.addView(nextW); contentArea.addView(weekNavBox);

        LinearLayout actionRow = new LinearLayout(this); actionRow.setOrientation(LinearLayout.HORIZONTAL); actionRow.setGravity(Gravity.CENTER); actionRow.setPadding((int)(20*DENSITY), 0, (int)(20*DENSITY), (int)(actionMarB*DENSITY)); actionRow.setWeightSum(2);
        LinearLayout markAllBtn = new LinearLayout(this); markAllBtn.setGravity(Gravity.CENTER); markAllBtn.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY)); LinearLayout.LayoutParams markLp = new LinearLayout.LayoutParams(0, -2, 1f);
        markLp.setMargins(0, 0, (int)(6*DENSITY), 0); markAllBtn.setLayoutParams(markLp); 
        TextView markAllTxt = new TextView(this); markAllTxt.setTextSize(13); markAllTxt.setTypeface(Typeface.DEFAULT_BOLD); 
        GradientDrawable bg1 = new GradientDrawable(); bg1.setCornerRadius(20f * DENSITY);
        bg1.setColor(themeColors[1]); bg1.setStroke((int)(1.5f*DENSITY), themeColors[4]); markAllBtn.setBackground(bg1); 
        
        if (countCompleted < 6) {
            markAllTxt.setText(lang.get("Mark All"));
            markAllTxt.setTextColor(themeColors[2]); 
            View mIcon = ui.getRoundImage("img_tick", 4, Color.TRANSPARENT, colorAccent); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); icLp.setMargins(0,0,(int)(8*DENSITY),0); mIcon.setLayoutParams(icLp); markAllBtn.addView(mIcon); markAllBtn.addView(markAllTxt);
            markAllBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showMarkOptions(); } });
            markAllBtn.setOnLongClickListener(new View.OnLongClickListener() { @Override public boolean onLongClick(View v) { 
                v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(String p : AppConstants.PRAYERS) { 
                    setQazaStat(r, p, true); setFardStat(r, p, "no");
                    sp.edit().putBoolean(selectedDate[0]+"_"+p+"_qaza", true).putString(selectedDate[0]+"_"+p, "no").apply(); 
                    fbHelper.save(selectedDate[0], p, "no"); 
                } 
                updateRoomRecord(r);
                ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null); loadTodayPage(); refreshWidget(); 
                return true; 
            } });
        } else {
            markAllTxt.setText(lang.get("All Done")); markAllTxt.setTextColor(themeColors[2]);
            View mIcon = ui.getRoundImage("img_trophy", 4, Color.TRANSPARENT, colorAccent); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); icLp.setMargins(0,0,(int)(8*DENSITY),0); mIcon.setLayoutParams(icLp); markAllBtn.addView(mIcon); markAllBtn.addView(markAllTxt);
            markAllBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showUnmarkOptions(); } });
            markAllBtn.setOnLongClickListener(new View.OnLongClickListener() { @Override public boolean onLongClick(View v) { 
                v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(String p : AppConstants.PRAYERS) { 
                    setQazaStat(r, p, true); setFardStat(r, p, "no");
                    sp.edit().putBoolean(selectedDate[0]+"_"+p+"_qaza", true).putString(selectedDate[0]+"_"+p, "no").apply(); 
                    fbHelper.save(selectedDate[0], p, "no"); 
                } 
                updateRoomRecord(r);
                ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null); loadTodayPage(); refreshWidget(); 
                return true; 
            } });
        }
        actionRow.addView(markAllBtn);

        LinearLayout todayBtn = new LinearLayout(this); todayBtn.setGravity(Gravity.CENTER); todayBtn.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
        LinearLayout.LayoutParams todayLp = new LinearLayout.LayoutParams(0, -2, 1f); todayLp.setMargins((int)(6*DENSITY), 0, 0, 0); todayBtn.setLayoutParams(todayLp); 
        TextView todayTxt = new TextView(this); todayTxt.setTextSize(13); todayTxt.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable bg2 = new GradientDrawable(); bg2.setCornerRadius(20f * DENSITY); bg2.setColor(themeColors[1]); bg2.setStroke((int)(1.5f*DENSITY), themeColors[4]); todayBtn.setBackground(bg2); 
        View tIcon = ui.getRoundImage("img_calender", 4, Color.TRANSPARENT, colorAccent);
        LinearLayout.LayoutParams tIcLp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); tIcLp.setMargins(0,0,(int)(8*DENSITY),0); tIcon.setLayoutParams(tIcLp);
        todayTxt.setTextColor(themeColors[2]); 
        if(!selectedDate[0].equals(sdf.format(new Date()))) { todayTxt.setText(lang.get("Today"));
            todayBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { selectedDate[0] = sdf.format(new Date()); selectedCalArr[0].setTime(new Date()); calendarViewPointer.setTime(new Date()); loadTodayPage(); } });
        } 
        else { todayTxt.setText(lang.get("This Week"));
            todayBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); } statsHelper.showStats(true); } });
        }
        todayBtn.addView(tIcon); todayBtn.addView(todayTxt); actionRow.addView(todayBtn); 
        contentArea.addView(actionRow);

        LinearLayout cardsContainer = new LinearLayout(this);
        cardsContainer.setOrientation(isLandscape ? LinearLayout.HORIZONTAL : LinearLayout.VERTICAL); 
        cardsContainer.setLayoutParams(new LinearLayout.LayoutParams(-1, 0, 1f)); 
        cardsContainer.setPadding((int)(20*DENSITY), 0, (int)(20*DENSITY), (int)(30*DENSITY));
        
        LinearLayout col1 = null, col2 = null;
        if(isLandscape) {
            col1 = new LinearLayout(this); col1.setOrientation(LinearLayout.VERTICAL);
            col1.setLayoutParams(new LinearLayout.LayoutParams(0, -1, 1f)); col1.setPadding(0,0,(int)(8*DENSITY),0); col1.setWeightSum(3f);
            col2 = new LinearLayout(this); col2.setOrientation(LinearLayout.VERTICAL); col2.setLayoutParams(new LinearLayout.LayoutParams(0, -1, 1f)); col2.setPadding((int)(8*DENSITY),0,0,0); col2.setWeightSum(3f);
            cardsContainer.addView(col1); cardsContainer.addView(col2);
        } else {
            cardsContainer.setWeightSum(6f);
        }
        
        String[] pImgs = {"img_fajr", "img_dhuhr", "img_asr", "img_maghrib", "img_isha", "img_witr"};
        int[] pPaddings = {8, 8, 8, 0, 8, 8}; 
        
        for(int i=0; i<6; i++) {
            final String name = AppConstants.PRAYERS[i];
            final String key = selectedDate[0]+"_"+name; 
            final String stat = getFardStat(todayRec, name); final boolean checked = stat.equals("yes") || stat.equals("excused");
            final boolean isQaza = getQazaStat(todayRec, name);
            
            LinearLayout card = new LinearLayout(this); card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)(cardPadV*DENSITY)); card.setGravity(Gravity.CENTER_VERTICAL);
            GradientDrawable cb = new GradientDrawable(); 
            if (stat.equals("excused")) { cb.setColor(isDarkTheme ? Color.parseColor("#1A1115") : Color.parseColor("#FCE4EC")); cb.setStroke((int)(1.5f*DENSITY), Color.parseColor("#FF4081"));
            } 
            else { cb.setColor(themeColors[1]);
            cb.setStroke((int)(1.5f*DENSITY), checked? colorAccent : themeColors[4]); }
            cb.setCornerRadius(25f * DENSITY);
            card.setBackground(cb); 
            
            LinearLayout.LayoutParams cLp = new LinearLayout.LayoutParams(-1, 0, 1f); 
            cLp.setMargins(0, 0, 0, i==5 ? 0 : (int)(cardMarB*DENSITY)); 
            card.setLayoutParams(cLp);
            View iconView = ui.getRoundImage(pImgs[i], pPaddings[i], android.graphics.Color.TRANSPARENT, colorAccent); 
            LinearLayout.LayoutParams icCardLp = new LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY)); 
            icCardLp.setMargins(0,0,(int)(15*DENSITY),0); iconView.setLayoutParams(icCardLp); card.addView(iconView);
            LinearLayout textContainer = new LinearLayout(this); textContainer.setOrientation(LinearLayout.VERTICAL); textContainer.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
            LinearLayout titleRow = new LinearLayout(this); titleRow.setOrientation(LinearLayout.HORIZONTAL); titleRow.setGravity(Gravity.CENTER_VERTICAL);
            TextView tv = new TextView(this); tv.setText(lang.get(name)); tv.setTextColor(stat.equals("excused") ? Color.parseColor("#FF4081") : themeColors[2]); tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setTextSize(16); tv.setSingleLine(true); titleRow.addView(tv);
            if (isQaza && stat.equals("no")) {
                TextView qBadge = new TextView(this);
                qBadge.setText(lang.get("QAZA")); qBadge.setTextColor(themeColors[2]); qBadge.setTextSize(10); qBadge.setTypeface(Typeface.DEFAULT_BOLD); qBadge.setPadding((int)(8*DENSITY), (int)(3*DENSITY), (int)(8*DENSITY), (int)(3*DENSITY)); GradientDrawable qBg = new GradientDrawable(); qBg.setColor(themeColors[5]); qBg.setCornerRadius(10f*DENSITY); qBadge.setBackground(qBg);
                LinearLayout.LayoutParams qLp = new LinearLayout.LayoutParams(-2, -2); qLp.setMargins((int)(10*DENSITY), 0, 0, 0); qBadge.setLayoutParams(qLp); titleRow.addView(qBadge);
            }
            textContainer.addView(titleRow); card.addView(textContainer);
            
            final int finalI = i;
            if (AppConstants.SUNNAHS[i].length > 0 && !stat.equals("excused")) {
                TextView sunnahBtn = new TextView(this);
                int doneSunnahs = 0; for(String sName : AppConstants.SUNNAHS[i]) { if (sp.getString(selectedDate[0]+"_"+name+"_Sunnah_"+sName, "no").equals("yes")) doneSunnahs++;
                }
                String sText = AppConstants.SUNNAHS[i].length > 1 ?
                (lang.get("Extras") + " (" + lang.bnNum(doneSunnahs) + "/" + lang.bnNum(AppConstants.SUNNAHS[i].length) + ")") : (i == 5 ? lang.get("Tahajjud") : lang.get("Sunnah"));
                sunnahBtn.setText(sText); sunnahBtn.setTextSize(11); sunnahBtn.setSingleLine(true);
                GradientDrawable customSunnahBg = new GradientDrawable(); customSunnahBg.setCornerRadius(12f*DENSITY); if(doneSunnahs > 0){customSunnahBg.setColor(colorAccent);sunnahBtn.setTextColor(android.graphics.Color.WHITE);}else{customSunnahBg.setColor(themeColors[5]);sunnahBtn.setTextColor(themeColors[2]);} 
                sunnahBtn.setPadding((int)(10*DENSITY), (int)(5*DENSITY), (int)(10*DENSITY), (int)(5*DENSITY));
                sunnahBtn.setBackground(customSunnahBg); LinearLayout.LayoutParams customSunnahLp = new LinearLayout.LayoutParams(-2, -2); customSunnahLp.setMargins(0, 0, (int)(15*DENSITY), 0); sunnahBtn.setLayoutParams(customSunnahLp);
                sunnahBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showSunnahDialog(name, AppConstants.SUNNAHS[finalI]); } }); card.addView(sunnahBtn);
            }
            
            final View chk = ui.getPremiumCheckbox(stat, colorAccent);
            card.addView(chk);
            card.setOnClickListener(new View.OnClickListener() { 
                @Override public void onClick(final View v) {
                    if (stat.equals("excused")) { 
                        SalahRecord r = getRoomRecord(selectedDate[0]); setFardStat(r, name, "no"); updateRoomRecord(r);
                        sp.edit().putString(key, "no").apply(); fbHelper.save(selectedDate[0], name, "no"); loadTodayPage(); refreshWidget(); return; 
                    }
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); 
                    boolean currentStatus = stat.equals("yes"); String newVal = !currentStatus ? "yes" : "no"; 
                    
                    SalahRecord r = getRoomRecord(selectedDate[0]);
                    if(newVal.equals("yes") && getQazaStat(r, name)) { setQazaStat(r, name, false); sp.edit().putBoolean(key+"_qaza", false).apply(); }
                    setFardStat(r, name, newVal); updateRoomRecord(r);
                    sp.edit().putString(key, newVal).apply(); fbHelper.save(selectedDate[0], name, newVal); 
                    
                    v.animate().scaleX(0.95f).scaleY(0.95f).alpha(0.8f).setDuration(100).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(250).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); } }).start();
                    if (!currentStatus) { 
                        int count = 0;
                        for(String p : AppConstants.PRAYERS) { String s = getFardStat(r, p); if(s.equals("yes") || s.equals("excused")) count++;
                        } 
                        if (count == 6) { showSuccessSequence();
                        } 
                    }
                    v.postDelayed(new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); }}, 150);
                }
            });
            card.setOnLongClickListener(new View.OnLongClickListener() {
                @Override public boolean onLongClick(View v) {
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); 
                    SalahRecord r = getRoomRecord(selectedDate[0]);
                    boolean wasQaza = getQazaStat(r, name);
                    if(!wasQaza) { 
                        setQazaStat(r, name, true); setFardStat(r, name, "no"); updateRoomRecord(r);
                        sp.edit().putBoolean(key+"_qaza", true).putString(key, "no").apply(); fbHelper.save(selectedDate[0], name, "no"); 
                        ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null); 
                    } 
                    else { 
                        setQazaStat(r, name, false); updateRoomRecord(r);
                        sp.edit().putBoolean(key+"_qaza", false).apply(); 
                        ui.showSmartBanner(root, lang.get("Qaza Removed"), lang.get("Name removed from Qaza list."), "img_tick", colorAccent, null);
                    }
                    loadTodayPage();
                    refreshWidget(); return true;
                }
            });
            if(isLandscape) { if(i<3) col1.addView(card);
            else col2.addView(card); } else cardsContainer.addView(card);
        }
        contentArea.addView(cardsContainer); 
        if(appFonts[0] != null) applyFont(root, appFonts[0], appFonts[1]);
    }

    private void showExcuseDialog() { 
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); 
        LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); 
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(30f * DENSITY); main.setBackground(gd); 
        View iconView = ui.getRoundImage("img_period", 12, Color.parseColor(isDarkTheme ? "#331520" : "#FCE4EC"), Color.parseColor("#D81B60"));
        LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(55*DENSITY), (int)(55*DENSITY)); icLp.gravity = Gravity.CENTER_HORIZONTAL; iconView.setLayoutParams(icLp); main.addView(iconView); 
        TextView title = new TextView(this); title.setText(lang.get("Excused Mode")); title.setTextColor(colorAccent); title.setTextSize(20);
        title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0, (int)(15*DENSITY), 0, (int)(10*DENSITY)); main.addView(title); 
        
        SalahRecord todayRec = getRoomRecord(selectedDate[0]);
        boolean isAlreadyExcused = true;
        for(String p : AppConstants.PRAYERS) { if(!getFardStat(todayRec, p).equals("excused")) { isAlreadyExcused = false; break;
        } } 
        
        TextView sub = new TextView(this);
        sub.setText(lang.get(isAlreadyExcused ? "Prayers are currently marked as excused." : "Mark today's prayers as excused. Streak will not break.")); sub.setGravity(Gravity.CENTER); sub.setTextColor(themeColors[3]);
        sub.setTextSize(12); sub.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(sub); 
        Button actionBtn = new Button(this);
        actionBtn.setText(lang.get(isAlreadyExcused ? "Remove Excused Status" : "Mark Today as Excused")); actionBtn.setAllCaps(false); actionBtn.setTextColor(Color.WHITE); actionBtn.setTypeface(Typeface.DEFAULT_BOLD); 
        GradientDrawable btnBg = new GradientDrawable(); btnBg.setColor(colorAccent);
        btnBg.setCornerRadius(20f * DENSITY); actionBtn.setBackground(btnBg); 
        LinearLayout.LayoutParams btnLp = new LinearLayout.LayoutParams(-1, (int)(50*DENSITY)); main.addView(actionBtn, btnLp); 
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2);
        flp.gravity = Gravity.CENTER; wrap.addView(main, flp); 
        
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(Gravity.CENTER); 
        
        final boolean finalIsExcused = isAlreadyExcused;
        actionBtn.setOnClickListener(new View.OnClickListener() { 
            @Override public void onClick(View v) { 
                String newVal = finalIsExcused ? "no" : "excused"; 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(String p : AppConstants.PRAYERS) { 
                    setFardStat(r, p, newVal);
                    sp.edit().putString(selectedDate[0]+"_"+p, newVal).apply(); 
                    fbHelper.save(selectedDate[0], p, newVal); 
                } 
                updateRoomRecord(r);
                ad.dismiss(); loadTodayPage(); refreshWidget(); 
            } 
        });
        applyFont(main, appFonts[0], appFonts[1]); ad.show(); 
    }

    private void showSunnahDialog(final String prayer, final String[] sunnahList) { 
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); TextView title = new TextView(this); title.setText(lang.get(prayer) + " " + lang.get("Extras")); title.setTextColor(colorAccent); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        for(int s=0; s<sunnahList.length; s++) { final String sName = sunnahList[s];
        final String sKey = selectedDate[0] + "_" + prayer + "_Sunnah_" + sName; final boolean sChecked = sp.getString(sKey, "no").equals("yes");
        final LinearLayout row = new LinearLayout(this); row.setOrientation(LinearLayout.HORIZONTAL); row.setGravity(Gravity.CENTER_VERTICAL); row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); LinearLayout.LayoutParams rowLp = new LinearLayout.LayoutParams(-1, -2);
        rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp); final GradientDrawable rowBg = new GradientDrawable(); rowBg.setCornerRadius(15f*DENSITY); rowBg.setColor(sChecked ? themeColors[4] : Color.TRANSPARENT); row.setBackground(rowBg);
        final TextView tv = new TextView(this); tv.setText(lang.get(sName)); tv.setTextColor(sChecked ? colorAccent : themeColors[2]); tv.setTextSize(16); tv.setTypeface(sChecked ? Typeface.DEFAULT_BOLD : Typeface.DEFAULT);
        tv.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f)); final View chk = ui.getPremiumCheckbox(sChecked ? "yes" : "no", colorAccent); row.addView(tv); row.addView(chk); main.addView(row);
        row.setOnClickListener(new View.OnClickListener() { @Override public void onClick(final View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); boolean cur = sp.getString(sKey, "no").equals("yes"); boolean newVal = !cur; sp.edit().putString(sKey, newVal ? "yes" : "no").apply(); fbHelper.save(selectedDate[0], prayer + "_Sunnah_" + sName, newVal ? "yes" : "no"); TextView t = (TextView) chk; GradientDrawable bg = (GradientDrawable) t.getBackground(); if(newVal) { bg.setColor(colorAccent); bg.setStroke(0, Color.TRANSPARENT); t.setText("✓"); t.setTextColor(Color.WHITE); rowBg.setColor(themeColors[4]); tv.setTextColor(colorAccent); tv.setTypeface(Typeface.DEFAULT_BOLD); } else { bg.setColor(Color.TRANSPARENT); bg.setStroke((int)(2*DENSITY), themeColors[4]); t.setText(""); rowBg.setColor(Color.TRANSPARENT); tv.setTextColor(themeColors[2]); tv.setTypeface(Typeface.DEFAULT); } } });
        } 
        TextView closeBtn = new TextView(this); closeBtn.setText(lang.get("Done")); closeBtn.setTextColor(Color.WHITE); closeBtn.setGravity(Gravity.CENTER); closeBtn.setTypeface(Typeface.DEFAULT_BOLD);
        closeBtn.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY)); GradientDrawable cBg = new GradientDrawable(); cBg.setColor(colorAccent); cBg.setCornerRadius(20f*DENSITY); closeBtn.setBackground(cBg); LinearLayout.LayoutParams clp = new LinearLayout.LayoutParams(-1, -2);
        clp.setMargins(0, (int)(15*DENSITY), 0, 0); closeBtn.setLayoutParams(clp); main.addView(closeBtn); FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(Gravity.CENTER); 
        
        closeBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); loadTodayPage(); refreshWidget(); } });
        applyFont(main, appFonts[0], appFonts[1]); ad.show(); 
    }

    private void showSettingsMenu() {
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout mainLayout = new LinearLayout(this); mainLayout.setOrientation(LinearLayout.VERTICAL); mainLayout.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); mainLayout.setBackground(gd);
        TextView title = new TextView(this); title.setText(lang.get("Settings & Options")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); mainLayout.addView(title);
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER); 

        class MenuRow {
            void addImg(String titleStr, String imgName, final Runnable action) {
                LinearLayout btn = new LinearLayout(MainActivity.this);
                btn.setOrientation(LinearLayout.HORIZONTAL); btn.setGravity(Gravity.CENTER_VERTICAL); btn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg);
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2);
                lp.setMargins(0, 0, 0, (int)(10*DENSITY)); btn.setLayoutParams(lp);
                View icon = ui.getRoundImage(imgName, 0, Color.TRANSPARENT, colorAccent); 
                LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(28*DENSITY), (int)(28*DENSITY)); icLp.setMargins(0,0,(int)(15*DENSITY),0); icon.setLayoutParams(icLp);
                btn.addView(icon);
                TextView t1 = new TextView(MainActivity.this); t1.setText(lang.get(titleStr)); t1.setTextColor(themeColors[2]); t1.setTextSize(16); t1.setTypeface(Typeface.DEFAULT_BOLD); btn.addView(t1);
                btn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); action.run(); } }); mainLayout.addView(btn);
            }
        }
        MenuRow mr = new MenuRow();
        mr.addImg("Choose Theme", "img_theme", new Runnable() { @Override public void run() { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); recreate(); }});
        mr.addImg("Change Language", "img_lang", new Runnable() { @Override public void run() { String nextL = sp.getString("app_lang", "en").equals("en") ? "bn" : "en"; sp.edit().putString("app_lang", nextL).apply(); recreate(); }});
        mr.addImg("Backup & Sync", "img_cloud", new Runnable() { @Override public void run() { backupHelper.showProfileDialog(new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); }}); }});
        mr.addImg("View Qaza List", "img_custom_qaza", new Runnable() { @Override public void run() { showQazaListDialog(); }});
        mr.addImg("Advanced Statistics", "img_stats", new Runnable() { @Override public void run() { try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); } statsHelper.showStatsOptionsDialog(); }});

        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2);
        flp.gravity = Gravity.CENTER; wrap.addView(mainLayout, flp);
        applyFont(mainLayout, appFonts[0], appFonts[1]); ad.show();
    }

    private void showQazaListDialog() {
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding(0, (int)(30*DENSITY), 0, (int)(30*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        TextView title = new TextView(this); title.setText(lang.get("View Qaza List")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0, 0, 0, (int)(20*DENSITY));
        main.addView(title);
        
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER); 
        
        ScrollView scroll = new ScrollView(this); final LinearLayout list = new LinearLayout(this);
        list.setOrientation(LinearLayout.VERTICAL); list.setPadding((int)(20*DENSITY), 0, (int)(20*DENSITY), 0);
        Calendar cal = Calendar.getInstance(); int qazaCount = 0;
        
        SalahDao dao = SalahDatabase.getDatabase(this).salahDao();
        for(int i=0; i<365; i++) { 
            final String dK = sdf.format(cal.getTime());
            final SalahRecord r = dao.getRecordByDate(dK);
            
            if (r != null) {
                for(final String p : AppConstants.PRAYERS) {
                    if(getQazaStat(r, p) && getFardStat(r, p).equals("no")) {
                        qazaCount++;
                        final LinearLayout row = new LinearLayout(this); row.setOrientation(LinearLayout.HORIZONTAL); row.setGravity(Gravity.CENTER_VERTICAL); row.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                        GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); row.setBackground(bg);
                        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2); lp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(lp);
                        LinearLayout tLay = new LinearLayout(this); tLay.setOrientation(LinearLayout.VERTICAL);
                        tLay.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
                        TextView t1 = new TextView(this); t1.setText(lang.get(p)); t1.setTextColor(themeColors[2]); t1.setTextSize(16); t1.setTypeface(Typeface.DEFAULT_BOLD);
                        TextView t2 = new TextView(this); t2.setText(lang.getShortGreg(cal.getTime())); t2.setTextColor(themeColors[3]);
                        t2.setTextSize(12);
                        tLay.addView(t1); tLay.addView(t2); row.addView(tLay);
                        TextView btn = new TextView(this); btn.setText(lang.get("Done")); btn.setTextColor(colorAccent); btn.setTypeface(Typeface.DEFAULT_BOLD); btn.setPadding((int)(15*DENSITY), (int)(8*DENSITY), (int)(15*DENSITY), (int)(8*DENSITY));
                        GradientDrawable bBg = new GradientDrawable(); bBg.setColor(themeColors[5]); bBg.setCornerRadius(10f*DENSITY); btn.setBackground(bBg); row.addView(btn);
                        btn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { 
                            setQazaStat(r, p, false); setFardStat(r, p, "yes"); updateRoomRecord(r);
                            sp.edit().putBoolean(dK+"_"+p+"_qaza", false).putString(dK+"_"+p, "yes").apply(); 
                            list.removeView(row); loadTodayPage(); refreshWidget(); 
                        } });
                        list.addView(row);
                    }
                }
            }
            cal.add(Calendar.DATE, -1);
        }
        
        if(qazaCount == 0) { 
            View customEmptyIcon = ui.getRoundImage("img_empty_qaza", 0, android.graphics.Color.TRANSPARENT, 0); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(80*DENSITY), (int)(80*DENSITY)); icLp.gravity = Gravity.CENTER; icLp.setMargins(0, (int)(20*DENSITY), 0, (int)(10*DENSITY)); customEmptyIcon.setLayoutParams(icLp); list.addView(customEmptyIcon);
            TextView empty = new TextView(this); empty.setText(lang.get("Alhamdulillah! No pending Qaza.")); empty.setTextColor(themeColors[3]); empty.setGravity(Gravity.CENTER);
            empty.setPadding(0, 0, 0, (int)(20*DENSITY)); list.addView(empty); 
        }
        
        scroll.addView(list);
        main.addView(scroll, new LinearLayout.LayoutParams(-1, (int)(300*DENSITY)));
        TextView closeBtn = new TextView(this); closeBtn.setText(lang.get("CLOSE")); closeBtn.setTextColor(themeColors[3]); closeBtn.setGravity(Gravity.CENTER); closeBtn.setTypeface(Typeface.DEFAULT_BOLD); closeBtn.setPadding(0, (int)(20*DENSITY), 0, 0); main.addView(closeBtn);
        closeBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); } });
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2);
        flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        applyFont(main, appFonts[0], appFonts[1]); ad.show();
    }

    private void showMarkOptions() {
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); TextView title = new TextView(this); title.setText(lang.get("Mark Options")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
        TextView t1 = new TextView(this); t1.setText(lang.get("Fard Only (6 Prayers)")); t1.setTextColor(themeColors[2]); t1.setTextSize(16); t1.setGravity(Gravity.CENTER); t1.setTypeface(Typeface.DEFAULT_BOLD); t1.setPadding((int)(15*DENSITY), (int)(20*DENSITY), (int)(15*DENSITY), (int)(20*DENSITY));
        GradientDrawable b1 = new GradientDrawable(); b1.setColor(themeColors[4]); b1.setCornerRadius(15f*DENSITY); t1.setBackground(b1); main.addView(t1); 
        TextView t2 = new TextView(this); t2.setText(lang.get("Include All Sunnahs")); t2.setTextColor(themeColors[2]); t2.setTextSize(16); t2.setGravity(Gravity.CENTER);
        t2.setTypeface(Typeface.DEFAULT_BOLD); t2.setPadding((int)(15*DENSITY), (int)(20*DENSITY), (int)(15*DENSITY), (int)(20*DENSITY)); LinearLayout.LayoutParams lp2 = new LinearLayout.LayoutParams(-1, -2); lp2.setMargins(0, (int)(10*DENSITY), 0, 0); t2.setLayoutParams(lp2);
        GradientDrawable b2 = new GradientDrawable(); b2.setColor(themeColors[4]); b2.setCornerRadius(15f*DENSITY); t2.setBackground(b2); main.addView(t2); 
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(Gravity.CENTER); 
        
        t1.setOnClickListener(new View.OnClickListener() { 
            @Override public void onClick(View v) { 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(String p : AppConstants.PRAYERS) { 
                    setFardStat(r, p, "yes");
                    sp.edit().putString(selectedDate[0]+"_"+p, "yes").apply(); 
                    fbHelper.save(selectedDate[0], p, "yes"); 
                } 
                updateRoomRecord(r);
                ad.dismiss(); loadTodayPage(); refreshWidget(); 
                showSuccessSequence(); // ✨ ফিক্স: মাশাআল্লাহ যুক্ত করা হলো
            } 
        });
        t2.setOnClickListener(new View.OnClickListener() { 
            @Override public void onClick(View v) { 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(int i=0; i<AppConstants.PRAYERS.length; i++) { 
                    setFardStat(r, AppConstants.PRAYERS[i], "yes");
                    sp.edit().putString(selectedDate[0]+"_"+AppConstants.PRAYERS[i], "yes").apply(); fbHelper.save(selectedDate[0], AppConstants.PRAYERS[i], "yes"); 
                    for(String sName : AppConstants.SUNNAHS[i]) { sp.edit().putString(selectedDate[0]+"_"+AppConstants.PRAYERS[i]+"_Sunnah_"+sName, "yes").apply(); fbHelper.save(selectedDate[0], AppConstants.PRAYERS[i]+"_Sunnah_"+sName, "yes"); } 
                } 
                updateRoomRecord(r);
                ad.dismiss(); loadTodayPage(); refreshWidget(); 
                showSuccessSequence(); // ✨ ফিক্স: মাশাআল্লাহ যুক্ত করা হলো
            } 
        });
        applyFont(main, appFonts[0], appFonts[1]); ad.show();
    }

    private void showUnmarkOptions() {
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); TextView title = new TextView(this); title.setText(lang.get("Unmark Options")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
        TextView t1 = new TextView(this); t1.setText(lang.get("Remove Fard Only")); t1.setTextColor(themeColors[2]); t1.setTextSize(16); t1.setGravity(Gravity.CENTER); t1.setTypeface(Typeface.DEFAULT_BOLD); t1.setPadding((int)(15*DENSITY), (int)(20*DENSITY), (int)(15*DENSITY), (int)(20*DENSITY));
        GradientDrawable b1 = new GradientDrawable(); b1.setColor(themeColors[4]); b1.setCornerRadius(15f*DENSITY); t1.setBackground(b1); main.addView(t1); 
        TextView t2 = new TextView(this); t2.setText(lang.get("Remove All (Inc. Sunnah)")); t2.setTextColor(Color.parseColor("#FF5252")); t2.setTextSize(16);
        t2.setGravity(Gravity.CENTER); t2.setTypeface(Typeface.DEFAULT_BOLD); t2.setPadding((int)(15*DENSITY), (int)(20*DENSITY), (int)(15*DENSITY), (int)(20*DENSITY)); LinearLayout.LayoutParams lp2 = new LinearLayout.LayoutParams(-1, -2); lp2.setMargins(0, (int)(10*DENSITY), 0, 0); t2.setLayoutParams(lp2);
        GradientDrawable b2 = new GradientDrawable(); b2.setColor(themeColors[4]); b2.setCornerRadius(15f*DENSITY); t2.setBackground(b2); main.addView(t2); 
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(Gravity.CENTER); 
        
        t1.setOnClickListener(new View.OnClickListener() { 
            @Override public void onClick(View v) { 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(String p : AppConstants.PRAYERS) { 
                    setFardStat(r, p, "no");
                    sp.edit().putString(selectedDate[0]+"_"+p, "no").apply(); 
                    fbHelper.save(selectedDate[0], p, "no"); 
                } 
                updateRoomRecord(r);
                ad.dismiss(); loadTodayPage(); refreshWidget(); 
            } 
        });
        t2.setOnClickListener(new View.OnClickListener() { 
            @Override public void onClick(View v) { 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(int i=0; i<AppConstants.PRAYERS.length; i++) { 
                    setFardStat(r, AppConstants.PRAYERS[i], "no");
                    sp.edit().putString(selectedDate[0]+"_"+AppConstants.PRAYERS[i], "no").apply(); fbHelper.save(selectedDate[0], AppConstants.PRAYERS[i], "no"); 
                    for(String sName : AppConstants.SUNNAHS[i]) { sp.edit().putString(selectedDate[0]+"_"+AppConstants.PRAYERS[i]+"_Sunnah_"+sName, "no").apply(); fbHelper.save(selectedDate[0], AppConstants.PRAYERS[i]+"_Sunnah_"+sName, "no"); } 
                } 
                updateRoomRecord(r);
                ad.dismiss(); loadTodayPage(); refreshWidget(); 
            } 
        }); applyFont(main, appFonts[0], appFonts[1]); ad.show();
    }

    private void showSuccessSequence() { 
        final LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL); main.setGravity(Gravity.CENTER); main.setPadding((int)(30*DENSITY), (int)(45*DENSITY), (int)(30*DENSITY), (int)(45*DENSITY)); 
        GradientDrawable gd = new GradientDrawable(); gd.setColor(colorAccent); gd.setCornerRadius(30f * DENSITY); main.setBackground(gd); 
        if(Build.VERSION.SDK_INT >= 21) main.setElevation(50f);
        TextView iconView = new TextView(this); iconView.setText("💎"); iconView.setTextSize(60); iconView.setGravity(Gravity.CENTER); iconView.setPadding(0, 0, 0, (int)(10*DENSITY)); main.addView(iconView); 
        TextView title = new TextView(this); title.setText(lang.get("Mashallah!")); title.setTextColor(Color.WHITE);
        title.setTextSize(26); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0, 0, 0, (int)(8*DENSITY)); 
        
        String timeContext = selectedDate[0].equals(sdf.format(new Date())) ? "today" : "for this day";
        TextView msg = new TextView(this); 
        msg.setText(lang.get(timeContext.equals("today") ? "You've completed all prayers today.\nMay Allah accept it." : "You've completed all prayers for this day.\nMay Allah accept it."));
        msg.setTextColor(Color.parseColor("#F0F0F0")); msg.setGravity(Gravity.CENTER); 
        if (Build.VERSION.SDK_INT >= 17) msg.setTextAlignment(View.TEXT_ALIGNMENT_CENTER); msg.setTextSize(14); msg.setLineSpacing(0, 1.2f); 
        
        main.addView(title); main.addView(msg); 
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2);
        flp.gravity = Gravity.CENTER; root.addView(main, flp); 
        
        main.setScaleX(0.5f); main.setScaleY(0.5f); main.setAlpha(0f); 
        main.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(300).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); 
        
        android.animation.ObjectAnimator scaleX = android.animation.ObjectAnimator.ofFloat(iconView, "scaleX", 1f, 1.15f, 1f);
        android.animation.ObjectAnimator scaleY = android.animation.ObjectAnimator.ofFloat(iconView, "scaleY", 1f, 1.15f, 1f); 
        scaleX.setRepeatCount(android.animation.ValueAnimator.INFINITE); scaleY.setRepeatCount(android.animation.ValueAnimator.INFINITE); 
        scaleX.setDuration(1000); scaleY.setDuration(1000); 
        android.animation.AnimatorSet animSet = new android.animation.AnimatorSet(); animSet.playTogether(scaleX, scaleY); animSet.start();
        new Handler().postDelayed(new Runnable() { @Override public void run() { main.animate().scaleX(0.8f).scaleY(0.8f).alpha(0f).setDuration(200).withEndAction(new Runnable() { @Override public void run() { root.removeView(main); } }).start(); } }, 2000);
        applyFont(main, appFonts[0], appFonts[1]); 
    }
}