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

    
    public static String getBnDateStr(String dateStr, android.content.SharedPreferences sp) {
        try {
            String[] p = dateStr.split("-"); int y = Integer.parseInt(p[0]), m = Integer.parseInt(p[1]), d = Integer.parseInt(p[2]);
            int bY = y - 593, bM = 0, bD = 0; boolean isLeap = (y%4==0 && y%100!=0)||(y%400==0);
            if (m==4 && d>=14) {bM=0; bD=d-13;} else if(m==4) {bM=11; bD=d+17; bY--;}
            else if (m==5 && d<=14) {bM=0; bD=d+17;} else if(m==5) {bM=1; bD=d-14;}
            else if (m==6 && d<=14) {bM=1; bD=d+17;} else if(m==6) {bM=2; bD=d-14;}
            else if (m==7 && d<=15) {bM=2; bD=d+16;} else if(m==7) {bM=3; bD=d-15;}
            else if (m==8 && d<=15) {bM=3; bD=d+16;} else if(m==8) {bM=4; bD=d-15;}
            else if (m==9 && d<=15) {bM=4; bD=d+16;} else if(m==9) {bM=5; bD=d-15;}
            else if (m==10 && d<=15) {bM=5; bD=d+15;} else if(m==10) {bM=6; bD=d-15;}
            else if (m==11 && d<=14) {bM=6; bD=d+16;} else if(m==11) {bM=7; bD=d-14;}
            else if (m==12 && d<=14) {bM=7; bD=d+16;} else if(m==12) {bM=8; bD=d-14;}
            else if (m==1 && d<=13) {bM=8; bD=d+17; bY--;} else if(m==1) {bM=9; bD=d-13; bY--;}
            else if (m==2 && d<=12) {bM=9; bD=d+18; bY--;} else if(m==2) {bM=10; bD=d-12; bY--;}
            else if (m==3 && d<=14) {bM=10; bD=d+(isLeap?17:16); bY--;} else if(m==3) {bM=11; bD=d-14; bY--;}
            bD += sp.getInt("bn_date_offset", 0);
            boolean isBn = sp.getString("app_lang", "en").equals("bn");
            String[] bMs = isBn ? new String[]{"বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"} : new String[]{"Boishakh", "Joistho", "Ashar", "Srabon", "Bhadro", "Ashwin", "Kartik", "Agrahayon", "Poush", "Magh", "Falgun", "Choitro"};
            
            String suf = "";
            if (!isBn) {
                if (bD >= 11 && bD <= 13) suf = "th";
                else switch (bD % 10) { case 1: suf="st"; break; case 2: suf="nd"; break; case 3: suf="rd"; break; default: suf="th"; }
            } else {
                if(bD == 1) suf = "লা"; else if(bD == 2 || bD == 3) suf = "রা"; else if(bD == 4) suf = "ঠা"; else if(bD >= 5 && bD <= 18) suf = "ই"; else if(bD >= 19 && bD <= 31) suf = "এ"; else suf = "শে";
            }

            String dayStr = String.valueOf(bD), yearStr = String.valueOf(bY);
            if(isBn) {
                dayStr = dayStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
                yearStr = yearStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
            }
            return dayStr + suf + " " + bMs[bM] + ", " + yearStr;
        } catch(Exception e) { return ""; }
    }

    private String tBn(String s) {
        if(s == null) return "";
        if(!getSharedPreferences("salah_pro_final", 0).getString("app_lang", "en").equals("bn")) return s;
        return s.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯")
                .replace("Saturday","শনিবার").replace("Sunday","রবিবার").replace("Monday","সোমবার").replace("Tuesday","মঙ্গলবার").replace("Wednesday","বুধবার").replace("Thursday","বৃহস্পতিবার").replace("Friday","শুক্রবার")
                .replace("Jan","জানু").replace("Feb","ফেব্রু").replace("Mar","মার্চ").replace("Apr","এপ্রিল").replace("May","মে").replace("Jun","জুন").replace("Jul","জুল").replace("Aug","আগস্ট").replace("Sep","সেপ্টে").replace("Oct","অক্টো").replace("Nov","নভে").replace("Dec","ডিসে");
    }

    
    
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

    private void applyNeo(android.view.View v, int type, float radius, float elev, int bgColor, boolean isDark) {
        soup.neumorphism.NeumorphShapeAppearanceModel model = new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, radius * DENSITY).build();
        soup.neumorphism.NeumorphShapeDrawable d = new soup.neumorphism.NeumorphShapeDrawable(v.getContext());
        d.setShapeAppearanceModel(model);
        d.setShapeType(type);

        if (type == 1 && !isDark && bgColor != colorAccent) {
            bgColor = android.graphics.Color.parseColor("#E2E8F0"); // গর্তের ভেতরটা হালকা ছাই
            d.setShadowColorDark(android.graphics.Color.parseColor("#A0AEC0")); // গাঢ় ছায়া
            d.setShadowColorLight(android.graphics.Color.parseColor("#FFFFFF"));
            elev = elev * 1.5f; // গর্তের গভীরতা বাড়ানো
        }

        d.setShadowColorLight(isDark ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
        d.setShadowColorDark(isDark ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        d.setShadowElevation(elev * DENSITY);
        d.setFillColor(android.content.res.ColorStateList.valueOf(bgColor));
        v.setBackground(d);
        
        // ছায়াকে বাইরে ছড়িয়ে পড়ার পারমিশন দেওয়া হচ্ছে
        v.post(() -> {
            android.view.ViewParent p1 = v.getParent();
            if (p1 instanceof android.view.ViewGroup) {
                ((android.view.ViewGroup) p1).setClipChildren(false);
                ((android.view.ViewGroup) p1).setClipToPadding(false);
                android.view.ViewParent p2 = p1.getParent();
                if (p2 instanceof android.view.ViewGroup) {
                    ((android.view.ViewGroup) p2).setClipChildren(false);
                    ((android.view.ViewGroup) p2).setClipToPadding(false);
                }
            }
        });
    }


    private View getNeoCheckbox(String status, int accentColor) {
        boolean isChk = status.equals("yes") || status.equals("excused");
        soup.neumorphism.NeumorphCardView nd = new soup.neumorphism.NeumorphCardView(this);
        int size = (int)(52 * DENSITY);
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams(size, size);
        nd.setLayoutParams(lp);
        nd.setShapeType(isChk ? 0 : 1);
        nd.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
        nd.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        nd.setShadowElevation((isChk ? 2f : 5.5f) * DENSITY);
        nd.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 26f*DENSITY).build());
        nd.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
        nd.setPadding((int)(14*DENSITY), (int)(14*DENSITY), (int)(14*DENSITY), (int)(14*DENSITY));
        
        if(isChk) {
            TextView inner = new TextView(this);
            inner.setText(status.equals("yes") ? "✓" : "🌸");
            inner.setTextColor(accentColor);
            inner.setTextSize(18);
            inner.setTypeface(null, Typeface.BOLD);
            inner.setGravity(Gravity.CENTER);
            FrameLayout.LayoutParams ilp = new FrameLayout.LayoutParams(-1, -1);
            inner.setLayoutParams(ilp);
            nd.addView(inner);
        }
        return nd;
    }

    public android.graphics.drawable.Drawable getUltra3D(int surfaceColor, int shadowColor, float radius, float depthDp) {
    float d = getResources().getDisplayMetrics().density;
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(surfaceColor); surface.setCornerRadius(radius);
    surface.setStroke((int)(1.0f * d), shadowColor); // চারদিকে সূক্ষ্ম আউটলাইন
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
    int offX = (int)((depthDp/2.0f) * d); int offY = (int)(depthDp * d); // সামান্য কোণাকুণি (Isometric) ছায়া
    ld.setLayerInset(0, offX, offY, 0, 0); ld.setLayerInset(1, 0, 0, offX, offY); return ld;
}
    public android.graphics.drawable.Drawable getPremium3D(int c1, float r, float dp, boolean isDark, int accent) {
    float d = getResources().getDisplayMetrics().density;
    int shadow;
    int red = android.graphics.Color.red(accent); int grn = android.graphics.Color.green(accent); int blu = android.graphics.Color.blue(accent);
    if (isDark) { shadow = android.graphics.Color.rgb((int)(red*0.4f), (int)(grn*0.4f), (int)(blu*0.4f)); } 
    else { shadow = android.graphics.Color.argb(80, red, grn, blu); }
    
    android.graphics.drawable.GradientDrawable sh = new android.graphics.drawable.GradientDrawable(); sh.setColor(shadow); sh.setCornerRadius(r);
    android.graphics.drawable.GradientDrawable su = new android.graphics.drawable.GradientDrawable(); su.setColor(c1); su.setCornerRadius(r);
    su.setStroke((int)(1.5f * d), shadow); // সব দিকে মোটা বর্ডার
    
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{sh, su});
    int ox = (int)((dp/1.5f) * d); int oy = (int)(dp * d);
    ld.setLayerInset(0, ox, oy, 0, 0); ld.setLayerInset(1, 0, 0, ox, oy); return ld;
}
    public android.graphics.drawable.Drawable getSafe3D(int c1, int c2, float r, float dp) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.GradientDrawable sh = new android.graphics.drawable.GradientDrawable(); sh.setColor(c2); sh.setCornerRadius(r);
        android.graphics.drawable.GradientDrawable su = new android.graphics.drawable.GradientDrawable(); su.setColor(c1); su.setCornerRadius(r);
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{sh, su});
        int o = (int)(dp * d); ld.setLayerInset(0, 0, o, 0, 0); ld.setLayerInset(1, 0, 0, 0, o); return ld;
    }

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

    @Override protected void onResume() { super.onResume(); if(sp!=null && !sp.getString("user_email", "").isEmpty() && sp.getString("offline_q", "").isEmpty()) { fbHelper.fetchAndLoad(null, new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); } }, null); } }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            requestWindowFeature(android.view.Window.FEATURE_NO_TITLE);
            getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | (!isDarkTheme && Build.VERSION.SDK_INT >= 23 ? View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR : 0));
            if (Build.VERSION.SDK_INT >= 21) { getWindow().setStatusBarColor((!isDarkTheme && Build.VERSION.SDK_INT < 23) ? android.graphics.Color.parseColor("#40000000") : android.graphics.Color.TRANSPARENT); getWindow().setNavigationBarColor(themeColors[0]); }
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

        long savedDate = getIntent().getLongExtra("RESTORE_DATE", -1L);
        if(savedDate != -1L) {
            selectedDate[0] = sdf.format(new java.util.Date(savedDate));
            calendarViewPointer.setTimeInMillis(savedDate);
        }


        boolean systemDark = (getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;
        isDarkTheme = sp.getBoolean("is_dark_mode", systemDark); 
        activeTheme = sp.getInt("app_theme", 0); 
        String[] themeAccents = {"#00BFA5", "#3B82F6", "#FF9559", "#D81B60", "#A67BFF", "#3BCC75"};
        if (isDarkTheme) {
            themeColors[0] = Color.parseColor("#1C1C1E"); 
            themeColors[1] = Color.parseColor("#1C1C1E");
            themeColors[2] = Color.parseColor("#FFFFFF"); 
            themeColors[3] = Color.parseColor("#A0A0A5"); 
            themeColors[4] = Color.parseColor("#2C2C2E"); 
        } else {
            themeColors[0] = Color.parseColor("#E2E8F0");
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
        setRequestedOrientation(android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT); setContentView(root);

        


        


        // --- INVINCIBLE DYNAMIC SCANNER ---
        getWindow().getDecorView().post(new Runnable() {
            @Override
            public void run() {
                try {
                    android.view.View decor = getWindow().getDecorView();
                    java.util.Stack<android.view.View> stack = new java.util.Stack<>();
                    stack.push(decor);
                    android.view.ViewGroup percentCard = null;
                    android.view.View prevArrow = null;
                    android.view.View nextArrow = null;
                    
                    while(!stack.isEmpty()) {
                        android.view.View v = stack.pop();
                        if(v instanceof android.widget.TextView) {
                            String txt = ((android.widget.TextView)v).getText().toString();
                            if(txt.contains("%")) {
                                android.view.ViewParent p1 = v.getParent();
                                if(p1 != null && p1.getParent() instanceof soup.neumorphism.NeumorphCardView) {
                                    percentCard = (android.view.ViewGroup) p1.getParent();
                                }
                            }
                            if(txt.equals("<") || txt.equals("❮")) {
                                if(v.getParent() instanceof soup.neumorphism.NeumorphCardView) prevArrow = (android.view.View) v.getParent();
                            }
                            if(txt.equals(">") || txt.equals("❯")) {
                                if(v.getParent() instanceof soup.neumorphism.NeumorphCardView) nextArrow = (android.view.View) v.getParent();
                            }
                        }
                        if(v instanceof android.view.ViewGroup) {
                            android.view.ViewGroup vg = (android.view.ViewGroup) v;
                            for(int i=0; i<vg.getChildCount(); i++) stack.push(vg.getChildAt(i));
                        }
                    }
                    
                    float den = getResources().getDisplayMetrics().density;
                    
                    if(prevArrow != null) {
                        android.view.ViewGroup.LayoutParams lp = prevArrow.getLayoutParams();
                        lp.width = (int)(52 * den); lp.height = (int)(52 * den);
                        prevArrow.setLayoutParams(lp);
                    }
                    if(nextArrow != null) {
                        android.view.ViewGroup.LayoutParams lp = nextArrow.getLayoutParams();
                        lp.width = (int)(52 * den); lp.height = (int)(52 * den);
                        nextArrow.setLayoutParams(lp);
                    }
                    
                    if(false && percentCard != null) {
                        percentCard.setTag("waved");
                        android.view.ViewGroup parent = (android.view.ViewGroup) percentCard.getParent();
                        if(parent != null) {
                            int index = parent.indexOfChild(percentCard);
                            parent.removeView(percentCard);
                            
                            soup.neumorphism.NeumorphCardView waveContainer = new soup.neumorphism.NeumorphCardView(percentCard.getContext());
                            waveContainer.setLayoutParams(percentCard.getLayoutParams());
                            waveContainer.setShapeType(0);
                            waveContainer.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
                            waveContainer.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
                            waveContainer.setShadowElevation(6f * den);
                            waveContainer.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 20f * den).build());
                            waveContainer.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
                            
                            android.widget.FrameLayout innerBox = new android.widget.FrameLayout(percentCard.getContext());
                            WaterWaveView wave = new WaterWaveView(percentCard.getContext());
                            
                            int p = 50;
                            java.util.Stack<android.view.View> pStack = new java.util.Stack<>(); pStack.push(percentCard);
                            while(!pStack.isEmpty()) {
                                android.view.View v = pStack.pop();
                                if(v instanceof android.widget.TextView) {
                                    String txt = ((android.widget.TextView)v).getText().toString();
                                    if(txt.contains("%")) p = Integer.parseInt(txt.replaceAll("[^0-9]", ""));
                                } else if (v instanceof android.view.ViewGroup) {
                                    android.view.ViewGroup vg = (android.view.ViewGroup) v;
                                    for(int i=0; i<vg.getChildCount(); i++) pStack.push(vg.getChildAt(i));
                                }
                            }
                            wave.setProgressAndColor(p, colorAccent);
                            innerBox.addView(wave, new android.widget.FrameLayout.LayoutParams(-1, -1));
                            
                            percentCard.setBackgroundColor(android.graphics.Color.TRANSPARENT);
                            percentCard.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                            innerBox.addView(percentCard);
                            
                            android.widget.FrameLayout.LayoutParams nlp = new android.widget.FrameLayout.LayoutParams(-1, -1);
                            nlp.setMargins((int)(4*den), (int)(4*den), (int)(4*den), (int)(4*den));
                            waveContainer.addView(innerBox, nlp);
                            
                            innerBox.setOutlineProvider(new android.view.ViewOutlineProvider() {
                                @Override public void getOutline(android.view.View view, android.graphics.Outline outline) { outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), 16f * den); }
                            });
                            innerBox.setClipToOutline(true);
                            
                            parent.addView(waveContainer, index);
                        }
                    }
                } catch(Exception e){}
            }
        });
    


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

    
    private void updateLivePercentage(String dK) {
        try {
            int nC = 0; 
            SalahRecord currR = SalahDatabase.getDatabase(this).salahDao().getRecordByDate(dK);
            if(currR != null) {
                for(String pr : AppConstants.PRAYERS) { 
                    String s = getFardStat(currR, pr); 
                    if(s.equals("yes") || s.equals("excused")) nC++; 
                }
            }
            TextView pT = getWindow().getDecorView().findViewWithTag("PERCENT_TEXT");
            TextView subBtm = getWindow().getDecorView().findViewWithTag("SUB_TEXT");
            if(pT != null) pT.setText(lang.bnNum(nC*100/6) + "%");
            String[] statusMsgs = {lang.get("Start your journey"), lang.get("Great start!"), lang.get("Keep going"), lang.get("Good progress!"), lang.get("Almost done!"), lang.get("Just one more!"), lang.get("Purity Achieved!")}; if(subBtm != null) subBtm.setText(statusMsgs[nC]);
        } catch(Exception e){}
    }

    private void loadTodayPage() {
        final int savedScrollPos = contentArea.getParent() instanceof ScrollView ? ((ScrollView)contentArea.getParent()).getScrollY() : 0;
        contentArea.removeAllViews();
        contentArea.post(new Runnable() { @Override public void run() { if (contentArea.getParent() instanceof ScrollView) ((ScrollView)contentArea.getParent()).scrollTo(0, savedScrollPos); } });
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
        // === NEW HEADER LAYOUT START ===
        android.widget.LinearLayout header = new android.widget.LinearLayout(this); 
        header.setOrientation(android.widget.LinearLayout.HORIZONTAL); 
        header.setGravity(android.view.Gravity.CENTER_VERTICAL); 
        header.setPadding((int)(20*DENSITY), (int)(headPadT*DENSITY), (int)(20*DENSITY), (int)(10*DENSITY));
        
        android.widget.LinearLayout leftHeader = new android.widget.LinearLayout(this); 
        leftHeader.setOrientation(android.widget.LinearLayout.VERTICAL);
        leftHeader.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); 
        leftHeader.setGravity(android.view.Gravity.CENTER_VERTICAL);
        
        android.widget.LinearLayout hRow = new android.widget.LinearLayout(this);
        hRow.setOrientation(android.widget.LinearLayout.HORIZONTAL); hRow.setGravity(android.view.Gravity.CENTER_VERTICAL);
        android.view.View moon = ui.getRoundImage("img_moon", 0, android.graphics.Color.TRANSPARENT, themeColors[3]);
        android.widget.LinearLayout.LayoutParams mLp = new android.widget.LinearLayout.LayoutParams((int)(14*DENSITY), (int)(14*DENSITY)); mLp.setMargins(0,0,(int)(6*DENSITY),0);
        moon.setLayoutParams(mLp); hRow.addView(moon);
        android.widget.TextView dHijri = new android.widget.TextView(this); 
        try { dHijri.setText(ui.getHijriDate(sdf.parse(selectedDate[0]), sp.getInt("hijri_offset", 0))); } catch(Exception e) {}
        dHijri.setTextColor(themeColors[2]); dHijri.setTextSize(14); dHijri.setTypeface(appFonts[1], android.graphics.Typeface.BOLD); 
        hRow.addView(dHijri); leftHeader.addView(hRow);
        hRow.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showHijri(); } });

        android.widget.TextView dBn = new android.widget.TextView(this);
        try { dBn.setText(getBnDateStr(selectedDate[0], sp)); } catch(Exception e) {}
        dBn.setTextColor(colorAccent); dBn.setTextSize(15); dBn.setTypeface(appFonts[0], android.graphics.Typeface.BOLD);
        dBn.setPadding(0, (int)(4*DENSITY), 0, (int)(2*DENSITY));
        leftHeader.addView(dBn);
        dBn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showGregorian(); }}); 

        android.widget.TextView dEn = new android.widget.TextView(this);
        try { dEn.setText(lang.getGregorian(sdf.parse(selectedDate[0]))); } catch(Exception e) {} 
        dEn.setTextColor(themeColors[3]); dEn.setTextSize(12); dEn.setTypeface(appFonts[0], android.graphics.Typeface.NORMAL); 
        leftHeader.addView(dEn);
        dEn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showGregorian(); }}); 
        
        android.widget.LinearLayout rightHeader = new android.widget.LinearLayout(this); 
        rightHeader.setOrientation(android.widget.LinearLayout.HORIZONTAL); 
        rightHeader.setGravity(android.view.Gravity.END | android.view.Gravity.CENTER_VERTICAL);
        
        int streakCount = ui.calculateStreak(sp, AppConstants.PRAYERS);
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        
        android.widget.TextView stBadge = new android.widget.TextView(this); 
        stBadge.setTextSize(12); stBadge.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        stBadge.setTextColor(colorAccent);
        stBadge.setText(streakCount >= 365 ? (isBn ? "১ বছর" : "1 YEAR") : (isBn ? lang.bnNum(streakCount) + " দিন" : streakCount + " DAYS"));
        applyNeo(stBadge, 0, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); 
        stBadge.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY)); 
        android.widget.LinearLayout.LayoutParams badgeLp = new android.widget.LinearLayout.LayoutParams(-2, -2); 
        badgeLp.setMargins(0, 0, (int)(10*DENSITY), 0); 
        rightHeader.addView(stBadge, badgeLp);

        android.view.View periodBtn = ui.getRoundImage("img_period", 6, android.graphics.Color.TRANSPARENT, colorAccent); applyNeo(periodBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); android.widget.LinearLayout.LayoutParams pLp = new android.widget.LinearLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY)); pLp.setMargins(0,0,(int)(8*DENSITY),0); periodBtn.setLayoutParams(pLp); periodBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showExcuseDialog(); } }); rightHeader.addView(periodBtn); 
        android.view.View settingsBtn = ui.getRoundImage("img_settings", 6, android.graphics.Color.TRANSPARENT, colorAccent); applyNeo(settingsBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); android.widget.LinearLayout.LayoutParams sLp = new android.widget.LinearLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY)); settingsBtn.setLayoutParams(sLp); settingsBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showSettingsMenu(); } }); rightHeader.addView(settingsBtn);
        
        header.addView(leftHeader); header.addView(rightHeader); contentArea.addView(header);
        // === NEW HEADER LAYOUT END ===
        LinearLayout pCard = new LinearLayout(this); pCard.setPadding((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY)); LinearLayout.LayoutParams pcLp = new LinearLayout.LayoutParams(-1, -2); pcLp.setMargins((int)(20*DENSITY), 0, (int)(20*DENSITY), (int)(pCardMarB*DENSITY)); pCard.setLayoutParams(pcLp);
        pCard.setOrientation(LinearLayout.HORIZONTAL); pCard.setGravity(Gravity.CENTER_VERTICAL);
        int[] pColors = isDayTime ? new int[]{Color.parseColor("#FF9500"), Color.parseColor("#FFCC00")} : new int[]{Color.parseColor("#1A2980"), Color.parseColor("#26D0CE")};
         // --- 💎 Glassmorphism Effect Applied Here ---
        int baseR = android.graphics.Color.red(colorAccent);
        int baseG = android.graphics.Color.green(colorAccent);
        int baseB = android.graphics.Color.blue(colorAccent);
        
        android.graphics.drawable.GradientDrawable glassGradient = new android.graphics.drawable.GradientDrawable(
            android.graphics.drawable.GradientDrawable.Orientation.TL_BR,
            new int[]{
                android.graphics.Color.argb(220, baseR, baseG, baseB),
                android.graphics.Color.argb(120, baseR, baseG, baseB),
                android.graphics.Color.argb(190, baseR, baseG, baseB)
            }
        );
        glassGradient.setCornerRadius(20f * DENSITY);
        glassGradient.setStroke((int)(1.5f * DENSITY), android.graphics.Color.argb(150, 255, 255, 255));
        
        pCard.setBackground(glassGradient);
        
        soup.neumorphism.NeumorphCardView pNeo = new soup.neumorphism.NeumorphCardView(this);
        pNeo.setShapeType(0);
        pNeo.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#FFFFFF"));
        pNeo.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        pNeo.setShadowElevation(8f * DENSITY);
        pNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 20f*DENSITY).build());
        pNeo.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
        
        LinearLayout.LayoutParams pNeoLp = new LinearLayout.LayoutParams(-1, -2);
        pNeoLp.setMargins((int)(10*DENSITY), 0, (int)(10*DENSITY), (int)(4*DENSITY));
        pNeo.setLayoutParams(pNeoLp);
        pCard.setLayoutParams(new FrameLayout.LayoutParams(-1, -2));
        pNeo.addView(pCard);
        pCard.setPadding((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));
        
        int countCompleted = 0; 
        for(String p : AppConstants.PRAYERS) {
            String status = getFardStat(todayRec, p);
            if(status.equals("yes") || status.equals("excused")) countCompleted++;
        }
        String[] statusMsgs = {lang.get("Start your journey"), lang.get("Great start!"), lang.get("Keep going"), lang.get("Good progress!"), lang.get("Almost done!"), lang.get("Just one more!"), lang.get("Purity Achieved!")};
        LinearLayout left = new LinearLayout(this); left.setOrientation(LinearLayout.VERTICAL); left.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1.2f)); 
        TextView gText = new TextView(this); gText.setText(greetingStr); gText.setTextColor(android.graphics.Color.WHITE); gText.setTextSize(14); gText.setTypeface(Typeface.DEFAULT_BOLD);
        
        TextView pT = new TextView(this); pT.setText(lang.bnNum(countCompleted*100/6) + "%"); pT.setTag("PERCENT_TEXT"); pT.setTextColor(android.graphics.Color.WHITE); pT.setTextSize(36); pT.setTypeface(Typeface.DEFAULT_BOLD); 
        TextView subBtm = new TextView(this); subBtm.setText(statusMsgs[countCompleted]);
