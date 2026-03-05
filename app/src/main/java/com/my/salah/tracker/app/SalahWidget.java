package com.my.salah.tracker.app;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.os.Build;
import android.widget.RemoteViews;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class SalahWidget extends AppWidgetProvider {
    private static final String ACTION_TOGGLE = "com.my.salah.tracker.app.TOGGLE_PRAYER";
    private static final String EXTRA_PRAYER_NAME = "prayer_name";

    public static Bitmap buildTextBitmap(Context ctx, String text, int color, float sizeSp, Typeface tf) {
        Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        paint.setTextSize(sizeSp * ctx.getResources().getDisplayMetrics().scaledDensity);
        paint.setColor(color);
        paint.setTypeface(tf);
        paint.setTextAlign(Paint.Align.LEFT);
        Paint.FontMetrics fm = paint.getFontMetrics();
        float w = paint.measureText(text); float h = fm.descent - fm.ascent;
        if (w <= 0) w = 1;
        Bitmap bmp = Bitmap.createBitmap((int) w + 4, (int) h + 4, Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bmp);
        canvas.drawText(text, 2, -fm.ascent + 2, paint);
        return bmp;
    }

    // ✨ বাংলা তারিখের গ্রামার লজিক (১লা, ২রা, ৫ই, ১৯শে) ✨
    public static String getBnSuffix(int d) {
        if(d == 1) return "লা"; if(d == 2 || d == 3) return "রা"; if(d == 4) return "ঠা";
        if(d >= 5 && d <= 18) return "ই"; return "শে";
    }

    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        for (int appWidgetId : appWidgetIds) updateAppWidget(context, appWidgetManager, appWidgetId);
    }
    
    @Override
    public void onReceive(Context context, Intent intent) {
        super.onReceive(context, intent);
        if (ACTION_TOGGLE.equals(intent.getAction())) {
            String prayerName = intent.getStringExtra(EXTRA_PRAYER_NAME);
            if (prayerName != null) {
                SharedPreferences sp = context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE);
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
                String todayKey = sdf.format(new Date());
                String currentStatus = sp.getString(todayKey + "_" + prayerName, "no");
                sp.edit().putString(todayKey + "_" + prayerName, currentStatus.equals("yes") ? "no" : "yes").apply();
                AppWidgetManager appWidgetManager = AppWidgetManager.getInstance(context);
                onUpdate(context, appWidgetManager, appWidgetManager.getAppWidgetIds(new ComponentName(context, SalahWidget.class)));
            }
        }
    }

    static void updateAppWidget(Context context, AppWidgetManager appWidgetManager, int appWidgetId) {
        SharedPreferences sp = context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE);
        LanguageEngine lang = new LanguageEngine(sp.getString("app_lang", "en"));
        RemoteViews views = new RemoteViews(context.getPackageName(), context.getResources().getIdentifier("salah_widget", "layout", context.getPackageName()));

        boolean systemDark = (context.getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;
        boolean isDarkTheme = sp.getBoolean("is_dark_mode", systemDark);
        boolean isBn = sp.getString("app_lang", "en").equals("bn");

        int mainBgColor = isDarkTheme ? Color.parseColor("#1C1C1E") : Color.parseColor("#FFFFFF");
        int cardEmptyBorderColor = isDarkTheme ? Color.parseColor("#38383A") : Color.parseColor("#E2E8F0");
        int mainTextColor = isDarkTheme ? Color.WHITE : Color.parseColor("#141416");
        int subTextColor = isDarkTheme ? Color.parseColor("#A0A0A5") : Color.parseColor("#64748B");
        int progressBgColor = isDarkTheme ? Color.parseColor("#2C2C2E") : Color.parseColor("#E2E8F0");

        int activeTheme = sp.getInt("app_theme", 0);
        String[] themeAccents = {"#00BFA5", "#3B82F6", "#FF9559", "#D81B60", "#A67BFF", "#3BCC75"};
        int colorAccent = Color.parseColor(themeAccents[activeTheme]);

        views.setInt(context.getResources().getIdentifier("widget_outer_border", "id", context.getPackageName()), "setColorFilter", colorAccent);
        views.setInt(context.getResources().getIdentifier("widget_inner_bg", "id", context.getPackageName()), "setColorFilter", mainBgColor);

        Typeface appFontBold;
        try {
            if (isBn) appFontBold = Typeface.createFromAsset(context.getAssets(), "fonts/hind_bold.ttf");
            else appFontBold = Typeface.createFromAsset(context.getAssets(), "fonts/poppins_bold.ttf");
        } catch (Exception e) { appFontBold = Typeface.DEFAULT_BOLD; }

        SimpleDateFormat sdfKey = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
        String todayKey = sdfKey.format(new Date());
        
        String hijriText = "";
        try {
            if (Build.VERSION.SDK_INT >= 24) {
                android.icu.util.IslamicCalendar hijriCal = new android.icu.util.IslamicCalendar();
                hijriCal.add(android.icu.util.IslamicCalendar.DATE, sp.getInt("hijri_offset", 0));
                String[] hMonths = {"Muharram", "Safar", "Rabi I", "Rabi II", "Jumada I", "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"};
                int hD = hijriCal.get(android.icu.util.IslamicCalendar.DAY_OF_MONTH);
                hijriText = lang.bnNum(hD) + (isBn ? getBnSuffix(hD) : "") + " " + lang.get(hMonths[hijriCal.get(android.icu.util.IslamicCalendar.MONTH)]) + " " + lang.bnNum(hijriCal.get(android.icu.util.IslamicCalendar.YEAR)) + " " + lang.get("AH");
            } else { hijriText = lang.bnNum(16) + (isBn ? "ই " : " ") + lang.get("Ramadan") + " " + lang.bnNum(1447) + " " + lang.get("AH"); }
        } catch (Exception e) {}

        String gregText;
        Calendar c = Calendar.getInstance();
        if (isBn) {
            String[] bnDays = {"রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার"};
            String[] bnMonths = {"জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"};
            int gD = c.get(Calendar.DAY_OF_MONTH);
            gregText = bnDays[c.get(Calendar.DAY_OF_WEEK) - 1] + ", " + lang.bnNum(gD) + getBnSuffix(gD) + " " + bnMonths[c.get(Calendar.MONTH)];
        } else {
            SimpleDateFormat sdfGreg = new SimpleDateFormat("EEEE, MMM dd", Locale.US);
            gregText = sdfGreg.format(new Date());
        }

        views.setImageViewBitmap(context.getResources().getIdentifier("widget_hijri_date_img", "id", context.getPackageName()), buildTextBitmap(context, hijriText, subTextColor, 13f, appFontBold));
        views.setInt(context.getResources().getIdentifier("widget_hijri_icon", "id", context.getPackageName()), "setColorFilter", subTextColor);
        views.setImageViewBitmap(context.getResources().getIdentifier("widget_greg_date_img", "id", context.getPackageName()), buildTextBitmap(context, gregText, mainTextColor, 18f, appFontBold));
        
        // ✨ পার্সেন্টেজ বক্স ডিজাইন (বর্ডার কালারফুল, ভেতরটা সাদা/কালো) ✨
        views.setInt(context.getResources().getIdentifier("widget_percent_border", "id", context.getPackageName()), "setColorFilter", colorAccent);
        views.setInt(context.getResources().getIdentifier("widget_percent_inner", "id", context.getPackageName()), "setColorFilter", mainBgColor);

        int countCompleted = 0;
        String[] pNames = AppConstants.PRAYERS;
        String[] pImgs = {"img_fajr", "img_dhuhr", "img_asr", "img_maghrib", "img_isha", "img_witr"};
        String[] boxIds = {"box_fajr", "box_dhuhr", "box_asr", "box_maghrib", "box_isha", "box_witr"};

        for (int i = 0; i < 6; i++) {
            String stat = sp.getString(todayKey + "_" + pNames[i], "no");
            boolean isDone = stat.equals("yes") || stat.equals("excused");
            if (isDone) countCompleted++;

            int boxId = context.getResources().getIdentifier(boxIds[i], "id", context.getPackageName());
            int iconId = context.getResources().getIdentifier("w_icon", "id", context.getPackageName());
            int textId = context.getResources().getIdentifier("w_name_img", "id", context.getPackageName());
            int borderId = context.getResources().getIdentifier("card_border", "id", context.getPackageName());
            int innerId = context.getResources().getIdentifier("card_inner", "id", context.getPackageName());

            RemoteViews prayerBox = new RemoteViews(context.getPackageName(), context.getResources().getIdentifier("widget_prayer_item", "layout", context.getPackageName()));

            // ✨ নামাজের ফন্ট কালার সবসময় ধ্রুবক (সাদা/কালো) থাকবে ✨
            prayerBox.setImageViewBitmap(textId, buildTextBitmap(context, lang.get(pNames[i]), mainTextColor, 14f, appFontBold));

            prayerBox.setInt(innerId, "setColorFilter", mainBgColor);
            if (isDone) prayerBox.setInt(borderId, "setColorFilter", colorAccent);
            else prayerBox.setInt(borderId, "setColorFilter", cardEmptyBorderColor);

            prayerBox.setImageViewResource(iconId, context.getResources().getIdentifier(pImgs[i], "drawable", context.getPackageName()));
            if (isDone) prayerBox.setInt(iconId, "setColorFilter", colorAccent); else prayerBox.setInt(iconId, "setColorFilter", subTextColor);

            Intent toggleIntent = new Intent(context, SalahWidget.class);
            toggleIntent.setAction(ACTION_TOGGLE); toggleIntent.putExtra(EXTRA_PRAYER_NAME, pNames[i]);
            PendingIntent pendingIntent = PendingIntent.getBroadcast(context, i, toggleIntent, PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= 23 ? PendingIntent.FLAG_IMMUTABLE : 0));
            prayerBox.setOnClickPendingIntent(context.getResources().getIdentifier("content_box", "id", context.getPackageName()), pendingIntent);
            views.removeAllViews(boxId); views.addView(boxId, prayerBox); views.setOnClickPendingIntent(boxId, pendingIntent);
        }

        int percent = (int) ((countCompleted / 6f) * 100);
        // পার্সেন্টেজ লেখাও সাদা/কালো হবে
        views.setImageViewBitmap(context.getResources().getIdentifier("widget_percent_badge_img", "id", context.getPackageName()), buildTextBitmap(context, lang.bnNum(percent) + "%", mainTextColor, 14f, appFontBold));

        try {
            Bitmap progressBmp = Bitmap.createBitmap(1000, 30, Bitmap.Config.ARGB_8888); Canvas canvas = new Canvas(progressBmp); Paint p = new Paint(Paint.ANTI_ALIAS_FLAG); p.setColor(progressBgColor);
            canvas.drawRoundRect(new RectF(0, 0, 1000, 30), 15, 15, p);
            if (countCompleted > 0) { p.setColor(colorAccent); canvas.drawRoundRect(new RectF(0, 0, (countCompleted / 6f) * 1000f, 30), 15, 15, p); }
            views.setImageViewBitmap(context.getResources().getIdentifier("widget_progress_img", "id", context.getPackageName()), progressBmp);
        } catch (Exception e) {}

        Intent appIntent = new Intent(context, MainActivity.class);
        PendingIntent appPendingIntent = PendingIntent.getActivity(context, 0, appIntent, PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= 23 ? PendingIntent.FLAG_IMMUTABLE : 0));
        views.setOnClickPendingIntent(context.getResources().getIdentifier("widget_content", "id", context.getPackageName()), appPendingIntent);

        appWidgetManager.updateAppWidget(appWidgetId, views);
    }
}