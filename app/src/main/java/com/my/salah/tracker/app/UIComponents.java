package com.my.salah.tracker.app;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.ShapeDrawable;
import android.graphics.drawable.shapes.OvalShape;
import android.icu.util.IslamicCalendar;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.content.SharedPreferences;

public class UIComponents {
    private Activity activity;
    private float DENSITY;
    private int[] themeColors;
    private LanguageEngine lang;
    private LinearLayout activeBanner = null;

    public UIComponents(Activity activity, float DENSITY, int[] themeColors, LanguageEngine lang) {
        this.activity = activity;
        this.DENSITY = DENSITY;
        this.themeColors = themeColors;
        this.lang = lang;
    }

    public View getPremiumIcon(String emoji, int colorStart, int colorEnd, int sizeDp) { 
        TextView tv = new TextView(activity); tv.setText(emoji); tv.setTextColor(Color.WHITE); tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setTextSize(sizeDp / 2.5f); tv.setGravity(Gravity.CENTER); 
        GradientDrawable gd = new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{colorStart, colorEnd}); gd.setShape(GradientDrawable.OVAL); tv.setBackground(gd); 
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams((int)(sizeDp*DENSITY), (int)(sizeDp*DENSITY)); tv.setLayoutParams(lp); return tv; 
    }
    
    public View getRoundImage(String resName, int paddingDp, int bgHex, int tintHex) { 
        FrameLayout wrap = new FrameLayout(activity); GradientDrawable gd = new GradientDrawable(); gd.setShape(GradientDrawable.OVAL); gd.setColor(bgHex); wrap.setBackground(gd); 
        ImageView iv = new ImageView(activity); int resID = activity.getResources().getIdentifier(resName, "drawable", activity.getPackageName()); if (resID != 0) iv.setImageResource(resID); iv.setScaleType(ImageView.ScaleType.FIT_CENTER); 
        if (tintHex != 0) iv.setColorFilter(tintHex, android.graphics.PorterDuff.Mode.SRC_IN);
        FrameLayout.LayoutParams ivLp = new FrameLayout.LayoutParams(-1, -1); ivLp.setMargins((int)(paddingDp*DENSITY), (int)(paddingDp*DENSITY), (int)(paddingDp*DENSITY), (int)(paddingDp*DENSITY)); iv.setLayoutParams(ivLp); wrap.addView(iv); return wrap; 
    }

    public String getHijriDate(java.util.Date date, int offsetDays) { 
        try { 
            if (Build.VERSION.SDK_INT >= 24) { 
                IslamicCalendar hijriCal = new IslamicCalendar(); hijriCal.setTime(date); hijriCal.add(IslamicCalendar.DATE, offsetDays); 
                String[] hMonths = {"Muharram", "Safar", "Rabi I", "Rabi II", "Jumada I", "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"}; 
                String day = lang.bnNum(hijriCal.get(IslamicCalendar.DAY_OF_MONTH));
                String month = lang.get(hMonths[hijriCal.get(IslamicCalendar.MONTH)]);
                String year = lang.bnNum(hijriCal.get(IslamicCalendar.YEAR));
                String ah = lang.get("AH");
                return day + " " + month + " " + year + " " + ah; 
            } else { return lang.bnNum(16) + " " + lang.get("Ramadan") + " " + lang.bnNum(1447) + " " + lang.get("AH"); } 
        } catch (Exception e) { return "Error Date"; } 
    }

    public View getPremiumCheckbox(String status, int activeColorHex) { 
        TextView tv = new TextView(activity); tv.setGravity(Gravity.CENTER); tv.setTextSize(14); 
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); tv.setLayoutParams(lp); 
        GradientDrawable gd = new GradientDrawable(); gd.setShape(GradientDrawable.OVAL); 
        if(status.equals("yes")) { gd.setColor(activeColorHex); tv.setText("✓"); tv.setTextColor(Color.WHITE); } 
        else if (status.equals("excused")) { gd.setColor(activeColorHex); tv.setText("🌸"); tv.setTextColor(Color.WHITE); } 
        else { gd.setColor(Color.TRANSPARENT); gd.setStroke((int)(2*DENSITY), themeColors[4]); tv.setText(""); } 
        tv.setBackground(gd); return tv; 
    }

    public int calculateStreak(SharedPreferences prefs, String[] prayerArray) { 
        java.text.SimpleDateFormat format = new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US); java.util.Calendar c = java.util.Calendar.getInstance(); int streak = 0; 
        for(int i=0; i<3650; i++) { String dKey = format.format(c.getTime()); boolean done = true; 
            for(String p : prayerArray) { String stat = prefs.getString(dKey+"_"+p, "no"); if(!stat.equals("yes") && !stat.equals("excused")) { done = false; break; } } 
            if(done) { streak++; c.add(java.util.Calendar.DATE, -1); } else break; 
        } return streak; 
    }

    public android.graphics.drawable.Drawable getRainbowBorder(final String dateKey, final int strokeWidthDp) { 
        return new ShapeDrawable(new OvalShape()) { 
            @Override public void draw(android.graphics.Canvas canvas) { android.graphics.Paint paint = new android.graphics.Paint(1); paint.setStyle(android.graphics.Paint.Style.FILL); paint.setColor(themeColors[1]); canvas.drawOval(new android.graphics.RectF(0, 0, getBounds().width(), getBounds().height()), paint); } 
        }; 
    }

    public void showSmartBanner(final FrameLayout root, final String titleStr, final String msg, final String imgName, final int colorAccent, final Runnable onClick) { 
        activity.runOnUiThread(new Runnable() { 
            @Override public void run() { 
                if (activeBanner != null) { root.removeView(activeBanner); activeBanner = null; } 
                activeBanner = new LinearLayout(activity); activeBanner.setOrientation(LinearLayout.VERTICAL); 
                GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); gd.setStroke((int)(1.5f*DENSITY), colorAccent); activeBanner.setBackground(gd); 
                if (Build.VERSION.SDK_INT >= 21) activeBanner.setElevation(40f); 
                LinearLayout topRow = new LinearLayout(activity); topRow.setOrientation(LinearLayout.HORIZONTAL); topRow.setGravity(Gravity.CENTER_VERTICAL); topRow.setPadding((int)(20*DENSITY), (int)(15*DENSITY), (int)(20*DENSITY), (int)(15*DENSITY)); 
                View icon = getRoundImage(imgName, 2, Color.TRANSPARENT, colorAccent); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); icLp.setMargins(0,0,(int)(12*DENSITY),0); icon.setLayoutParams(icLp); 
                LinearLayout textCol = new LinearLayout(activity); textCol.setOrientation(LinearLayout.VERTICAL); TextView title = new TextView(activity); title.setText(lang.get(titleStr)); title.setTextColor(themeColors[2]); title.setTextSize(14); title.setTypeface(Typeface.DEFAULT_BOLD); 
                TextView sub = new TextView(activity); sub.setText(lang.get(msg)); sub.setTextColor(themeColors[3]); sub.setTextSize(11); textCol.addView(title); textCol.addView(sub); topRow.addView(icon); topRow.addView(textCol); activeBanner.addView(topRow); 
                if (onClick != null) { activeBanner.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { onClick.run(); hideLoadingBanner(root); } }); } 
                FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(-1, -2); lp.gravity = Gravity.TOP; lp.setMargins((int)(20*DENSITY), (int)(50*DENSITY), (int)(20*DENSITY), 0); root.addView(activeBanner, lp); 
                activeBanner.setTranslationY(-250f * DENSITY); activeBanner.setAlpha(0f); activeBanner.animate().translationY(0).alpha(1f).setDuration(500).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); 
                if (onClick == null) { new Handler(Looper.getMainLooper()).postDelayed(new Runnable() { @Override public void run() { hideLoadingBanner(root); } }, 2500); } 
            } 
        }); 
    }

    public void hideLoadingBanner(final FrameLayout root) { 
        activity.runOnUiThread(new Runnable() { 
            @Override public void run() { if(activeBanner != null) { activeBanner.animate().translationY(-250f * DENSITY).alpha(0f).setDuration(400).setInterpolator(new android.view.animation.AnticipateInterpolator()).withEndAction(new Runnable() { @Override public void run() { root.removeView(activeBanner); activeBanner = null; } }).start(); } } 
        }); 
    }

    // ✨ FIX: 100% Crash-Proof Custom Native Dialog (Replaced buggy SweetAlertDialog)
    public void showPremiumLocked(int colorAccent) { 
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); 
        LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setGravity(Gravity.CENTER); main.setPadding((int)(25*DENSITY), (int)(35*DENSITY), (int)(25*DENSITY), (int)(35*DENSITY)); 
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(30f * DENSITY); main.setBackground(gd); 
        
        TextView iconView = new TextView(activity); iconView.setText("⏳"); iconView.setTextSize(50); iconView.setGravity(Gravity.CENTER); main.addView(iconView);
        android.animation.ObjectAnimator rot = android.animation.ObjectAnimator.ofFloat(iconView, "rotation", 0f, 15f, -15f, 15f, -15f, 0f);
        rot.setDuration(500); rot.start();

        TextView title = new TextView(activity); title.setText(lang.get("Patience is Virtue")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0,(int)(15*DENSITY),0,(int)(5*DENSITY)); main.addView(title); 
        TextView sub = new TextView(activity); sub.setText(lang.get("You cannot mark future prayers.")); sub.setTextColor(themeColors[3]); sub.setTextSize(14); sub.setGravity(Gravity.CENTER); main.addView(sub);
        
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(280*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp); 
        
        android.app.AlertDialog ad = new android.app.AlertDialog.Builder(activity).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(Gravity.CENTER); 
        ad.show(); 
    }
}