subBtm.setTag("SUB_TEXT"); subBtm.setTextColor(android.graphics.Color.WHITE); subBtm.setTextSize(12); subBtm.setAlpha(0.9f);
        left.addView(gText); left.addView(pT); left.addView(subBtm);
        PremiumTasbihView tasbihView = new PremiumTasbihView(this, isDarkTheme, colorAccent);
        tasbihView.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 0.8f));
        // লাইট থিমের জন্য ব্রাইট গ্রেডিয়েন্ট (ডার্ক থিমে হাত দেওয়া হয়নি, অরিজিনাল থাকবে)
        if (!isDarkTheme) {
            int r = android.graphics.Color.red(colorAccent);
            int g = android.graphics.Color.green(colorAccent);
            int b = android.graphics.Color.blue(colorAccent);
            
            int color1 = android.graphics.Color.rgb((int)(r * 0.9), (int)(g * 0.9), (int)(b * 0.9)); 
            int color2 = android.graphics.Color.rgb((int)(r * 0.75), (int)(g * 0.75), (int)(b * 0.75)); 
            
            android.graphics.drawable.GradientDrawable niceBg = new android.graphics.drawable.GradientDrawable(
                android.graphics.drawable.GradientDrawable.Orientation.TL_BR, 
                new int[]{color1, color2}
            );
            niceBg.setCornerRadius(30f); 
            pCard.setBackground(niceBg);
            
            try {
                for(int i=0; i<left.getChildCount(); i++) {
                    android.view.View v = left.getChildAt(i);
                    if(v instanceof android.widget.TextView) {
                        ((android.widget.TextView)v).setTextColor(android.graphics.Color.WHITE);
                    } else if (v instanceof android.widget.LinearLayout) {
                        android.widget.LinearLayout ll = (android.widget.LinearLayout) v;
                        for(int j=0; j<ll.getChildCount(); j++) {
                            android.view.View innerV = ll.getChildAt(j);
                            if(innerV instanceof android.widget.TextView) {
                                ((android.widget.TextView)innerV).setTextColor(android.graphics.Color.WHITE);
                            }
                        }
                    }
                }
            } catch (Exception e){}
        }
        // ডার্ক থিমের কোনো কোড নেই, তাই আপনার আগের অরিজিনাল ডিজাইনটাই শো করবে!
        pCard.addView(left); 
        pCard.addView(tasbihView); 
        contentArea.addView(pNeo);

        final Calendar now = Calendar.getInstance(); final Calendar[] selectedCalArr = { Calendar.getInstance() };
        try { selectedCalArr[0].setTime(sdf.parse(selectedDate[0])); } catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }
        LinearLayout weekNavBox = new LinearLayout(this); weekNavBox.setGravity(Gravity.CENTER_VERTICAL);
        weekNavBox.setPadding((int)(15*DENSITY), 0, (int)(15*DENSITY), 0);
        TextView prevW = new TextView(this); prevW.setText("❮"); prevW.setTextSize(16); prevW.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(6*DENSITY)); prevW.setTextColor(themeColors[2]); prevW.setGravity(Gravity.CENTER);
        GradientDrawable navBg = new GradientDrawable(); navBg.setColor(themeColors[1]); navBg.setCornerRadius(12f * DENSITY); navBg.setStroke((int)(1.5f*DENSITY), themeColors[4]); applyNeo(prevW, 1, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
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
            
            soup.neumorphism.NeumorphCardView neoW = new soup.neumorphism.NeumorphCardView(this);
            neoW.setShapeType(1); // 100% Guaranteed Sunken Effect for all
            neoW.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
            neoW.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
            neoW.setShadowElevation(6f * DENSITY);
            neoW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 26f * DENSITY).build());
            neoW.setBackgroundColor(isSel ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")));
            neoW.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY));
            
            FrameLayout.LayoutParams nLp = new FrameLayout.LayoutParams((int)(52 * DENSITY), (int)(52 * DENSITY));
            nLp.gravity = Gravity.CENTER;
            neoW.setLayoutParams(nLp);
            
            TextView t = new TextView(this); t.setText(dLabel); t.setTypeface(Typeface.DEFAULT_BOLD); t.setTextSize(13); t.setGravity(Gravity.CENTER);
            // Fix: Future dates are now a visible grey color (#94A3B8) instead of blending into background
            t.setTextColor(isSel ? android.graphics.Color.parseColor("#F1F5F9") : (isFuture ? android.graphics.Color.parseColor("#94A3B8") : themeColors[3]));
            
            neoW.addView(t, new FrameLayout.LayoutParams(-1, -1));
            cell.addView(neoW);
            cell.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { if(isFuture) { ui.showPremiumLocked(colorAccent); } else if(isTooOld) { ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } else { selectedDate[0] = dKey; loadTodayPage(); } } });
            weekBox.addView(cell); cal.add(Calendar.DATE, 1);
        }
        
        TextView nextW = new TextView(this);
        nextW.setText("❯"); nextW.setTextSize(16); nextW.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(6*DENSITY)); nextW.setTextColor(themeColors[2]); nextW.setGravity(Gravity.CENTER); applyNeo(nextW, 1, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); 
        Calendar weekStartNow = (Calendar) now.clone();
        while (weekStartNow.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) { weekStartNow.add(Calendar.DATE, -1); }
        final boolean isCurrentWeekArr = !selectedCalArr[0].before(weekStartNow);
        nextW.setAlpha(isCurrentWeekArr ? 0.3f : 1.0f);
        nextW.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { if(!isCurrentWeekArr) { selectedCalArr[0].add(Calendar.DATE, 7); if(selectedCalArr[0].after(Calendar.getInstance())) { selectedCalArr[0].setTime(Calendar.getInstance().getTime()); } selectedDate[0] = sdf.format(selectedCalArr[0].getTime()); loadTodayPage(); } } });
        prevW.setLayoutParams(new LinearLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY))); prevW.setPadding(5, 2, 5, 2); prevW.setGravity(android.view.Gravity.CENTER);
        nextW.setLayoutParams(new LinearLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY))); nextW.setPadding(5, 2, 5, 2); nextW.setGravity(android.view.Gravity.CENTER);
        weekNavBox.addView(prevW); weekNavBox.addView(weekBox); weekNavBox.addView(nextW); contentArea.addView(weekNavBox);

        LinearLayout actionRow = new LinearLayout(this); actionRow.setOrientation(LinearLayout.HORIZONTAL); actionRow.setGravity(Gravity.CENTER); actionRow.setPadding((int)(20*DENSITY), 0, (int)(20*DENSITY), 0); actionRow.setWeightSum(2);
        LinearLayout markAllBtn = new LinearLayout(this); markAllBtn.setGravity(Gravity.CENTER); markAllBtn.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY)); LinearLayout.LayoutParams markLp = new LinearLayout.LayoutParams(0, -2, 1f);
        markLp.setMargins((int)(16*DENSITY), (int)(4*DENSITY), (int)(8*DENSITY), (int)(4*DENSITY)); markAllBtn.setLayoutParams(markLp); 
        TextView markAllTxt = new TextView(this); markAllTxt.setTextSize(13); markAllTxt.setTypeface(Typeface.DEFAULT_BOLD); 
        GradientDrawable bg1 = new GradientDrawable(); bg1.setCornerRadius(20f * DENSITY);
        bg1.setColor(themeColors[1]); bg1.setStroke((int)(1.5f*DENSITY), themeColors[4]); applyNeo(markAllBtn, 0, 12f, 4f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); markAllBtn.setPadding((int)(16*DENSITY), (int)(10*DENSITY), (int)(16*DENSITY), (int)(10*DENSITY)); 
        
        if (countCompleted < 6) {
            markAllTxt.setText(lang.get("Mark All"));
            markAllTxt.setTextColor(themeColors[2]); 
            View mIcon = ui.getRoundImage("img_tick", 4, Color.TRANSPARENT, colorAccent); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); icLp.setMargins(0,0,(int)(8*DENSITY),0); mIcon.setLayoutParams(icLp); mIcon.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        FrameLayout mIconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams mFlp = new LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));
        mFlp.setMargins(0, 0, (int)(10*DENSITY), 0);
        mIconFrame.setLayoutParams(mFlp);
        applyNeo(mIconFrame, 0, 12f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        FrameLayout.LayoutParams miLp = new FrameLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY));
        miLp.gravity = Gravity.CENTER;
        mIcon.setLayoutParams(miLp);
        mIconFrame.addView(mIcon);
        markAllBtn.addView(mIconFrame); markAllBtn.addView(markAllTxt);
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
            View mIcon = ui.getRoundImage("img_trophy", 4, Color.TRANSPARENT, colorAccent); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); icLp.setMargins(0,0,(int)(8*DENSITY),0); mIcon.setLayoutParams(icLp); mIcon.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        FrameLayout mIconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams mFlp = new LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));
        mFlp.setMargins(0, 0, (int)(10*DENSITY), 0);
        mIconFrame.setLayoutParams(mFlp);
        applyNeo(mIconFrame, 0, 12f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        FrameLayout.LayoutParams miLp = new FrameLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY));
        miLp.gravity = Gravity.CENTER;
        mIcon.setLayoutParams(miLp);
        mIconFrame.addView(mIcon);
        markAllBtn.addView(mIconFrame); markAllBtn.addView(markAllTxt);
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
        LinearLayout.LayoutParams todayLp = new LinearLayout.LayoutParams(0, -2, 1f); todayLp.setMargins((int)(8*DENSITY), (int)(4*DENSITY), (int)(16*DENSITY), (int)(4*DENSITY)); todayBtn.setLayoutParams(todayLp); 
        TextView todayTxt = new TextView(this); todayTxt.setTextSize(13); todayTxt.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable bg2 = new GradientDrawable(); bg2.setCornerRadius(20f * DENSITY); bg2.setColor(themeColors[1]); bg2.setStroke((int)(1.5f*DENSITY), themeColors[4]); applyNeo(todayBtn, 0, 12f, 4f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); todayBtn.setPadding((int)(16*DENSITY), (int)(10*DENSITY), (int)(16*DENSITY), (int)(10*DENSITY)); 
        View tIcon = ui.getRoundImage("img_calender", 4, Color.TRANSPARENT, colorAccent);
        LinearLayout.LayoutParams tIcLp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); tIcLp.setMargins(0,0,(int)(8*DENSITY),0); tIcon.setLayoutParams(tIcLp);
        todayTxt.setTextColor(themeColors[2]); 
        if(!selectedDate[0].equals(sdf.format(new Date()))) { todayTxt.setText(lang.get("Today"));
            todayBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { selectedDate[0] = sdf.format(new Date()); selectedCalArr[0].setTime(new Date()); calendarViewPointer.setTime(new Date()); loadTodayPage(); } });
        } 
        else { todayTxt.setText(lang.get("This Week"));
            todayBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); } statsHelper.showStats(true); } });
        }
        tIcon.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        FrameLayout tIconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams tFlp = new LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));
        tFlp.setMargins(0, 0, (int)(10*DENSITY), 0);
        tIconFrame.setLayoutParams(tFlp);
        applyNeo(tIconFrame, 0, 12f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        FrameLayout.LayoutParams tiLp = new FrameLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY));
        tiLp.gravity = Gravity.CENTER;
        tIcon.setLayoutParams(tiLp);
        tIconFrame.addView(tIcon);
        todayBtn.addView(tIconFrame); todayBtn.addView(todayTxt); actionRow.addView(todayBtn); 
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
        int[] pPaddings = {8, 8, 8, 8, 8, 8}; 
        
        for(int i=0; i<6; i++) {
            final String name = AppConstants.PRAYERS[i];
            final String key = selectedDate[0]+"_"+name; 
            final String stat = getFardStat(todayRec, name); final boolean checked = stat.equals("yes") || stat.equals("excused");
            final boolean isQaza = getQazaStat(todayRec, name);
            
            soup.neumorphism.NeumorphCardView card = new soup.neumorphism.NeumorphCardView(this);
		card.setShapeType(0);
            card.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
            card.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
            card.setShadowElevation(3f * DENSITY);
            card.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 16f*DENSITY).build());
            card.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
            LinearLayout.LayoutParams cLp = new LinearLayout.LayoutParams(-1, -2); 
            cLp.setMargins(0, 0, 0, i==5 ? (int)(15*DENSITY) : 0); 
            card.setLayoutParams(cLp);

            LinearLayout innerCard = new LinearLayout(this);
            innerCard.setOrientation(LinearLayout.HORIZONTAL);
            innerCard.setGravity(Gravity.CENTER_VERTICAL);
            innerCard.setPadding((int)(20*DENSITY), (int)(18*DENSITY), (int)(20*DENSITY), (int)(18*DENSITY));
            card.addView(innerCard);
            View iconView = ui.getRoundImage(pImgs[i], pPaddings[i], android.graphics.Color.TRANSPARENT, colorAccent); 
            LinearLayout.LayoutParams icCardLp = new LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY)); 
            icCardLp.setMargins(0,0,(int)(15*DENSITY),0); iconView.setLayoutParams(icCardLp); 
        iconView.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        iconView.setPadding(5, 2, 5, 2);
        FrameLayout iconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams flp = new LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));
        flp.setMargins(0, 0, (int)(15*DENSITY), 0);
        iconFrame.setLayoutParams(flp);
        applyNeo(iconFrame, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        
        FrameLayout.LayoutParams ivLp = new FrameLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY));
        ivLp.gravity = Gravity.CENTER;
        iconView.setLayoutParams(ivLp);
        iconFrame.addView(iconView);
        innerCard.addView(iconFrame);

            LinearLayout textContainer = new LinearLayout(this); textContainer.setOrientation(LinearLayout.VERTICAL); textContainer.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
            LinearLayout titleRow = new LinearLayout(this); titleRow.setOrientation(LinearLayout.HORIZONTAL); titleRow.setGravity(Gravity.CENTER_VERTICAL);
            TextView tv = new TextView(this); tv.setText(lang.get(name)); tv.setTextColor(stat.equals("excused") ? Color.parseColor("#FF4081") : themeColors[2]); tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setTextSize(16); tv.setSingleLine(true); titleRow.addView(tv);
            if (isQaza && stat.equals("no")) {
                TextView qBadge = new TextView(this);
                qBadge.setText(lang.get("QAZA")); qBadge.setTextColor(themeColors[2]); qBadge.setTextSize(10); qBadge.setTypeface(Typeface.DEFAULT_BOLD); qBadge.setPadding((int)(8*DENSITY), (int)(3*DENSITY), (int)(8*DENSITY), (int)(3*DENSITY)); GradientDrawable qBg = new GradientDrawable(); qBg.setColor(themeColors[5]); qBg.setCornerRadius(10f*DENSITY); qBadge.setBackground(qBg);
                LinearLayout.LayoutParams qLp = new LinearLayout.LayoutParams(-2, -2); qLp.setMargins((int)(10*DENSITY), 0, 0, 0); qBadge.setLayoutParams(qLp); titleRow.addView(qBadge);
            }
            textContainer.addView(titleRow); innerCard.addView(textContainer);
            
            final int finalI = i;
            if (AppConstants.SUNNAHS[i].length > 0 && !stat.equals("excused")) {
                TextView sunnahBtn = new TextView(this);
                int doneSunnahs = 0; int totalS = AppConstants.SUNNAHS[i].length; 
                for(String sName : AppConstants.SUNNAHS[i]) { if (sp.getString(selectedDate[0]+"_"+name+"_Sunnah_"+sName, "no").equals("yes")) doneSunnahs++; }
                String cStr = sp.getString("custom_nafl_" + name, "");
                if(!cStr.isEmpty()) { for(String cN : cStr.split(",")) { if(cN.contains(":")) cN = cN.split(":")[0]; totalS++; if("yes".equals(sp.getString(selectedDate[0]+"_"+name+"_Custom_"+cN, "no"))) doneSunnahs++; } }
                String sText = totalS > 1 ? (lang.get("Extras") + " (" + lang.bnNum(doneSunnahs) + "/" + lang.bnNum(totalS) + ")") : (i == 5 ? lang.get("Tahajjud") : lang.get("Sunnah"));
                sunnahBtn.setText(sText); sunnahBtn.setTextSize(11); sunnahBtn.setSingleLine(true);
                GradientDrawable customSunnahBg = new GradientDrawable(); customSunnahBg.setCornerRadius(12f*DENSITY); if(doneSunnahs > 0){customSunnahBg.setColor(colorAccent);sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]);
                }else{customSunnahBg.setColor(themeColors[5]);sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]);
                } 
                sunnahBtn.setPadding((int)(10*DENSITY), (int)(5*DENSITY), (int)(10*DENSITY), (int)(5*DENSITY));
                int sSur = doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : themeColors[1]); int _rX = android.graphics.Color.red(colorAccent); int _gX = android.graphics.Color.green(colorAccent); int _bX = android.graphics.Color.blue(colorAccent); int accShdTemp = isDarkTheme ? android.graphics.Color.rgb((int)(_rX*0.4f), (int)(_gX*0.4f), (int)(_bX*0.4f)) : android.graphics.Color.argb(100, _rX, _gX, _bX); int sShd = doneSunnahs > 0 ? accShdTemp : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : themeColors[4]); applyNeo(sunnahBtn, 1, 10f, 2f, doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")), isDarkTheme); sunnahBtn.setPadding((int)(14*DENSITY), (int)(8*DENSITY), (int)(14*DENSITY), (int)(8*DENSITY));sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]);
                 sunnahBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY) + (int)(2f*DENSITY)); LinearLayout.LayoutParams customSunnahLp = new LinearLayout.LayoutParams(-2, -2); customSunnahLp.setMargins(0, 0, (int)(15*DENSITY), 0); sunnahBtn.setLayoutParams(customSunnahLp);
                sunnahBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showSunnahDialog(name, AppConstants.SUNNAHS[finalI]); } }); innerCard.addView(sunnahBtn);
            }
            
            final View chk = getNeoCheckbox(stat, colorAccent);
            innerCard.addView(chk);
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
                    
                    v.animate().scaleX(0.95f).scaleY(0.95f).alpha(0.8f).setDuration(35).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(120).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); } }).start();
                    if (!currentStatus) { 
                        int count = 0;
                        for(String p : AppConstants.PRAYERS) { String s = getFardStat(r, p); if(s.equals("yes") || s.equals("excused")) count++;
                        } 
                        if (count == 6) { showSuccessSequence();
                        } 
                    }
                    loadTodayPage(); refreshWidget();
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
         
        // --- ROZA TRACKER START ---
        final boolean isRozaBn = sp.getString("app_lang", "en").equals("bn");
        final String rozaDbKey = selectedDate[0] + "_roza_stat";
        
        android.widget.TextView rozaHdr = new android.widget.TextView(MainActivity.this);
        rozaHdr.setText(isRozaBn ? "অন্যান্য ইবাদত" : "Other Trackers");
        rozaHdr.setTextColor(themeColors[2]);
        rozaHdr.setTextSize(18);
        rozaHdr.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams rozaHdrLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        // মার্জিন জিরো করা হয়েছে যাতে ঠিক নামাজের কার্ডের সাথে এলাইন হয়
        rozaHdrLp.setMargins(0, (int)(5*DENSITY), 0, (int)(10*DENSITY));

        // 100% Match with Prayer Card Layout (pCard)
        soup.neumorphism.NeumorphCardView rCardNeo = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        rCardNeo.setShapeType(0);
        rCardNeo.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
        rCardNeo.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        rCardNeo.setShadowElevation(3f * DENSITY);
        rCardNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 16f*DENSITY).build());
        rCardNeo.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
        android.widget.LinearLayout.LayoutParams rCLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        rCLp.setMargins(0, 0, 0, 0); // 0 margin to exactly match prayer cards
        rCardNeo.setLayoutParams(rCLp);

        android.widget.LinearLayout rInner = new android.widget.LinearLayout(MainActivity.this);
        rInner.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rInner.setGravity(android.view.Gravity.CENTER_VERTICAL);
        rInner.setPadding((int)(20*DENSITY), (int)(18*DENSITY), (int)(20*DENSITY), (int)(18*DENSITY)); // Exact Padding match!
        rCardNeo.addView(rInner);

        // 100% Match with Icon Frame
        android.view.View rIconView = ui.getRoundImage("img_roza", 8, android.graphics.Color.TRANSPARENT, colorAccent);
        rIconView.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        rIconView.setPadding(5, 2, 5, 2);
        android.widget.FrameLayout rIconFrame = new android.widget.FrameLayout(MainActivity.this);
        android.widget.LinearLayout.LayoutParams rFlp = new android.widget.LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));
        rFlp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rIconFrame.setLayoutParams(rFlp);
        applyNeo(rIconFrame, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        android.widget.FrameLayout.LayoutParams rIvLp = new android.widget.FrameLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY));
        rIvLp.gravity = android.view.Gravity.CENTER;
        rIconView.setLayoutParams(rIvLp);
        rIconFrame.addView(rIconView);
        rInner.addView(rIconFrame);

        // Title Row
        android.widget.LinearLayout rTxtCon = new android.widget.LinearLayout(MainActivity.this);
        rTxtCon.setOrientation(android.widget.LinearLayout.VERTICAL);
        rTxtCon.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView rTv = new android.widget.TextView(MainActivity.this);
        rTv.setText(isRozaBn ? "রোজা" : "Fasting");
        rTv.setTextColor(themeColors[2]);
        rTv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        rTv.setTextSize(16);
        rTv.setSingleLine(true);
        rTxtCon.addView(rTv);
        rInner.addView(rTxtCon);

        final String rozaType = sp.getString(selectedDate[0] + "_roza_type", "nafil");
        final boolean isRozaDone = sp.getString(rozaDbKey, "no").equals("yes");

        // Category Button (100% Match with Sunnah Button)
        android.widget.TextView rCatBtn = new android.widget.TextView(MainActivity.this);
        String catLabel = isRozaBn ? "নফল" : "Nafil";
        if(rozaType.equals("fard")) catLabel = isRozaBn ? "ফরজ" : "Fard";
        else if(rozaType.equals("qaza")) catLabel = isRozaBn ? "কাজা" : "Qaza";
        rCatBtn.setText(catLabel);
        rCatBtn.setTextSize(11);
        rCatBtn.setSingleLine(true);
        rCatBtn.setTextColor(isRozaDone ? android.graphics.Color.WHITE : themeColors[2]);
        
        // Exact Sunken 3D Effect for button
        applyNeo(rCatBtn, 1, 10f, 2f, isRozaDone ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")), isDarkTheme);
        rCatBtn.setPadding((int)(14*DENSITY), (int)(8*DENSITY), (int)(14*DENSITY), (int)(8*DENSITY));
        rCatBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY) + (int)(2f*DENSITY));
        android.widget.LinearLayout.LayoutParams rCatLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rCatLp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rCatBtn.setLayoutParams(rCatLp);
        rCatBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showRozaCategoryDialog(); } });
        rInner.addView(rCatBtn);

        // Checkbox (100% Exact match using your own getNeoCheckbox)
        final android.view.View rChkBox = getNeoCheckbox(isRozaDone ? "yes" : "no", colorAccent);
        rInner.addView(rChkBox);

        // Click Action
        rCardNeo.setOnClickListener(new android.view.View.OnClickListener() {
            @Override public void onClick(final android.view.View v) {
                v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                sp.edit().putString(rozaDbKey, !isRozaDone ? "yes" : "no").apply();
                v.animate().scaleX(0.95f).scaleY(0.95f).alpha(0.8f).setDuration(35).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(120).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); } }).start();
                loadTodayPage();
            }
        });

        // সরাসরি নামাজের কার্ডের সাথে যুক্ত করা হচ্ছে (gap ও size 100% match করবে)
        if(isLandscape) {
            col2.addView(rozaHdr, rozaHdrLp);
            col2.addView(rCardNeo);
        } else {
            cardsContainer.addView(rozaHdr, rozaHdrLp);
            cardsContainer.addView(rCardNeo);
        }
        // --- ROZA TRACKER END ---

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
        sub.setTextSize(11); sub.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(sub); 
        Button actionBtn = new Button(this);
        actionBtn.setText(lang.get(isAlreadyExcused ? "Remove Excused Status" : "Mark Today as Excused")); actionBtn.setAllCaps(false); actionBtn.setTextColor(android.graphics.Color.WHITE); actionBtn.setTypeface(Typeface.DEFAULT_BOLD); 
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
        
        

        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show(); 
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
        
        // একদম পারফেক্ট A-Z সর্টিং
        // --- SETTINGS NEW START ---
        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কালার ও থিম পরিবর্তন" : "Change Color & Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() {
            @Override public void run() { 
                final boolean isBn = sp.getString("app_lang", "en").equals("bn");
                android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL);
                main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
                
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "নির্বাচন করুন" : "Select Option");
                title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                
                String[] copts = isBn ? new String[]{"থিম পরিবর্তন (সাদা/কালো)", "কালার পরিবর্তন করুন"} : new String[]{"Change Theme (Dark/Light)", "Change Color"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                
                for(int i=0; i<copts.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout row = new android.widget.LinearLayout(MainActivity.this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL);
                    row.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY));
                    android.widget.TextView dot = new android.widget.TextView(MainActivity.this); dot.setText("•"); dot.setTextColor(colorAccent); dot.setTextSize(22); dot.setPadding(0,0,(int)(10*DENSITY),0);
                    android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(copts[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
                    row.addView(dot); row.addView(tv); main.addView(row);
                    row.setOnClickListener(new android.view.View.OnClickListener() {
                        @Override public void onClick(android.view.View v) {
                            if(w==0) { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); }
                            else { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); }
                            ad.dismiss(); finish(); overridePendingTransition(0, 0); android.content.Intent intent = new android.content.Intent(MainActivity.this, MainActivity.class); try{intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime());}catch(Exception e){} startActivity(intent);
                        }
                    });
                }
                android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER;
                wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
                if(!isFinishing()) ad.show();
            }
        });

        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
            @Override public void run() {
                final boolean isBn = sp.getString("app_lang", "en").equals("bn");
                android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL);
                main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
                
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
                title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                
                String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                
                for(int i=0; i<ops.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout row = new android.widget.LinearLayout(MainActivity.this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL);
                    row.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY));
                    android.widget.TextView dot = new android.widget.TextView(MainActivity.this); dot.setText("•"); dot.setTextColor(colorAccent); dot.setTextSize(22); dot.setPadding(0,0,(int)(10*DENSITY),0);
                    android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(ops[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
                    row.addView(dot); row.addView(tv); main.addView(row);
                    row.setOnClickListener(new android.view.View.OnClickListener() {
                        @Override public void onClick(android.view.View v) {
                            ad.dismiss();
                            final boolean iH = (w == 0); final String pK = iH ? "hijri_offset" : "bn_date_offset";
                            android.widget.FrameLayout iWrap = new android.widget.FrameLayout(MainActivity.this); iWrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                            android.widget.LinearLayout iMain = new android.widget.LinearLayout(MainActivity.this); iMain.setOrientation(android.widget.LinearLayout.VERTICAL);
                            iMain.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                            android.graphics.drawable.GradientDrawable igd = new android.graphics.drawable.GradientDrawable(); igd.setColor(themeColors[1]); igd.setCornerRadius(20f * DENSITY); iMain.setBackground(igd);
                            
                            android.widget.TextView iTitle = new android.widget.TextView(MainActivity.this); iTitle.setText(iH ? (isBn ? "আরবি তারিখ এডজাস্ট" : "Adjust Hijri") : (isBn ? "বাংলা তারিখ এডজাস্ট" : "Adjust Bengali"));
                            iTitle.setTextColor(themeColors[2]); iTitle.setTextSize(18); iTitle.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); iTitle.setPadding(0,0,0,(int)(15*DENSITY)); iMain.addView(iTitle);
                            
                            final android.widget.EditText inp = new android.widget.EditText(MainActivity.this); inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                            inp.setText(String.valueOf(sp.getInt(pK, 0))); inp.setTextColor(themeColors[2]);
                            android.graphics.drawable.GradientDrawable ibg = new android.graphics.drawable.GradientDrawable(); ibg.setStroke((int)(1.5f*DENSITY), themeColors[3]); ibg.setCornerRadius(10f*DENSITY); inp.setBackground(ibg); inp.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
                            iMain.addView(inp);
                            
                            android.widget.TextView btn = new android.widget.TextView(MainActivity.this); btn.setText("OK"); btn.setTextColor(android.graphics.Color.WHITE); btn.setGravity(android.view.Gravity.CENTER); btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                            btn.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
                            android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setColor(colorAccent); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg);
                            android.widget.LinearLayout.LayoutParams blp = new android.widget.LinearLayout.LayoutParams(-1, -2); blp.setMargins(0, (int)(20*DENSITY), 0, 0); iMain.addView(btn, blp);
                            
                            final android.app.AlertDialog iAd = new android.app.AlertDialog.Builder(MainActivity.this).setView(iWrap).create();
                            btn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); iAd.dismiss(); } catch(Exception e){} } });
                            
                            android.widget.FrameLayout.LayoutParams iflp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); iflp.gravity = android.view.Gravity.CENTER;
                            iWrap.addView(iMain, iflp); iAd.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                            iAd.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(iMain, appFonts[0], appFonts[1]);
                            if(!isFinishing()) iAd.show();
                        }
                    });
                }
                android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER;
                wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
                if(!isFinishing()) ad.show();
            }
        });
        // --- SETTINGS NEW END ---
        mr.addImg("Advanced Statistics", "img_stats", new Runnable() { @Override public void run() { try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); } statsHelper.showStatsOptionsDialog(); }});
        mr.addImg("Backup & Sync", "img_cloud", new Runnable() { @Override public void run() { backupHelper.showProfileDialog(new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); }}); }});
        mr.addImg("Change Language", "img_lang", new Runnable() { @Override public void run() { String nextL = sp.getString("app_lang", "en").equals("en") ? "bn" : "en"; sp.edit().putString("app_lang", nextL).apply(); finish(); Intent intent = new Intent(MainActivity.this, MainActivity.class); try { intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime()); } catch(Exception e){} startActivity(intent); overridePendingTransition(0, 0); }});
        // mr.addImg("Choose Theme", "img_theme", new Runnable() { @Override public void run() { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); finish(); Intent intent = new Intent(MainActivity.this, MainActivity.class); try { intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime()); } catch(Exception e){} startActivity(intent); overridePendingTransition(0, 0); }});
        mr.addImg("View Qaza List", "img_custom_qaza", new Runnable() { @Override public void run() { showQazaListDialog(); }});

        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2);
        flp.gravity = Gravity.CENTER; wrap.addView(mainLayout, flp);
        applyFont(mainLayout, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
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
            View customEmptyIcon = ui.getRoundImage("img_empty_qaza", 0, android.graphics.Color.TRANSPARENT, colorAccent);
            LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(80*DENSITY), (int)(80*DENSITY)); icLp.gravity = Gravity.CENTER; icLp.setMargins(0, (int)(20*DENSITY), 0, (int)(10*DENSITY)); customEmptyIcon.setLayoutParams(icLp); list.addView(customEmptyIcon);
            TextView empty = new TextView(this);
            empty.setText(lang.get("Alhamdulillah! No pending Qaza.")); empty.setTextColor(themeColors[3]); empty.setGravity(Gravity.CENTER);
            empty.setPadding(0, 0, 0, (int)(20*DENSITY)); list.addView(empty);
        }
        
        scroll.addView(list);
        main.addView(scroll, new LinearLayout.LayoutParams(-1, (int)(300*DENSITY)));
        TextView closeBtn = new TextView(this); closeBtn.setText(lang.get("CLOSE")); closeBtn.setTextColor(themeColors[3]); closeBtn.setGravity(Gravity.CENTER); closeBtn.setTypeface(Typeface.DEFAULT_BOLD); closeBtn.setPadding(0, (int)(20*DENSITY), 0, 0); main.addView(closeBtn);
        closeBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); } });
        FrameLayout.LayoutParams flp2 = new FrameLayout.LayoutParams((int)(320*DENSITY), -2);
        flp2.gravity = Gravity.CENTER; wrap.addView(main, flp2);
        
        

        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
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
                    setFardStat(r, p, "yes"); setQazaStat(r, p, false);
                    sp.edit().putString(selectedDate[0]+"_"+p, "yes").apply(); sp.edit().putBoolean(selectedDate[0]+"_"+p+"_qaza", false).apply(); 
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
                    setFardStat(r, AppConstants.PRAYERS[i], "yes"); setQazaStat(r, AppConstants.PRAYERS[i], false);
                    sp.edit().putString(selectedDate[0]+"_"+AppConstants.PRAYERS[i], "yes").apply(); sp.edit().putBoolean(selectedDate[0]+"_"+AppConstants.PRAYERS[i]+"_qaza", false).apply(); fbHelper.save(selectedDate[0], AppConstants.PRAYERS[i], "yes"); 
                    for(String sName : AppConstants.SUNNAHS[i]) { sp.edit().putString(selectedDate[0]+"_"+AppConstants.PRAYERS[i]+"_Sunnah_"+sName, "yes").apply(); fbHelper.save(selectedDate[0], AppConstants.PRAYERS[i]+"_Sunnah_"+sName, "yes"); } 
                } 
                updateRoomRecord(r);
                ad.dismiss(); loadTodayPage(); refreshWidget(); 
                showSuccessSequence(); // ✨ ফিক্স: মাশাআল্লাহ যুক্ত করা হলো
            } 
        });
        
        

        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
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
        }); 
        

        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }

    private void showSuccessSequence() {
        if(sp.getBoolean(selectedDate[0] + "_success_shown", false)) return;
        sp.edit().putBoolean(selectedDate[0] + "_success_shown", true).apply(); 
        final LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL); main.setGravity(Gravity.CENTER); main.setPadding((int)(30*DENSITY), (int)(45*DENSITY), (int)(30*DENSITY), (int)(45*DENSITY)); 
        GradientDrawable gd = new GradientDrawable(); gd.setColor(colorAccent); gd.setCornerRadius(30f * DENSITY); main.setBackground(gd); 
        if(Build.VERSION.SDK_INT >= 21) main.setElevation(50f);
        TextView iconView = new TextView(this); iconView.setText("💎"); iconView.setTextSize(60); iconView.setGravity(Gravity.CENTER); iconView.setPadding(0, 0, 0, (int)(10*DENSITY)); main.addView(iconView); 
        TextView title = new TextView(this); title.setText(lang.get("Mashallah!")); title.setTextColor(android.graphics.Color.WHITE);
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
        new Handler().postDelayed(new Runnable() { @Override public void run() { main.animate().scaleX(0.8f).scaleY(0.8f).alpha(0f).setDuration(200).withEndAction(new Runnable() { @Override public void run() { root.removeView(main); } }).start(); } }, 2500);
        
        

        applyFont(main, appFonts[0], appFonts[1]); 
    }
