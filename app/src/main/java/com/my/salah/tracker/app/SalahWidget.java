package com.my.salah.tracker.app;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.widget.RemoteViews;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class SalahWidget extends AppWidgetProvider {

    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        for (int appWidgetId : appWidgetIds) {
            updateAppWidget(context, appWidgetManager, appWidgetId);
        }
    }

    static void updateAppWidget(Context context, AppWidgetManager appWidgetManager, int appWidgetId) {
        SharedPreferences sp = context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
        String today = sdf.format(new Date());
        
        String lang = sp.getString("app_lang", "en");
        boolean isBn = lang.equals("bn");

        RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.salah_widget);

        // Header Date Setup
        SimpleDateFormat dispFormat = new SimpleDateFormat("MMM dd, yyyy", Locale.US);
        String dateStr = dispFormat.format(new Date());
        if(isBn) {
            String s = dateStr;
            String[] en = {"0","1","2","3","4","5","6","7","8","9"};
            String[] bn = {"০","১","২","৩","৪","৫","৬","৭","৮","৯"};
            for(int i=0; i<10; i++) s = s.replace(en[i], bn[i]);
            dateStr = s;
        }
        views.setTextViewText(R.id.widget_title, isBn ? "আজকের নামাজ (" + dateStr + ")" : "Today's Prayers (" + dateStr + ")");

        // Icons and Texts Setup
        String[] prayers = {"Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr"};
        int[] textIds = {R.id.t_fajr, R.id.t_dhuhr, R.id.t_asr, R.id.t_maghrib, R.id.t_isha, R.id.t_witr};
        int[] iconIds = {R.id.i_fajr, R.id.i_dhuhr, R.id.i_asr, R.id.i_maghrib, R.id.i_isha, R.id.i_witr};
        String[] bnNames = {"ফজর", "যোহর", "আসর", "মাগরিব", "এশা", "বিতর"};
        int[] defaultIcons = {R.drawable.img_fajr, R.drawable.img_dhuhr, R.drawable.img_asr, R.drawable.img_maghrib, R.drawable.img_isha, R.drawable.img_witr};

        for(int i=0; i<6; i++) {
            views.setTextViewText(textIds[i], isBn ? bnNames[i] : prayers[i]);
            String stat = sp.getString(today + "_" + prayers[i], "no");
            
            if (stat.equals("yes")) {
                views.setImageViewResource(iconIds[i], R.drawable.img_tick);
            } else if (stat.equals("excused")) {
                views.setImageViewResource(iconIds[i], R.drawable.img_period);
            } else {
                views.setImageViewResource(iconIds[i], defaultIcons[i]);
            }
        }

        // On-Click opens the Main App
        Intent intent = new Intent(context, MainActivity.class);
        PendingIntent pendingIntent;
        if (android.os.Build.VERSION.SDK_INT >= 23) {
            pendingIntent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        } else {
            pendingIntent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);
        }
        views.setOnClickPendingIntent(R.id.widget_root, pendingIntent);

        appWidgetManager.updateAppWidget(appWidgetId, views);
    }
}