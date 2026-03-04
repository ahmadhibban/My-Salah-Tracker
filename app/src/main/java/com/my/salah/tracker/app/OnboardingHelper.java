package com.my.salah.tracker.app;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.OvershootInterpolator;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

public class OnboardingHelper {
    private Activity activity;
    private float DENSITY;
    private int[] themeColors;
    private int colorAccent;
    private LanguageEngine lang;
    private UIComponents ui;
    private SharedPreferences sp;
    private FrameLayout root;
    private Typeface[] appFonts;

    public OnboardingHelper(Activity activity, float DENSITY, int[] themeColors, int colorAccent, LanguageEngine lang, UIComponents ui, SharedPreferences sp, FrameLayout root, Typeface[] appFonts) {
        this.activity = activity;
        this.DENSITY = DENSITY;
        this.themeColors = themeColors;
        this.colorAccent = colorAccent;
        this.lang = lang;
        this.ui = ui;
        this.sp = sp;
        this.root = root;
        this.appFonts = appFonts;
    }

    private void applyFont(View v) {
        if (v instanceof TextView) {
            TextView tv = (TextView) v;
            if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(appFonts[1]);
            else tv.setTypeface(appFonts[0]);
        } else if (v instanceof ViewGroup) {
            ViewGroup vg = (ViewGroup) v;
            for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i));
        }
    }

    public void showOnboarding() {
        final FrameLayout obRoot = new FrameLayout(activity);
        obRoot.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        obRoot.setBackgroundColor(themeColors[0]);
        obRoot.setClickable(true); 
        if(Build.VERSION.SDK_INT >= 21) obRoot.setElevation(100f);

        final LinearLayout obMain = new LinearLayout(activity);
        obMain.setOrientation(LinearLayout.VERTICAL);
        obMain.setGravity(Gravity.CENTER);
        obMain.setPadding((int)(40*DENSITY), 0, (int)(40*DENSITY), 0);

        final View[] currentIcon = {null};
        final TextView obTitle = new TextView(activity);
        obTitle.setTextColor(themeColors[2]); obTitle.setTextSize(26); obTitle.setTypeface(Typeface.DEFAULT_BOLD); obTitle.setGravity(Gravity.CENTER); obTitle.setPadding(0, (int)(30*DENSITY), 0, (int)(15*DENSITY));
        final TextView obDesc = new TextView(activity);
        obDesc.setTextColor(themeColors[3]); obDesc.setTextSize(16); obDesc.setGravity(Gravity.CENTER); obDesc.setLineSpacing(0, 1.3f);
        
        final boolean isBn = sp.getString("app_lang", "en").equals("bn"); 
        
        final Button obNext = new Button(activity);
        obNext.setText(isBn ? "পরবর্তী" : "Next"); obNext.setTextColor(Color.WHITE); obNext.setAllCaps(false); obNext.setTextSize(16);
        GradientDrawable nBg = new GradientDrawable(); nBg.setColor(colorAccent); nBg.setCornerRadius(25f*DENSITY); obNext.setBackground(nBg);
        LinearLayout.LayoutParams bnLp = new LinearLayout.LayoutParams(-1, (int)(55*DENSITY)); bnLp.setMargins(0, (int)(50*DENSITY), 0, 0); obNext.setLayoutParams(bnLp);

        final String[] titles = isBn ? new String[]{"সালাহ প্রো-তে স্বাগতম", "প্রতিদিনের নামাজ ট্র্যাক করুন", "কাজা নামাজ আর ভুলবেন না", "প্রিমিয়াম ট্রফি অর্জন করুন", "সিকিউর ক্লাউড ব্যাকআপ"} : new String[]{"Welcome to Salah Pro", "Track Daily Prayers", "Never Miss a Qaza", "Win Premium Trophies", "Secure Cloud Backup"};
        final String[] descs = isBn ? new String[]{"আপনার ব্যক্তিগত, আধুনিক এবং অ্যাড-ফ্রি সঙ্গী, যা আপনাকে নিয়মিত নামাজ আদায়ে সাহায্য করবে।", "শুধুমাত্র একটি ট্যাপের মাধ্যমে সহজেই ফরজ এবং সুন্নাহ নামাজ মার্ক করুন।", "যেকোনো নামাজের উপর লং প্রেস করে সহজেই সেটিকে কাজা লিস্টে যোগ করুন।", "প্রতিদিন নামাজ আদায় করে আপনার স্ট্রিক বজায় রাখুন এবং সুন্দর ব্যাজ ও অর্জন আনলক করুন।", "আপনার ডাটা মোবাইলে বা ক্লাউডে নিরাপদে সেভ রাখুন। চলুন শুরু করি!"} : new String[]{"Your personal, modern, and ad-free companion to build a consistent prayer habit.", "Easily mark Fard and Sunnah prayers with a single tap.", "Long press any prayer to safely add it to your pending Qaza list.", "Maintain your daily streaks to unlock beautiful badges and achievements.", "Keep your data safe locally or sync it to the cloud. Let's begin!"};
            
        final String[] emojis = {"🕌", "✨", "⚠️", "🏆", "☁️"};
        final int[] colorsH = {Color.parseColor("#8E2DE2"), Color.parseColor("#00D2FF"), Color.parseColor("#FF5252"), Color.parseColor("#FFB75E"), Color.parseColor("#4CA1AF")};
        final int[] step = {0};

        final Runnable updateSlide = new Runnable() {
            @Override public void run() {
                obMain.removeAllViews();
                currentIcon[0] = ui.getPremiumIcon(emojis[step[0]], colorsH[step[0]], colorsH[step[0]], 120);
                ((TextView)currentIcon[0]).setTextSize(60);
                obTitle.setText(titles[step[0]]); obDesc.setText(descs[step[0]]);
                if(step[0] == titles.length - 1) obNext.setText(isBn ? "শুরু করুন" : "Get Started"); 
                obMain.addView(currentIcon[0]); obMain.addView(obTitle); obMain.addView(obDesc); obMain.addView(obNext);
                applyFont(obMain); 
                obMain.setAlpha(0f); obMain.setTranslationY(50f*DENSITY);
                obMain.animate().alpha(1f).translationY(0).setDuration(400).setInterpolator(new OvershootInterpolator()).start();
            }
        };
        
        obNext.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                if (step[0] < titles.length - 1) { step[0]++; updateSlide.run(); } 
                else {
                    sp.edit().putBoolean("is_first_run_tutorial", false).apply();
                    obRoot.animate().alpha(0f).translationY(-100f*DENSITY).setDuration(500).withEndAction(new Runnable() { @Override public void run() { root.removeView(obRoot); } }).start();
                }
            }
        });

        updateSlide.run(); obRoot.addView(obMain); root.addView(obRoot);
    }
}