private void showWipeDataDialog() {
        FrameLayout wrap = new FrameLayout(this); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        View icon = ui.getRoundImage("img_offline_warning", 0, android.graphics.Color.TRANSPARENT, android.graphics.Color.parseColor("#FF5252")); 
        LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(50*DENSITY), (int)(50*DENSITY)); icLp.gravity = Gravity.CENTER_HORIZONTAL; icLp.setMargins(0, 0, 0, (int)(3f * DENSITY)); icon.setLayoutParams(icLp); main.addView(icon);
        TextView title = new TextView(this); title.setText(lang.get("Wipe All Data")); title.setTextColor(android.graphics.Color.parseColor("#FF5252")); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); main.addView(title);
        TextView sub = new TextView(this); sub.setText(lang.get("Are you sure? This will delete all your local data permanently.")); sub.setTextColor(themeColors[3]); sub.setTextSize(14); sub.setGravity(Gravity.CENTER); sub.setPadding(0, (int)(10*DENSITY), 0, (int)(25*DENSITY)); main.addView(sub);
        LinearLayout row = new LinearLayout(this); row.setOrientation(LinearLayout.HORIZONTAL);
        Button btnC = new Button(this); btnC.setText(lang.get("CANCEL")); btnC.setTextColor(themeColors[2]); btnC.setAllCaps(false); btnC.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable bgC = new GradientDrawable(); bgC.setColor(themeColors[4]); bgC.setCornerRadius(15f*DENSITY); btnC.setBackground(bgC);
        LinearLayout.LayoutParams lpC = new LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f); lpC.setMargins(0,0,(int)(10*DENSITY),0); row.addView(btnC, lpC);
        Button btnD = new Button(this); btnD.setText(lang.get("Delete")); btnD.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); btnD.setAllCaps(false); btnD.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable bgD = new GradientDrawable(); bgD.setColor(android.graphics.Color.parseColor("#FF5252")); bgD.setCornerRadius(15f*DENSITY); btnD.setBackground(bgD);
        LinearLayout.LayoutParams lpD = new LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f); row.addView(btnD, lpD); main.addView(row);
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(Gravity.CENTER);
        
        

        applyFont(main, appFonts[0], appFonts[1]); btnC.setOnClickListener(new View.OnClickListener(){@Override public void onClick(View v){ad.dismiss();}});
        btnD.setOnClickListener(new View.OnClickListener(){@Override public void onClick(View v){
            ad.dismiss(); ui.showSmartBanner(root, lang.get("Deleting..."), "", "img_offline_warning", android.graphics.Color.parseColor("#FF5252"), null);
            new Thread(new Runnable(){@Override public void run(){
                SalahDatabase.getDatabase(MainActivity.this).clearAllTables(); sp.edit().clear().apply();
                runOnUiThread(new Runnable(){@Override public void run(){ finish(); Intent intent = new Intent(MainActivity.this, MainActivity.class);
        try { intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime()); } catch(Exception e){}
        startActivity(intent); }});
            }}).start();
        }}); if(!isFinishing()) ad.show();
    }

    
    private void showRozaCategoryDialog() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this);
        wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); 
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); 
        main.setOrientation(android.widget.LinearLayout.VERTICAL); 
        main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); 
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); 
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); 
        
        android.widget.TextView title = new android.widget.TextView(this); 
        title.setText(isBn ? "রোজার ক্যাটাগরি" : "Fasting Category"); 
        title.setTextColor(colorAccent); title.setTextSize(20); 
        title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        
        android.widget.ScrollView sv = new android.widget.ScrollView(this); 
        android.widget.LinearLayout list = new android.widget.LinearLayout(this); 
        list.setOrientation(android.widget.LinearLayout.VERTICAL);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); 
        
        String[] opts = isBn ? new String[]{"ফরজ", "কাজা", "নফল"} : new String[]{"Fard", "Qaza", "Nafil"};
        final String[] vals = {"fard", "qaza", "nafil"};
        String curType = sp.getString(selectedDate[0] + "_roza_type", "nafil");
        
        for(int s=0; s<opts.length; s++) { 
            final String sName = opts[s];
            final String sVal = vals[s];
            final boolean sChecked = curType.equals(sVal);
            
            final android.widget.LinearLayout row = new android.widget.LinearLayout(this); 
            row.setOrientation(android.widget.LinearLayout.HORIZONTAL); 
            row.setGravity(android.view.Gravity.CENTER_VERTICAL); 
            row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); 
            android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
            rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp); 
            final android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); 
            rowBg.setCornerRadius(15f*DENSITY); 
            rowBg.setColor(sChecked ? themeColors[4] : android.graphics.Color.TRANSPARENT); 
            row.setBackground(rowBg);
            
            final android.widget.TextView tv = new android.widget.TextView(this); 
            tv.setText(sName); 
            tv.setTextColor(sChecked ? colorAccent : themeColors[2]); 
            tv.setTextSize(16); 
            tv.setTypeface(sChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT);
            tv.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); 
            
            final android.view.View chk = ui.getPremiumCheckbox(sChecked ? "yes" : "no", colorAccent); 
            row.addView(tv); row.addView(chk); list.addView(row);
            
            row.setOnClickListener(new android.view.View.OnClickListener() { 
                @Override public void onClick(final android.view.View v) { 
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); 
                    sp.edit().putString(selectedDate[0] + "_roza_type", sVal).apply(); 
                    sp.edit().putString(selectedDate[0] + "_roza_stat", "yes").apply();
                    ad.dismiss();
                    loadTodayPage();
                } 
            });
        } 
        
        sv.addView(list);
        main.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, -2, 1f));
        
        android.widget.TextView closeBtn = new android.widget.TextView(this); 
        closeBtn.setText(lang.get("Done")); 
        closeBtn.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); 
        closeBtn.setGravity(android.view.Gravity.CENTER); 
        closeBtn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); 
        closeBtn.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY));
        android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); 
        cBg.setColor(colorAccent); cBg.setCornerRadius(20f*DENSITY); 
        closeBtn.setBackground(cBg); 
        android.widget.LinearLayout.LayoutParams clp = new android.widget.LinearLayout.LayoutParams(-1, -2); 
        clp.setMargins(0, (int)(15*DENSITY), 0, 0); 
        closeBtn.setLayoutParams(clp); 
        main.addView(closeBtn);
        
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); 
        flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(android.view.Gravity.CENTER);
        closeBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); loadTodayPage(); } });
        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
    // --- ROZA DIALOG END ---

    private void showSunnahDialog(final String prayer, final String[] sunnahList) { 
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); 
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get(prayer) + " " + lang.get("Extras")); title.setTextColor(colorAccent); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        android.widget.ScrollView sv = new android.widget.ScrollView(this); android.widget.LinearLayout list = new android.widget.LinearLayout(this); list.setOrientation(android.widget.LinearLayout.VERTICAL);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); 
        for(int s=0; s<sunnahList.length; s++) { 
            final String sName = sunnahList[s]; final String sKey = selectedDate[0] + "_" + prayer + "_Sunnah_" + sName; final boolean sChecked = sp.getString(sKey, "no").equals("yes");
            final android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL); row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2); rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp); final android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); rowBg.setCornerRadius(15f*DENSITY); rowBg.setColor(sChecked ? themeColors[4] : android.graphics.Color.TRANSPARENT); row.setBackground(rowBg);
            final android.widget.TextView tv = new android.widget.TextView(this); tv.setText(lang.get(sName)); tv.setTextColor(sChecked ? colorAccent : themeColors[2]); tv.setTextSize(16); tv.setTypeface(sChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT); tv.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); final android.view.View chk = ui.getPremiumCheckbox(sChecked ? "yes" : "no", colorAccent); row.addView(tv); row.addView(chk); list.addView(row);
            row.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); boolean cur = sp.getString(sKey, "no").equals("yes"); boolean newVal = !cur; sp.edit().putString(sKey, newVal ? "yes" : "no").apply(); fbHelper.save(selectedDate[0], prayer + "_Sunnah_" + sName, newVal ? "yes" : "no"); android.widget.TextView t = (android.widget.TextView) chk; android.graphics.drawable.GradientDrawable bg = (android.graphics.drawable.GradientDrawable) t.getBackground(); if(newVal) { bg.setColor(colorAccent); bg.setStroke(0, android.graphics.Color.TRANSPARENT); t.setText("✓"); t.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); rowBg.setColor(themeColors[4]); tv.setTextColor(colorAccent); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); } else { bg.setColor(android.graphics.Color.TRANSPARENT); bg.setStroke((int)(2*DENSITY), themeColors[4]); t.setText(""); rowBg.setColor(android.graphics.Color.TRANSPARENT); tv.setTextColor(themeColors[2]); tv.setTypeface(android.graphics.Typeface.DEFAULT); } } });
        } 
        String cStr = sp.getString("custom_nafl_" + prayer, "");
        if(!cStr.isEmpty()) {
            for(final String cItem : cStr.split(",")) {
                if(cItem.trim().isEmpty()) continue; String[] pts = cItem.split(":"); final String cName = pts[0]; final String cRak = pts.length>1?pts[1]:"2";
                final String cKey = selectedDate[0] + "_" + prayer + "_Custom_" + cName; final boolean cChecked = sp.getString(cKey, "no").equals("yes");
                final android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL); row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2); rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp); final android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); rowBg.setCornerRadius(15f*DENSITY); rowBg.setColor(cChecked ? themeColors[4] : android.graphics.Color.TRANSPARENT); row.setBackground(rowBg);
                android.widget.LinearLayout tCon = new android.widget.LinearLayout(this); tCon.setOrientation(android.widget.LinearLayout.VERTICAL); tCon.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
                final android.widget.TextView tv = new android.widget.TextView(this); tv.setText(cName); tv.setSingleLine(true); tv.setEllipsize(android.text.TextUtils.TruncateAt.END); tv.setTextColor(cChecked ? colorAccent : themeColors[2]); tv.setTextSize(16); tv.setTypeface(cChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT); tCon.addView(tv);
                android.widget.TextView tvR = new android.widget.TextView(this); tvR.setText(lang.bnNum(cRak) + " " + lang.get("Rakats")); tvR.setTextColor(themeColors[3]); tvR.setTextSize(12); tvR.setPadding(5, 2, 5, 2); tCon.addView(tvR); row.addView(tCon);
                final android.view.View chk = ui.getPremiumCheckbox(cChecked ? "yes" : "no", colorAccent); row.addView(chk); list.addView(row);
                row.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); boolean cur = sp.getString(cKey, "no").equals("yes"); boolean newVal = !cur; sp.edit().putString(cKey, newVal ? "yes" : "no").apply(); fbHelper.save(selectedDate[0], prayer + "_Custom_" + cName, newVal ? "yes" : "no"); android.widget.TextView t = (android.widget.TextView) chk; android.graphics.drawable.GradientDrawable bg = (android.graphics.drawable.GradientDrawable) t.getBackground(); if(newVal) { bg.setColor(colorAccent); bg.setStroke(0, android.graphics.Color.TRANSPARENT); t.setText("✓"); t.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); rowBg.setColor(themeColors[4]); tv.setTextColor(colorAccent); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); } else { bg.setColor(android.graphics.Color.TRANSPARENT); bg.setStroke((int)(2*DENSITY), themeColors[4]); t.setText(""); rowBg.setColor(android.graphics.Color.TRANSPARENT); tv.setTextColor(themeColors[2]); tv.setTypeface(android.graphics.Typeface.DEFAULT); } } });
                row.setOnLongClickListener(new android.view.View.OnLongClickListener() { @Override public boolean onLongClick(android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); showDeleteCustomPrayerDialog(prayer, cName, ad); return true; } });
            }
        }
        android.widget.LinearLayout addBtn = new android.widget.LinearLayout(this); addBtn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY)); addBtn.setGravity(android.view.Gravity.CENTER); android.graphics.drawable.GradientDrawable aBg = new android.graphics.drawable.GradientDrawable(); aBg.setColor(themeColors[4]); aBg.setCornerRadius(15f*DENSITY); addBtn.setBackground(aBg); android.widget.LinearLayout.LayoutParams aLp = new android.widget.LinearLayout.LayoutParams(-1, -2); aLp.setMargins(0, (int)(10*DENSITY), 0, (int)(10*DENSITY)); addBtn.setLayoutParams(aLp);
        android.widget.TextView aTxt = new android.widget.TextView(this); aTxt.setText("➕ " + lang.get("Add Extra Prayer")); aTxt.setTextColor(themeColors[2]); aTxt.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); addBtn.addView(aTxt);
        addBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); showAddCustomPrayerDialog(prayer, ad); } }); list.addView(addBtn);
        sv.addView(list); main.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, -2, 1f));
        android.widget.TextView closeBtn = new android.widget.TextView(this); closeBtn.setText(lang.get("Done")); closeBtn.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); closeBtn.setGravity(android.view.Gravity.CENTER); closeBtn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); closeBtn.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY)); android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(colorAccent); cBg.setCornerRadius(20f*DENSITY); closeBtn.setBackground(cBg); android.widget.LinearLayout.LayoutParams clp = new android.widget.LinearLayout.LayoutParams(-1, -2); clp.setMargins(0, (int)(15*DENSITY), 0, 0); closeBtn.setLayoutParams(clp); main.addView(closeBtn); 
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); 
        closeBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); loadTodayPage(); refreshWidget(); } });
        
        

        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show(); 
    }

    private void showAddCustomPrayerDialog(final String prayer, final android.app.AlertDialog parentDialog) {
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(30f * DENSITY); main.setBackground(gd);
        android.view.View iconView = ui.getRoundImage("img_custom_nafl", 0, android.graphics.Color.TRANSPARENT, 0); android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(60*DENSITY), (int)(60*DENSITY)); icLp.gravity = android.view.Gravity.CENTER; icLp.setMargins(0, 0, 0, (int)(3f * DENSITY)); iconView.setLayoutParams(icLp); main.addView(iconView);
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get("Add Extra Prayer")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setGravity(android.view.Gravity.CENTER); title.setPadding(0, (int)(10*DENSITY), 0, (int)(25*DENSITY)); main.addView(title);
        final android.widget.EditText nameIn = new android.widget.EditText(this); nameIn.setHint(lang.get("Prayer Name (e.g. Ishraq)")); nameIn.setTextColor(themeColors[2]); nameIn.setHintTextColor(themeColors[3]); android.graphics.drawable.GradientDrawable iBg = new android.graphics.drawable.GradientDrawable(); iBg.setColor(themeColors[4]); iBg.setCornerRadius(15f*DENSITY); nameIn.setBackground(iBg); nameIn.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY)); main.addView(nameIn, new android.widget.LinearLayout.LayoutParams(-1, -2));
        final android.widget.EditText rakIn = new android.widget.EditText(this); rakIn.setHint(lang.get("Rakats (e.g. 2)")); rakIn.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); rakIn.setTextColor(themeColors[2]); rakIn.setHintTextColor(themeColors[3]); rakIn.setBackground(iBg); rakIn.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY)); android.widget.LinearLayout.LayoutParams rLp = new android.widget.LinearLayout.LayoutParams(-1, -2); rLp.setMargins(0,(int)(10*DENSITY),0,(int)(25*DENSITY)); main.addView(rakIn, rLp);
        android.widget.Button btn = new android.widget.Button(this); btn.setText(lang.get("Add Prayer")); btn.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btn.setAllCaps(false); android.graphics.drawable.GradientDrawable bBg = new android.graphics.drawable.GradientDrawable(); bBg.setColor(colorAccent); bBg.setCornerRadius(20f*DENSITY); btn.setBackground(bBg); main.addView(btn, new android.widget.LinearLayout.LayoutParams(-1, (int)(55*DENSITY)));
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); 
        

        applyFont(main, appFonts[0], appFonts[1]);
        btn.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){
            String n = nameIn.getText().toString().trim().replace(":", "").replace(",", "").replace("|", ""); String r = rakIn.getText().toString().trim();
            if(!n.isEmpty()) { String cList = sp.getString("custom_nafl_" + prayer, ""); sp.edit().putString("custom_nafl_" + prayer, cList + (cList.isEmpty()?"":",") + n + ":" + (r.isEmpty()?"2":r)).apply(); ad.dismiss(); if(parentDialog!=null) parentDialog.dismiss(); loadTodayPage(); refreshWidget(); int idx = java.util.Arrays.asList(AppConstants.PRAYERS).indexOf(prayer); if(idx != -1) showSunnahDialog(prayer, AppConstants.SUNNAHS[idx]); }
        }}); if(!isFinishing()) ad.show();
    }
    
    private void showDeleteCustomPrayerDialog(final String prayer, final String cName, final android.app.AlertDialog parentDialog) {
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get("Delete Extra Prayer?")); title.setTextColor(android.graphics.Color.parseColor("#FF5252")); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setGravity(android.view.Gravity.CENTER); main.addView(title);
        android.widget.TextView sub = new android.widget.TextView(this); sub.setText(lang.get("This will remove it from your list.")); sub.setTextColor(themeColors[3]); sub.setGravity(android.view.Gravity.CENTER); sub.setPadding(0,(int)(10*DENSITY),0,(int)(25*DENSITY)); main.addView(sub);
        android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        android.widget.Button btnC = new android.widget.Button(this); btnC.setText(lang.get("CANCEL")); btnC.setTextColor(themeColors[2]); btnC.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btnC.setAllCaps(false); android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(themeColors[4]); cBg.setCornerRadius(15f*DENSITY); btnC.setBackground(cBg); android.widget.LinearLayout.LayoutParams lpC = new android.widget.LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f); lpC.setMargins(0,0,(int)(10*DENSITY),0); row.addView(btnC, lpC);
        android.widget.Button btnD = new android.widget.Button(this); btnD.setText(lang.get("Delete")); btnD.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); btnD.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btnD.setAllCaps(false); android.graphics.drawable.GradientDrawable dBg = new android.graphics.drawable.GradientDrawable(); dBg.setColor(android.graphics.Color.parseColor("#FF5252")); dBg.setCornerRadius(15f*DENSITY); btnD.setBackground(dBg); row.addView(btnD, new android.widget.LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f)); main.addView(row);
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); 
        

        applyFont(main, appFonts[0], appFonts[1]);
        btnC.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){ad.dismiss();}});
        btnD.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){ String cList = sp.getString("custom_nafl_" + prayer, ""); String[] pts = cList.split(","); StringBuilder sb = new StringBuilder(); for(String p : pts) { if(!p.startsWith(cName+":") && !p.equals(cName)) { sb.append(p).append(","); } } String res = sb.toString(); if(res.endsWith(",")) res = res.substring(0, res.length()-1); sp.edit().putString("custom_nafl_" + prayer, res).apply(); ad.dismiss(); if(parentDialog!=null) parentDialog.dismiss(); loadTodayPage(); refreshWidget(); int idx = java.util.Arrays.asList(AppConstants.PRAYERS).indexOf(prayer); if(idx != -1) showSunnahDialog(prayer, AppConstants.SUNNAHS[idx]); }}); if(!isFinishing()) ad.show();
    }


    public static class WaterWaveView extends android.view.View {
        private android.graphics.Path path = new android.graphics.Path();
        private android.graphics.Paint paint = new android.graphics.Paint();
        private float phase = 0f;
        private int progress = 0;
        public WaterWaveView(android.content.Context context) {
            super(context);
            paint.setStyle(android.graphics.Paint.Style.FILL);
            paint.setAntiAlias(true);
        }
        public void setProgressAndColor(int p, int c) {
            this.progress = p;
            paint.setColor(c);
            invalidate();
        }
        @Override
        protected void onDraw(android.graphics.Canvas canvas) {
            super.onDraw(canvas);
            int w = getWidth();
            int h = getHeight();
            if (w == 0 || h == 0) return;
            path.reset();
            float baseHeight = h - (h * progress / 100f);
            float amplitude = h * 0.05f; // ঢেউয়ের উচ্চতা
            path.moveTo(0, h);
            path.lineTo(0, baseHeight);
            for (int i = 0; i <= w; i += 10) {
                float y = (float) (Math.sin((i * 3 * Math.PI / w) + phase) * amplitude) + baseHeight;
                path.lineTo(i, y);
            }
            path.lineTo(w, h);
            path.close();
            canvas.drawPath(path, paint);
            phase += 0.15f; // ঢেউয়ের স্পিড
            postInvalidateDelayed(20); // স্মুথ অ্যানিমেশনের জন্য
        }
    }
    

    


    


    


    


    

}