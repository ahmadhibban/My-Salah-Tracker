package com.my.salah.tracker.app;
import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

public class OnboardingHelper {
    private Activity activity; private float DENSITY; private int[] themeColors; private int colorAccent; private LanguageEngine lang; private UIComponents ui; private SharedPreferences sp; private FrameLayout root; private Typeface[] appFonts;
    private int currentPage = 0;
    public OnboardingHelper(Activity activity, float DENSITY, int[] themeColors, int colorAccent, LanguageEngine lang, UIComponents ui, SharedPreferences sp, FrameLayout root, Typeface[] appFonts) {
        this.activity = activity; this.DENSITY = DENSITY; this.themeColors = themeColors; this.colorAccent = colorAccent; this.lang = lang; this.ui = ui; this.sp = sp; this.root = root; this.appFonts = appFonts;
    }
    public void showOnboarding() {
        final FrameLayout overlay = new FrameLayout(activity); overlay.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); overlay.setBackgroundColor(themeColors[0]); overlay.setClickable(true);
        final LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setGravity(Gravity.CENTER); main.setPadding((int) (30 * DENSITY), (int) (30 * DENSITY), (int) (30 * DENSITY), (int) (30 * DENSITY));
        final FrameLayout iconContainer = new FrameLayout(activity); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int) (120 * DENSITY), (int) (120 * DENSITY)); icLp.setMargins(0, 0, 0, (int) (30 * DENSITY)); iconContainer.setLayoutParams(icLp);
        final TextView title = new TextView(activity); title.setTextColor(themeColors[2]); title.setTextSize(24); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0, 0, 0, (int) (15 * DENSITY));
        final TextView desc = new TextView(activity); desc.setTextColor(themeColors[3]); desc.setTextSize(14); desc.setGravity(Gravity.CENTER); desc.setLineSpacing(0, 1.3f); desc.setPadding(0, 0, 0, (int) (40 * DENSITY));
        final Button nextBtn = new Button(activity); nextBtn.setText(sp.getString("app_lang", "en").equals("bn") ? "পরবর্তী" : "Next"); nextBtn.setTextColor(Color.WHITE); nextBtn.setAllCaps(false); nextBtn.setTextSize(16); nextBtn.setTypeface(Typeface.DEFAULT_BOLD); GradientDrawable btnBg = new GradientDrawable(); btnBg.setColor(colorAccent); btnBg.setCornerRadius(25f * DENSITY); nextBtn.setBackground(btnBg); LinearLayout.LayoutParams btnLp = new LinearLayout.LayoutParams(-1, (int) (55 * DENSITY)); btnLp.setMargins(0, (int) (20 * DENSITY), 0, 0); nextBtn.setLayoutParams(btnLp);
        main.addView(iconContainer); main.addView(title); main.addView(desc); main.addView(nextBtn); overlay.addView(main); root.addView(overlay);

        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        final String[][] pages = {
                { "img_moon", isBn ? "My Salah Tracker - এ স্বাগতম" : "Welcome to My Salah Tracker", isBn ? "আপনার ব্যক্তিগত, আধুনিক এবং বিজ্ঞাপন-মুক্ত সালাহ ট্র্যাকার।" : "Your personal, modern, and ad-free companion to build a consistent prayer habit." },
                { "img_calender", isBn ? "সহজ ট্র্যাকিং" : "Easy Tracking", isBn ? "প্রতিদিনের নামাজগুলো খুব সহজেই মার্ক করুন। আপনার অগ্রগতি এবং কাজা নামাজের হিসেব রাখুন।" : "Mark your daily prayers with ease. Keep track of your progress and pending Qaza." }
        };

        final Runnable updatePage = new Runnable() {
            @Override public void run() {
                iconContainer.removeAllViews();
                View icon = ui.getRoundImage(pages[currentPage][0], 0, Color.TRANSPARENT, colorAccent); iconContainer.addView(icon);
                title.setText(pages[currentPage][1]); desc.setText(pages[currentPage][2]);
                if (currentPage == pages.length - 1) nextBtn.setText(sp.getString("app_lang", "en").equals("bn") ? "শুরু করুন" : "Get Started");
            }
        };
        updatePage.run();
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                if (currentPage < pages.length - 1) { currentPage++; updatePage.run(); } else {
                    sp.edit().putBoolean("is_first_run_tutorial", false).apply();
                    overlay.animate().alpha(0f).setDuration(300).withEndAction(new Runnable() { @Override public void run() { root.removeView(overlay); } }).start();
                }
            }
        });
        applyFont(main, appFonts[0], appFonts[1]);
    }
    private void applyFont(View v, Typeface reg, Typeface bold) {
        if (v instanceof TextView) { TextView tv = (TextView) v; if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(bold); else tv.setTypeface(reg);
        } else if (v instanceof ViewGroup) { ViewGroup vg = (ViewGroup) v; for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i), reg, bold); }
    }
}
